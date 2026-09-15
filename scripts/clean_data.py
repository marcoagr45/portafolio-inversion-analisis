import pandas as pd
datos = pd.read_csv('data/raw/precios_combinados.csv', parse_dates=['Date'])
#print(datos.dtypes)
datos['Date'] = pd.to_datetime(datos['Date'])
tickers_unicos = datos['Ticker'].unique()
resultados_limpios = []
for ticker in tickers_unicos:
    data_ticker = datos[datos['Ticker'] == ticker].set_index('Date')
    full_range = pd.date_range(start=data_ticker.index.min(), end=data_ticker.index.max(), name='Date')
    full_data = data_ticker.reindex(full_range)
    full_data = full_data.ffill()
    resultados_limpios.append(full_data)
tabla_final_limpia = pd.concat(resultados_limpios)
tabla_final_limpia = tabla_final_limpia.reset_index()
tabla_final_limpia.to_csv('data/processed/precios_limpios.csv', index=False)


