from gino import Gino

db = Gino()

async def init_db():
    await db.set_bind("postgresql+asyncpg://root:root@localhost:5432/forum")
    await db.gino.create_all()