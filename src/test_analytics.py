from src.queries.analytics_queries import (
    cheapest_stations,
    trending_fuels
)

print("\nMAIS BARATOS")
print(cheapest_stations("GASOLINA_COMUM"))

print("\nTRENDING")
print(trending_fuels())