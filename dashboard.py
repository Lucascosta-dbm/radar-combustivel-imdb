import streamlit as st
import redis
import pandas as pd
import time

# -----------------------------
# Conexão Redis
# -----------------------------
@st.cache_resource
def get_redis():
    return redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

r = get_redis()

# -----------------------------
# TÍTULO
# -----------------------------
st.title("Radar Combustível — Dashboard Redis")

st.caption("""
Arquitetura:
MongoDB (eventos) → Python Loader → Redis Serving Layer → Streamlit Dashboard
""")

# -----------------------------
# AUTO REFRESH (Real-time feel)
# -----------------------------
REFRESH_SECONDS = 10

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

st.caption(f"Atualização automática a cada {REFRESH_SECONDS}s")

now = time.time()

if now - st.session_state.last_refresh > REFRESH_SECONDS:
    st.session_state.last_refresh = now
    st.rerun()

# -----------------------------
# KPIs (Resumo rápido)
# -----------------------------
st.divider()

col1, col2, col3 = st.columns(3)

total_postos = r.zcard("ranking:GASOLINA_COMUM:price")

buscas = r.zrevrange(
    "ranking:search:fuel", 0, -1, withscores=True
)
total_buscas = sum(score for _, score in buscas)

top_variation = r.zrevrange(
    "ranking:price:variation", 0, 0, withscores=True
)

max_variation = top_variation[0][1] if top_variation else 0

col1.metric("Postos Monitorados", total_postos)
col2.metric("Total de Buscas", int(total_buscas))
col3.metric("Maior Variação", f"{max_variation:.2f}%")

# -----------------------------
# MAIS BARATOS
# -----------------------------
st.header("Postos com menor preço (Gasolina Comum)")

cheap = r.zrange(
    "ranking:GASOLINA_COMUM:price",
    0,
    4,
    withscores=True
)

if cheap:
    for station, price in cheap:
        st.write(f"Posto: `{station}` — R$ {price:.3f}")
else:
    st.warning("Nenhum dado encontrado.")

# -----------------------------
# TRENDING
# -----------------------------
st.header("Combustíveis em alta (buscas)")

trending = r.zrevrange(
    "ranking:search:fuel",
    0,
    4,
    withscores=True
)

if trending:
    for fuel, score in trending:
        st.write(f"{fuel} — {int(score)} buscas")
else:
    st.warning("Nenhum dado encontrado.")

# -----------------------------
# VARIAÇÃO DE PREÇO (Analytics)
# -----------------------------
st.header("Maior variação recente de preço")

try:
    variations = r.zrevrange(
        "ranking:price:variation",
        0,
        4,
        withscores=True
    )

    if variations:
        for station, score in variations:
            st.write(f"Posto `{station}` — variação {score:.2f}%")
    else:
        st.info("Sem dados de variação ainda.")

except Exception as e:
    st.error(f"Erro analytics: {e}")

# -----------------------------
# INFO PIPELINE
# -----------------------------
st.divider()

st.success(" Dados servidos diretamente do Redis (Serving Layer)")

# -----------------------------
# MAPA DE POSTOS (REDIS GEO)
# -----------------------------
st.header("Postos próximos (Mapa)")

try:
    members = r.zrange("stations:geo", 0, -1)
    coords = r.geopos("stations:geo", *members)

    data = []

    for coord in coords:
        if coord:
            lon, lat = coord
            data.append({
                "lat": float(lat),
                "lon": float(lon)
            })

    if data:
        df = pd.DataFrame(data)
        st.map(df)
    else:
        st.info("Nenhum posto encontrado no GEO.")

except Exception as e:
    st.error(f"Erro ao carregar mapa: {e}")