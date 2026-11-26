from intelligence.data.providers.binance import fetch_ohlcv

df = fetch_ohlcv()

print(df.head())
print(df.tail())
print(df.shape)
print(df.dtypes)