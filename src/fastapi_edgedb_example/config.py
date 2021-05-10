from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=True)
DB_DSN = config("DB_DSN", cast=str, default=None)
