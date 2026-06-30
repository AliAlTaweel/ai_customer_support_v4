from prisma import Prisma
from config import settings

db = Prisma()

async def connect_db():
    await db.connect()

async def disconnect_db():
    await db.disconnect()

async def get_db():
    return db
