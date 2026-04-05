from src.config.connections import get_redis_client

redis_client = get_redis_client()


# ==================================
# 1️⃣ combustível mais barato perto
# ==================================

def cheapest_fuel_nearby(lat, lng, radius_km=5, fuel_type="gasolina"):
    stations = redis_client.georadius(
        "stations:geo",
        lng,
        lat,
        radius_km,
        unit="km"
    )

    results = []

    for station_id in stations:
        price = redis_client.hget(
            f"station:{station_id}:prices",
            fuel_type
        )

        if price:
            results.append(
                {
                    "station_id": station_id,
                    "price": float(price)
                }
            )

    return sorted(results, key=lambda x: x["price"])


# ==================================
# 2️⃣ combustíveis em alta
# ==================================

def trending_fuels(top_n=5):
    return redis_client.zrevrange(
        "ranking:search:fuel",
        0,
        top_n - 1,
        withscores=True
    )


# ==================================
# 3️⃣ ranking por preço global
# ==================================

def cheapest_overall(fuel_type="gasolina"):
    return redis_client.zrange(
        f"ranking:{fuel_type}:price",
        0,
        -1,
        withscores=True
    )