from envparse import Env


env = Env()

DATABASE_URL = env.str(
    'DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres'
)
