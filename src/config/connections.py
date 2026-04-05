import os
from pymongo import MongoClient
import redis
from dotenv import load_dotenv

load_dotenv()


# ======================
# MONGO
# ======================

def get_mongo_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "radar_combustivel")

    client = MongoClient(mongo_uri)
    return client[db_name]


# ======================
# REDIS
# ======================

def get_redis():
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))

    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        decode_responses=True
    )

    return r