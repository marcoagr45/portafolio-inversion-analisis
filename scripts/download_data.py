import yfinance as yf
import pandas as pd
PERIODO = '5y'
TICKERS = {
    'acciones': ['SPY', 'QQQ', 'AAPL', 'JNJ', 'JPM', 'KO'],
    'cripto': ['BTC-USD', 'ETH-USD', 'SOL-USD']
}
def descargar_activo(ticker):
    datos = yf.download(ticker, period=PERIODO)
    if isinstance(datos.columns,pd.MultiIndex):
        datos.columns = datos.columns.get_level_values(0)
    if datos.empty:
        print(f"No se obtuvieron datos del {ticker}")
        return None
    return datos
resultados_tickers = []
for categoria, lista_tickers in TICKERS.items():
    for ticker in lista_tickers:
        data = descargar_activo(ticker)
        if data is not None:
            data['Ticker'] = ticker
            data['Categoria'] = categoria
            resultados_tickers.append(data)
tabla_final = pd.concat(resultados_tickers)
tabla_final.to_csv('data/raw/precios_combinados.csv') 
