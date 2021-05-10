import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)


def get_app():
    app = FastAPI()

    from .user.endpoints import init_app
    init_app(app)

    @app.get("/ping")
    async def ping():
        from .db import db
        async with db.transaction() as tx:
            await tx.execute("""
            INSERT User {
                username := "test3"
            };
            """)
            result = await tx.query_json("SELECT User {username};")
        return result
    from .db import EdgeDBMiddleware
    app.add_middleware(EdgeDBMiddleware)
    return app
