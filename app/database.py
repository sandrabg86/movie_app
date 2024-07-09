from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(settings.mongodb_url)

async def close_mongo_connection():
    global client
    if client:
        client.close()

def get_database():
    global client
    return client.movie_db