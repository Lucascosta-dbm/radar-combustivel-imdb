from src.config.connections import get_mongo_db, get_redis
from tqdm import tqdm

mongo = get_mongo_db()
redis = get_redis()


def _build_station_name_cache() -> dict:
    """Builds a posto_id_str → nome_fantasia map from MongoDB postos collection."""
    print("Pré-carregando nomes dos postos do MongoDB...")
    cache = {}
    for posto in mongo.postos.find({}, {"_id": 1, "nome_fantasia": 1, "bandeira": 1}):
        key = str(posto["_id"])
        cache[key] = {
            "name":  posto.get("nome_fantasia", key),
            "brand": posto.get("bandeira", ""),
        }
    print(f"  {len(cache)} postos carregados.")
    return cache


def load_prices_to_redis():

    print("Carregando eventos_preco → Redis")

    station_names = _build_station_name_cache()

    eventos = mongo.eventos_preco.find({}).sort("data_coleta", 1)

    # guarda último preço por posto + combustível
    last_price = {}

    registered_ids: set = set()

    for ev in tqdm(eventos):

        station_id = str(ev["posto_id"])
        combustivel = ev["combustivel"]

        # dataset oficial usa preco_novo
        preco = float(ev["preco_novo"])

        # ===============================
        # Nome do posto no Redis (uma vez por posto)
        # ===============================
        if station_id not in registered_ids:
            info = station_names.get(station_id)
            if info:
                redis.hset(
                    f"station:{station_id}:info",
                    mapping={"name": info["name"], "brand": info["brand"]},
                )
            registered_ids.add(station_id)

        # ===============================
        # Ranking de menor preço
        # ===============================
        redis.zadd(
            f"ranking:{combustivel}:price",
            {station_id: preco}
        )

        # ===============================
        # Trending combustível
        # ===============================
        redis.zincrby(
            "ranking:search:fuel",
            1,
            combustivel
        )

        # ===============================
        # ANALYTICS — VARIAÇÃO DE PREÇO
        # ===============================
        key = f"{station_id}:{combustivel}"

        if key in last_price:

            preco_anterior = last_price[key]

            if preco_anterior > 0:
                variacao_pct = (
                    (preco - preco_anterior) / preco_anterior
                ) * 100

                redis.zadd(
                    "ranking:price:variation",
                    {station_id: variacao_pct}
                )

        # atualiza último preço
        last_price[key] = preco

    print("Redis abastecido")


if __name__ == "__main__":
    load_prices_to_redis()