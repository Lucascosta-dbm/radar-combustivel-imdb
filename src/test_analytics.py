from src.queries.analytics_queries import (
    cheapest_stations,
    trending_fuels
)

print("\n⛽ MAIS BARATOS")
print(cheapest_stations("GASOLINA_COMUM"))

print("\n🔥 TRENDING")
print(trending_fuels())