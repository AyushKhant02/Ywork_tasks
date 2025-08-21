# core/mongo.py
from django.conf import settings
from pymongo import MongoClient, ASCENDING

_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        _client = MongoClient(settings.MONGODB_URI)
        db = _client[settings.MONGODB_DB]
        _collection = db[settings.MONGODB_COLLECTION]
        # Partition key & sort index
        _collection.create_index([("group", ASCENDING), ("ts", ASCENDING)])
    return _collection
