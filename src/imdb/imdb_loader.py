from src.config.connections import get_mongo_db, get_redis
from tqdm import tqdm

mongo = get_mongo_db()
redis = get_redis()


def load_prices_to_redis():

    print("Carregando eventos_preco → Redis")

    eventos = mongo.eventos_preco.find({}).sort("data_coleta", 1)

    # guarda último preço por posto + combustível
    last_price = {}

    for ev in tqdm(eventos):

        station_id = str(ev["posto_id"])
        combustivel = ev["combustivel"]

        # dataset oficial usa preco_novo
        preco = float(ev["preco_novo"])

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