import pandas as pd
datos_ejemplo = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02', '2024-01-05', '2024-01-01','2024-01-02','2024-01-03'],
    'Ticker': ['AAPL','AAPL','AAPL','BTC-USD','BTC-USD','BTC-USD'],
    'Close': [180,182,185,420000,42500,43000]
})
datos_ejemplo['Date'] = pd.to_datetime(datos_ejemplo['Date'])
lista_tickers_unicos = datos_ejemplo['Ticker'].unique()
for ticker in lista_tickers_unicos:
    datos_del_ticker = datos_ejemplo[datos_ejemplo['Ticker'] == ticker]
    print(f"--- Datos de {ticker} ---")
    print(datos_del_ticker)
datos_aapl = datos_ejemplo[datos_ejemplo['Ticker'] == 'AAPL'].set_index('Date')
rango_completo =pd.date_range(start=datos_aapl.index.min(), end=datos_aapl.index.max())
datos_aapl_completo = datos_aapl.reindex(rango_completo)
datos_aapl_completo = datos_aapl_completo.ffill()
print(datos_aapl_completo)