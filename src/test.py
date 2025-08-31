from exchange_rates import Fx

# EUR/USD currency pair
eur_usd = Fx(base="EUR",quote="USD")

# The most recent reference spot rate
spot_date, spot_rate = eur_usd.spot()
print(spot_date, spot_rate)

# Historical rates
print(eur_usd.rates())

# Visualization
eur_usd.visualize()