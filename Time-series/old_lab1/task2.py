import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.ar_model import AutoReg

data_path = 'AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")

# Шаг 2: Проверка на стационарность
# Удаление строк с отсутствующими значениями для выбранного ряда
data_clean = data.dropna(subset=['RH'])

# Преобразование во временной ряд
time_series = data_clean['RH'][2500:3250].copy()
plt.plot(time_series)
plt.show()

# Проведение теста Дики-Фуллера на стационарность
result = adfuller(time_series, autolag='AIC')
print(result)
# Шаг 3: Определение лага авторегрессии
# Построение графика PACF
fig, ax = plt.subplots(figsize=(10, 6))
plot_pacf(time_series, ax=ax, lags=30, method='ywm')
plt.show()

# Шаг 4: Построение модели AR
# Определение количества лагов на основе графика PACF
lags = 2 # Примерное количество значимых лагов, видимых на графике

# Создание и обучение модели AR
model = AutoReg(time_series, lags=lags)
model_fitted = model.fit()
print(model_fitted.summary())
# Шаг 5: Прогнозирование
# Создание прогноза на 10 шагов вперед
forecast_steps = 10
forecast_end_idx = len(time_series) + forecast_steps - 1  # Индекс последнего прогнозируемого значения
forecast_index = range(len(time_series), len(time_series) + forecast_steps)  # Генерация новых индексов для прогноза

forecast = model_fitted.predict(start=len(time_series), end=forecast_end_idx, dynamic=True)
forecast.index = forecast_index  # Присвоение новых индексов прогнозу


# Визуализация фактических данных и прогноза
plt.figure(figsize=(14, 7))
plt.plot(range(len(time_series)), time_series.values, label='Фактические данные', color='blue')
plt.plot(forecast.index, forecast.values, label='Прогноз', color='red', linestyle='--')
plt.xlabel('Индекс времени')
plt.ylabel('Концентрация RH')
plt.title('Прогноз концентрации RH с использованием модели авторегрессии')
plt.legend()
plt.show()

