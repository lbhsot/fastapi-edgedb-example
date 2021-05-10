from typing import Any
from fastapi import APIRouter
from ..db import db


router = APIRouter()


@router.get('/users')
async def fetch_users():
    conn = db.conn()
    return await conn.query_json("SELECT User {username};")


@router.get('/post_users')
async def add_user(username: str) -> Any:
    async with db.transaction() as tx:
        result = await tx.query(
            "INSERT User { username := <str>$value };",
            value=username,
        )
    return dict(success=True)


def init_app(app):
    app.include_router(router)
