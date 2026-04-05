from src.config.connections import get_mongo_db, get_redis_client

db = get_mongo_db()
redis_client = get_redis_client()

events_collection = db["events"]


# =========================
# HANDLERS
# =========================

def handle_station_created(event):
    station_id = event["station_id"]
    lat = event["location"]["lat"]
    lng = event["location"]["lng"]

    redis_client.geoadd(
        "stations:geo",
        (lng, lat, station_id)
    )

    print(f"GEOADD station {station_id}")


def handle_price_update(event):
    station_id = event["station_id"]

    for fuel in event["fuel_updates"]:
        fuel_type = fuel["fuel_type"]
        price = fuel["new_price"]

        # estado atual
        redis_client.hset(
            f"station:{station_id}:prices",
            fuel_type,
            price
        )

        # ranking por preço
        redis_client.zadd(
            f"ranking:{fuel_type}:price",
            {station_id: price}
        )

    print(f"PRICE UPDATE {station_id}")


def handle_station_search(event):
    fuels = event["search_params"]["fuel_types"]

    for fuel in fuels:
        redis_client.zincrby(
            "ranking:search:fuel",
            1,
            fuel
        )

    print("SEARCH TREND updated")


# =========================
# ROUTER
# =========================

def process_event(event):
    event_type = event["event_type"]

    if event_type == "station_created":
        handle_station_created(event)

    elif event_type == "price_update":
        handle_price_update(event)

    elif event_type == "station_search":
        handle_station_search(event)


# =========================
# MAIN
# =========================

def run():
    events = events_collection.find()

    for event in events:
        process_event(event)

    print("Processing finalizado")


if __name__ == "__main__":
    run()