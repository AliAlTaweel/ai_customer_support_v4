from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from models import Tenant, TenantUser, Integration, Case, CaseMessage
from logger import logger

client: AsyncIOMotorClient = None
db = None

async def connect_to_mongo():
    global client
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        await client.admin.command('ping')
        logger.info("✓ Connected to MongoDB")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")

async def init_db():
    global db
    try:
        await connect_to_mongo()
        db = client.get_database(settings.mongodb_db_name)
        await init_beanie(
            database=db,
            models=[Tenant, TenantUser, Integration, Case, CaseMessage]
        )
        logger.info(f"✓ Beanie initialized with database: {settings.mongodb_db_name}")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

async def get_db():
    if not db:
        await init_db()
    return db
