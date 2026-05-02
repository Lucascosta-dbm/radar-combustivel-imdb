import uuid
import random
from datetime import datetime
from src.config.connections import get_mongo_db


db = get_mongo_db()
events = db["events"]

# 25 postos reais espalhados por São Paulo e Grande SP
STATIONS = [
    {"id": "station_sp_001", "name": "Posto Ipiranga Paulista",      "brand": "Ipiranga",      "lat": -23.5630, "lng": -46.6950, "address": "Av. Rebouças 1500",           "region": "SP_PINHEIROS"},
    {"id": "station_sp_002", "name": "Posto Shell Moema",            "brand": "Shell",          "lat": -23.6014, "lng": -46.6640, "address": "Av. Ibirapuera 2800",          "region": "SP_MOEMA"},
    {"id": "station_sp_003", "name": "Posto BR Vila Mariana",        "brand": "BR",             "lat": -23.5836, "lng": -46.6383, "address": "Rua Domingos de Morais 1200",  "region": "SP_VILA_MARIANA"},
    {"id": "station_sp_004", "name": "Posto Raízen Santana",         "brand": "Raízen",         "lat": -23.5027, "lng": -46.6271, "address": "Av. Braz Leme 2000",           "region": "SP_SANTANA"},
    {"id": "station_sp_005", "name": "Posto Ale Tatuapé",            "brand": "Ale",            "lat": -23.5415, "lng": -46.5710, "address": "Rua Melo Freire 500",          "region": "SP_TATUAPE"},
    {"id": "station_sp_006", "name": "Posto Petrobras Lapa",         "brand": "Petrobras",      "lat": -23.5200, "lng": -46.7080, "address": "Av. Antônio Bardella 300",     "region": "SP_LAPA"},
    {"id": "station_sp_007", "name": "Posto Boxter Santo André",     "brand": "Boxter",         "lat": -23.6638, "lng": -46.5330, "address": "Av. Industrial 1800",          "region": "SP_SANTO_ANDRE"},
    {"id": "station_sp_008", "name": "Posto Shell Guarulhos",        "brand": "Shell",          "lat": -23.4627, "lng": -46.5327, "address": "Av. Monteiro Lobato 900",      "region": "SP_GUARULHOS"},
    {"id": "station_sp_009", "name": "Posto Ipiranga Osasco",        "brand": "Ipiranga",       "lat": -23.5322, "lng": -46.7919, "address": "Av. dos Autonomistas 2300",    "region": "SP_OSASCO"},
    {"id": "station_sp_010", "name": "Posto BR São Bernardo",        "brand": "BR",             "lat": -23.6944, "lng": -46.5654, "address": "Av. Kennedy 1500",             "region": "SP_SAO_BERNARDO"},
    {"id": "station_sp_011", "name": "Posto Shell Itaim Bibi",       "brand": "Shell",          "lat": -23.5870, "lng": -46.6800, "address": "Rua Leopoldo Couto 300",       "region": "SP_ITAIM_BIBI"},
    {"id": "station_sp_012", "name": "Posto Raízen Brooklin",        "brand": "Raízen",         "lat": -23.6218, "lng": -46.6922, "address": "Av. Santo Amaro 5000",         "region": "SP_BROOKLIN"},
    {"id": "station_sp_013", "name": "Posto Ale Morumbi",            "brand": "Ale",            "lat": -23.6190, "lng": -46.7180, "address": "Av. Giovanni Gronchi 4700",    "region": "SP_MORUMBI"},
    {"id": "station_sp_014", "name": "Posto Ipiranga Perdizes",      "brand": "Ipiranga",       "lat": -23.5360, "lng": -46.6580, "address": "Rua Cardoso de Almeida 800",   "region": "SP_PERDIZES"},
    {"id": "station_sp_015", "name": "Posto BR Consolação",          "brand": "BR",             "lat": -23.5540, "lng": -46.6560, "address": "Av. Paulista 500",             "region": "SP_CONSOLACAO"},
    {"id": "station_sp_016", "name": "Posto Shell Jabaquara",        "brand": "Shell",          "lat": -23.6480, "lng": -46.6350, "address": "Av. Cupecê 1200",             "region": "SP_JABAQUARA"},
    {"id": "station_sp_017", "name": "Posto Petrobras Penha",        "brand": "Petrobras",      "lat": -23.5312, "lng": -46.5430, "address": "Av. Penha 1800",               "region": "SP_PENHA"},
    {"id": "station_sp_018", "name": "Posto Boxter Ipiranga",        "brand": "Boxter",         "lat": -23.5892, "lng": -46.6050, "address": "Av. Nazaré 700",               "region": "SP_IPIRANGA"},
    {"id": "station_sp_019", "name": "Posto Ale Campo Limpo",        "brand": "Ale",            "lat": -23.6550, "lng": -46.7580, "address": "Estrada do Campo Limpo 2000",  "region": "SP_CAMPO_LIMPO"},
    {"id": "station_sp_020", "name": "Posto Raízen Butantã",         "brand": "Raízen",         "lat": -23.5780, "lng": -46.7280, "address": "Av. Prof. Francisco Morato 2500", "region": "SP_BUTANTA"},
    {"id": "station_sp_021", "name": "Posto Shell Bela Vista",       "brand": "Shell",          "lat": -23.5617, "lng": -46.6441, "address": "Av. Brigadeiro Luis Antonio 2100", "region": "SP_BELA_VISTA"},
    {"id": "station_sp_022", "name": "Posto Ipiranga Jardins",       "brand": "Ipiranga",       "lat": -23.5690, "lng": -46.6630, "address": "Rua Oscar Freire 1400",        "region": "SP_JARDINS"},
    {"id": "station_sp_023", "name": "Posto BR Vila Olímpia",        "brand": "BR",             "lat": -23.5970, "lng": -46.6850, "address": "Av. Funchal 400",              "region": "SP_VILA_OLIMPIA"},
    {"id": "station_sp_024", "name": "Posto Petrobras Barra Funda",  "brand": "Petrobras",      "lat": -23.5240, "lng": -46.6660, "address": "Av. Marquês de São Vicente 1800", "region": "SP_BARRA_FUNDA"},
    {"id": "station_sp_025", "name": "Posto Ale Diadema",            "brand": "Ale",            "lat": -23.6862, "lng": -46.6222, "address": "Av. Piraporinha 1100",         "region": "SP_DIADEMA"},
]

# Faixas de preço por região (ajusta preços realistas 2024)
PRICE_RANGES = {
    "GASOLINA_COMUM":   (5.49, 6.39),
    "GASOLINA_ADITIVADA": (5.79, 6.79),
    "ETANOL":           (3.79, 4.49),
    "DIESEL_S10":       (5.89, 6.49),
}


def generate_station_created(station: dict) -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "station_created",
        "timestamp": datetime.utcnow(),
        "station_id": station["id"],
        "name": station["name"],
        "brand": station["brand"],
        "location": {
            "lat": station["lat"],
            "lng": station["lng"],
            "address": station["address"],
            "region_code": station["region"],
        },
    }


def generate_price_update(station: dict) -> dict:
    fuel_updates = []
    for fuel, (lo, hi) in PRICE_RANGES.items():
        fuel_updates.append({
            "fuel_type": fuel,
            "old_price": round(random.uniform(lo, hi), 2),
            "new_price": round(random.uniform(lo, hi), 2),
        })

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "price_update",
        "timestamp": datetime.utcnow(),
        "station_id": station["id"],
        "fuel_updates": fuel_updates,
    }


def generate_station_search() -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "station_search",
        "timestamp": datetime.utcnow(),
        "user_id": f"user_{uuid.uuid4().hex[:8]}",
        "search_params": {
            "fuel_types": ["GASOLINA_COMUM", "ETANOL"],
            "radius_km": random.choice([1, 2, 3, 5, 10]),
        },
    }


def seed():
    docs = []

    for station in STATIONS:
        docs.append(generate_station_created(station))
        docs.append(generate_price_update(station))

    for _ in range(10):
        docs.append(generate_station_search())

    events.insert_many(docs)
    print(f"{len(docs)} eventos inseridos! ({len(STATIONS)} postos)")


if __name__ == "__main__":
    seed()
