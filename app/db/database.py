from pymongo import MongoClient
from app.core.config import settings

try:
    # Connect to MongoDB Atlas
    client = MongoClient(settings.MONGODB_URI)

    db = client[settings.DATABASE_NAME]

    client.admin.command('ping')
    print(f"✅ Successfully connected to MongoDB: {settings.DATABASE_NAME}")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
