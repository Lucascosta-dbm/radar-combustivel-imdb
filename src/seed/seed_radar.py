import uuid
from datetime import datetime
from src.config.connections import get_mongo_db


db = get_mongo_db()

events = db["events"]


def generate_station_created():
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "station_created",
        "timestamp": datetime.utcnow(),
        "station_id": "station_br_001",
        "name": "Posto BR Paulista",
        "brand": "BR",
        "location": {
            "lat": -23.5505,
            "lng": -46.6333,
            "address": "Av Paulista 1000",
            "region_code": "SP_CENTRO"
        }
    }


def generate_price_update():
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "price_update",
        "timestamp": datetime.utcnow(),
        "station_id": "station_br_001",
        "fuel_updates": [
            {
                "fuel_type": "gasolina",
                "old_price": 5.79,
                "new_price": 5.92
            },
            {
                "fuel_type": "etanol",
                "old_price": 3.89,
                "new_price": 4.05
            }
        ]
    }


def generate_station_search():
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "station_search",
        "timestamp": datetime.utcnow(),
        "user_id": "user_123",
        "search_params": {
            "fuel_types": ["gasolina", "etanol"],
            "radius_km": 5
        }
    }


def seed():
    docs = []

    for _ in range(5):
        docs.append(generate_station_created())
        docs.append(generate_price_update())
        docs.append(generate_station_search())

    events.insert_many(docs)

    print(f"✅ {len(docs)} eventos inseridos!")


if __name__ == "__main__":
    seed()