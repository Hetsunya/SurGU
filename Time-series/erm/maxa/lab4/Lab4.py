import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

data_path = '../AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")
data_clean = data.dropna(subset=['CO(GT)'])
timeseries = data_clean['CO(GT)'][9280:9340].copy()

# Преобразуем данные, так как ARIMA работает с числами float
timeseries = timeseries.astype(float)

# Определение и обучение модели ARIMA
# Обычно необходимо выполнить анализ ACF и PACF, чтобы выбрать параметры p и q, но для упрощения примера мы возьмем p=2, d=1 и q=2
model = ARIMA(timeseries, order=(0, 0, 2))
model_fit = model.fit()

# Прогнозирование на 10 шагов вперед
forecast_steps = 10
forecast = model_fit.forecast(steps=forecast_steps)

# Визуализация результатов
plt.figure(figsize=(10, 5))
plt.plot(timeseries, label='Исходный ряд')
plt.plot(timeseries.index[-1] + np.arange(1, forecast_steps + 1), forecast, label='Прогноз ARIMA', linestyle='--')
plt.xlabel('Время')
plt.ylabel('Концентрация CO(GT)')
plt.title('Прогноз ARIMA для концентрации CO(GT)')
plt.legend()
plt.show()