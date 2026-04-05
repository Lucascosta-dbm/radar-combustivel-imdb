from config.connections import get_mongo_db, get_redis_client


def test_mongo():
    db = get_mongo_db()
    print("Mongo conectado:", db.list_collection_names())


def test_redis():
    r = get_redis_client()
    r.set("teste", "ok")
    print("Redis conectado:", r.get("teste"))


if __name__ == "__main__":
    test_mongo()
    test_redis()