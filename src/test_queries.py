from src.services.queries import (
    cheapest_fuel_nearby,
    trending_fuels,
    cheapest_overall
)


print("\n⛽ MAIS BARATO PRÓXIMO")
print(cheapest_fuel_nearby(-23.55, -46.63))

print("\n🔥 TRENDING")
print(trending_fuels())

print("\n🏆 RANKING GLOBAL")
print(cheapest_overall())