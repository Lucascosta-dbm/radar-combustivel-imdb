import redis
import pandas as pd

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def postos_proximos(lat, lon, raio_km=5):

    results = r.geosearch(
        "stations:geo",
        longitude=lon,
        latitude=lat,
        radius=raio_km,
        unit="km",
        withdist=True
    )

    data = []

    for station_id, dist in results:
        prices = r.hgetall(f"station:{station_id}:prices")

        data.append({
            "station_id": station_id,
            "distancia_km": float(dist),
            "gasolina": prices.get("GASOLINA_COMUM"),
            "etanol": prices.get("ETANOL")
        })

    return pd.DataFrame(data)