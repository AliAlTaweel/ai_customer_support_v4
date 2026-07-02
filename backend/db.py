from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from models import Tenant, TenantUser, Integration, Case, CaseMessage
from logger import logger
import asyncio

client: AsyncIOMotorClient = None
db = None
connection_ready = False

async def connect_to_mongo():
    global client, connection_ready
    try:
        logger.info("Connecting to MongoDB...")
        client = AsyncIOMotorClient(
            settings.mongodb_url,
            connectTimeoutMS=10000,
            serverSelectionTimeoutMS=10000,
            retryWrites=True
        )
        await asyncio.wait_for(client.admin.command('ping'), timeout=10)
        logger.info("✓ Connected to MongoDB")
        connection_ready = True
        return True
    except asyncio.TimeoutError:
        logger.error("MongoDB connection timeout")
        return False
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        return False

async def close_mongo_connection():
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")

async def init_db():
    global db, connection_ready
    try:
        # Try to connect with retries
        for attempt in range(3):
            logger.info(f"MongoDB connection attempt {attempt + 1}/3...")
            success = await connect_to_mongo()
            if success:
                break
            if attempt < 2:
                await asyncio.sleep(2)

        if not connection_ready:
            logger.warning("MongoDB not available - running in fallback mode")
            return

        db = client.get_database(settings.mongodb_db_name)
        await init_beanie(
            database=db,
            models=[Tenant, TenantUser, Integration, Case, CaseMessage]
        )
        logger.info(f"✓ Beanie initialized with database: {settings.mongodb_db_name}")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        logger.warning("Continuing without MongoDB - some features may not work")

async def get_db():
    if not connection_ready:
        await init_db()
    return db
