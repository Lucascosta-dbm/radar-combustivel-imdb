from src.config.connections import get_redis

r = get_redis()


# ======================================
# 1️⃣ Combustível mais barato
# ======================================
def cheapest_stations(fuel, limit=5):

    key = f"ranking:{fuel}:price"

    data = r.zrange(key, 0, limit - 1, withscores=True)

    return [
        {"station_id": s, "price": p}
        for s, p in data
    ]


# ======================================
# 2️⃣ Combustíveis trending
# ======================================
def trending_fuels(limit=5):

    return r.zrevrange(
        "ranking:search:fuel",
        0,
        limit - 1,
        withscores=True
    )