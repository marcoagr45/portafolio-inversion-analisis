import pandas as pd
datos = pd.read_csv('data/processed/precios_limpios.csv', parse_dates=['Date'])
datos = datos.sort_values(by=['Ticker', 'Date'])
datos['retorno_diario'] = datos.groupby('Ticker')['Close'].pct_change()
datos['retorno_diario_mas_uno'] = 1 + datos['retorno_diario']
datos['retorno_acumulado'] = datos.groupby('Ticker')['retorno_diario_mas_uno'].cumprod()
print(datos['Ticker'].unique())
print(datos['Ticker'].nunique())
volatilidad_por_ticker = datos.groupby('Ticker')['retorno_diario'].std()
tasa_libre_riesgo_anual = 0.04  # 4% anual, aproximado en bonos USD
tasa_libre_riesgo_diaria = (1 + tasa_libre_riesgo_anual) ** (1/252) - 1
rendimiento_promedio = datos.groupby('Ticker')['retorno_diario'].mean()
volatilidad = datos.groupby('Ticker')['retorno_diario'].std()
sharpe_ratio = ((rendimiento_promedio - tasa_libre_riesgo_diaria) / volatilidad).rename('Sharpe_Ratio')
datos['maximo_acumulado'] = datos.groupby('Ticker')['retorno_acumulado'].cummax()
datos['drawdown'] = (datos['retorno_acumulado'] - datos['maximo_acumulado']) / datos['maximo_acumulado']
maximo_drawdown_por_ticker = datos.groupby('Ticker')['drawdown'].min()
print(maximo_drawdown_por_ticker)
tabla_resumen = pd.DataFrame({
    'rendimiento_promedio' : rendimiento_promedio,
    'volatilidad' : volatilidad,
    'sharpe_ratio' : sharpe_ratio,
    'maximo_drawdown' : maximo_drawdown_por_ticker
})
tabla_resumen = tabla_resumen.reset_index()
tabla_resumen.to_csv('data/processed/tabla_resumen_metricas.csv', index=False)
datos.to_csv('data/processed/datos_completos.csv', index=False)
tabla_pivote = datos.pivot(index='Date', columns='Ticker', values='retorno_diario')
matriz_correlacion = tabla_pivote.corr()
matriz_correlacion.to_csv('data/processed/matriz_correlacion.csv')
matriz_correlacion = matriz_correlacion.reset_index()
matriz_larga = matriz_correlacion.melt(id_vars='Ticker', var_name='Ticker2', value_name='correlacion')
matriz_larga = matriz_larga.rename(columns={'Ticker': 'Ticker1'})
matriz_larga.to_csv('data/processed/matriz_larga.csv', index=False)
