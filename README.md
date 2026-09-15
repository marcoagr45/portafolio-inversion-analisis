# Análisis de Rentabilidad de un Portafolio de Inversión (Acciones + Criptomonedas)
## Descripción del Proyecto
Se completó la descarga de datos (tickers) a través de Yahoo Finance via yfinance, utilizando un rango de fechas de 5 años, tomados desde septiembre 2021 a septiembre 2026.
Se realizó limpieza y alineación de fechas entre acciones (5 días/semana) y criptomonedas (7 días/semana) utilizando forwardfill (ffill) para completar los días sin cotización bursátil.
Se creó un archivo para almacenar el resultado: data/processed/precios_limpios.csv. 
Se realizó el cálculo de retornos diarios y acumulados por ticker (usando groupby()) para evitar mezclar datos entre activos.
Se calculó la volatilidad (usando desviación estándar de retornos diarios) como medida de riesgo.
Se calculó el sharpe-ratio tomando en consideración el rendimiento promedio de cada ticker, sustrayendo la tasa libre de riesgo (calculada por medio de los 'T-Bill') y dividiéndola sobre la volatilidad del ticker.
Se calculó el máximo drawdown (máxima caída desde un pico/punto histórico) tomando en consideración el máximo acumulado de retornos y los máximos históricos de cada ticker.
Se consolidaron las 4 métricas de riesgo/rendimiento en una tabla resumen por ticker, exportada a data/processed/tabla_resumen_metricas.csv, para su uso en la etapa de visualización en conjunto con la tabla de precios_limpios.csv.
Se creó una matriz de correlación utilizando los ticker como índices y el retorno diario como valor a examinar.
Se calculó la matriz de correlación entre los 9 tickers utilizando los retornos diarios, para lo que se usó el método .pivot(), una vez creada la tabla de pivote se usó el método .corr() de pandas. Siendo que la matriz de correlación nos serviría para visualización en Tableau, se transformó de formato ancho (creado por defecto) a formato laro utilizando .melt() y exportando la tabla matriz_correlacion_larga.csv.
Se conectaron las 4 fuentes de datos (precios_limpios, tabla_resumen_metricas, datos_completos(retornos/drawdown) y matriz de correlación) en Tableau Public, donde se construyeron 4 visualizaciones: comparación de Sharpe Ratio entre tickers, panel de riesgo (dispersión volatilidad vs rendimiento), evolución del retorno acumulado en el tiempo, y un mapa de calor de correlación entre pares de tickers.
## Pregunta de negocio
¿Cómo se habría comportado un portafolio diversificado entre acciones y criptomonedas frente a uno tradicional en los últimos 5 años, y qué combinación habría ofrecido la mejor relación rentabilidad-riesgo?
¿Qué patrones históricos son útiles a considerar al construir un portafolio propio?
## Estructura del proyecto
```
data/
├── raw/
│   └── precios_combinados.csv
└── processed/
    ├── precios_limpios.csv
    ├── tabla_resumen_metricas.csv
    ├── datos_completos.csv
    ├── matriz_correlacion.csv
    └── matriz_correlacion_larga.csv
scripts/
├── download_data.py
├── clean_data.py
└── analysis.py
tableau/
venv/
```
## Herramientas utilizadas
- Python
- SQL
- Tableau 
## Notas sobre herramientas de visualización
Elegí Tableau en esta etapa porque para usar Power BI requiero una máquina virtual con Windows en Apple Silicon, y no es el momento de justificar el costo de una suscripción de Parallels Desktop sin tener aún un ingreso de esta área.
## Dashboard en Tableau Public
El dashboard muestra los principales indicadores generados en Python: sharpe-ratio, rendimiento promedio, volatilidad, retorno acumulado, evolución en el tiempo y matriz de correlación entre tickers. 

Link al dashboard:https://public.tableau.com/app/profile/marco.g.emez/viz/Portafolio_Inversion_Analisis/Dashboard?publish=yes 

Se generaron 4 visualizaciones: 
- Gráfico de barras:  ranking de tickers utilizando el sharpe-ratio como medida
- Una gráfica de dispersión comparando la volatilidad vs el rendimiento promedio de cada ticker
- Gráfico de líneas que muestre el retorno acumulado hasta la fecha
- Mapa de calor de correlación entre tickers.

Para la Matriz de Correlación se decidió mantener la paleta secuencia en azul, debido a que usar un color divergente podría indicar que alguna es negativa, cuando no fue el caso.
Se optó por ajustar la anchura del heatmap para liberar más espacio en el dashboard final.
Se verificó la asignación de colores automáticos para tickers, encontrando el código hex #FF9933 para BTC-USD.
Se decidió publicar sin filtros activos, sin embargo existen acciones de filtros (clic en una barra filtra las demás vistas).
## Hallazgos principales
- SOL-USD registra la mayor volatilidad diaria (4.9%), casi 5 veces superior a la de KO (0.87%), la acción más estable del grupo.
- SPY y KO muestran la menor volatilidad con 0.89 % y 0.87 % respectivamente.
- JPM registró el mayor Sharpe Ratio (0.0345) seguido por KO (0.0247), casi empatado con AAPL (0.0243) y dejando en últimos lugares con los menores Sharpe Ratio a SOL-USD (0.0160) y ETH-USD (0.009)
- SPY (S&P 500) registró un Sharpe Ratio de 0.0239 a pesar de ser un ETF consolidado de las 500 empresas más grandes de EEUU. Esta tasa es muy cercana a las demás acciones a excepción de JPM lo cual podría explicarse por el periodo evaluado (2021-2026) donde han habido ciclos de tasas de interés altas, esto explicaría por qué JPM (un banco) presentó esta variación mayor de desempeño frente al resto de acciones.
- Se calculó el máximo drawdown (peor caída porcentual desde un pico) por ticker utilizando .cummax() para calcular el máximo acumulado y comparándolo contra el retorno acumulado real. 
- SOL-USD registró el peor drawdown (-96.3%), seguido de ETH-USD (-79.4%) y BTC-USD (-76.6%), lo cual es consistente con la mayor volatilidad ya documentada.
- KO registró el mejor drawdown (-17.3%) lo cual refuerza el patrón observado en volatilidad y Sharpe Ratio: haciendo KO la acción más defensiva y estable del grupo evaluado.
- Las tres métricas de riesgo nos muestran un patrón consistente en la misma dirección: las criptomonedas concentran el mayor riesgo, mientras que las acciones defensivas como KO ofrecen la mayor estabilidad.
- BTC-USD y ETH-USD presentan una correlación muy alta entre ellas (0.840556), esto puede explicarse debido a que gran parte del mercado cripto se mueve en conjunto.
- JNJ presenta correlaciones bajas con prácticamente todos los demás tickers (0.005 a 0.45), lo cual la hace la mejor candidata para diversificación real dentro de este portafolio.
- QQQ y SPY, ambos ETFs de mercado amplio, muestran una correlación de 0.95, lo cual indica que combinarlos en un portafolio aporta poca diversificación entre sí.
