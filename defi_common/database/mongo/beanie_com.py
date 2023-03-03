from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from defi_common.database.mongo.models import TraderUpdate
from defi_common.dbconfig import db_config


async def create_beanie():
    client = AsyncIOMotorClient(db_config.mongo_url)
    await init_beanie(database=client.db_name, document_models=[TraderUpdate])
