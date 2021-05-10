from asyncio import Queue
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Optional

from edgedb import AsyncIOPool, create_async_pool
from edgedb.asyncio_pool import PoolConnection
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from . import config

_request_scope_context_storage: ContextVar[PoolConnection] = ContextVar(
    "request_context"
)


class ConnectionMeta(type):
    @property
    def conn(self):
        conn = _request_scope_context_storage.get()
        if conn is None:
            raise
        return conn


class Connection(metaclass=ConnectionMeta):
    def __init__(self):
        self.token = None

    async def __aenter__(self):
        pool = await db.get_pool()
        conn = await pool.acquire()
        self.token = _request_scope_context_storage.set(conn)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pool = await db.get_pool()
        conn = _request_scope_context_storage.get()
        await pool.release(conn)
        _request_scope_context_storage.reset(self.token)


class EdgeDBMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        async with connection() as conn:
            response = await call_next(request)
        return response


connection: ConnectionMeta = Connection


class DB:
    _pool: Optional[AsyncIOPool] = None

    async def init_pool(self) -> AsyncIOPool:
        self._pool = await create_async_pool(config.DB_DSN)
        return self._pool

    async def get_pool(self) -> AsyncIOPool:
        if self._pool is not None:
            return self._pool
        return await self.init_pool()

    @asynccontextmanager
    async def transaction(self, conn=None):
        if not conn:
            conn = self.conn()
        async for tx in conn.retrying_transaction():
            async with tx:
                yield tx

    def conn(self):
        return connection.conn


db = DB()
