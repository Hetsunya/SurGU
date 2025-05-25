import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Шаг 1: Загрузка и подготовка данных
data_path = 'AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")
data_clean = data.dropna(subset=['RH'])
time_series = data_clean['RH'][2500:3250].astype(float).copy()

# Шаг 2: Построение модели ARMA(p, q) и предсказания
p, q = 2, 2  # Указываем порядок модели ARMA(p, q)
model_arma = ARIMA(time_series, order=(p, 0, q))  # ARMA — это ARIMA без интеграции (d=0)
model_arma_fitted = model_arma.fit()

# Прогноз на 10 шагов вперед
forecast_arma = model_arma_fitted.forecast(steps=10)

# Построение графика
plt.figure(figsize=(14, 7))
plt.plot(time_series.index, time_series, label='Фактический временной ряд', color='blue')
forecast_idx = range(time_series.index[-1] + 1, time_series.index[-1] + 11)
plt.plot(forecast_idx, forecast_arma.values, label=f'Прогноз ARMA({p},{q})', color='red', linestyle='--')
plt.xlabel('Индекс')
plt.ylabel('Концентрация RH')
plt.title(f'Прогноз временного ряда с использованием модели ARMA({p},{q})')
plt.legend()
plt.show()

# # Шаг 3: Реализация модели ARMA(p, q) вручную
# # Устанавливаем коэффициенты модели (предполагаются заранее известными)
# phi = [0.6, -0.2]  # Коэффициенты AR
# theta = [0.3, 0.1]  # Коэффициенты MA
#
# # Генерация предсказаний вручную
# # Рассчитаем ошибки модели на тренировочных данных
# residuals = model_arma_fitted.resid[-q:]  # Берем последние q ошибок из обученной модели
#
# # Обновленная ручная реализация ARMA(p, q)
# manual_forecast_corrected = []
# errors = list(residuals)  # Инициализация ошибок последними остатками из модели
#
# for t in range(10):
#     # AR компонент
#     ar_component = sum(phi[i] * time_series.iloc[-(i + 1)] for i in range(len(phi)))
#     # MA компонент (учитываем реальные ошибки)
#     ma_component = sum(theta[i] * errors[-(i + 1)] for i in range(len(theta)))
#     # Итоговое значение
#     predicted_value = ar_component + ma_component
#     manual_forecast_corrected.append(predicted_value)
#     # Обновляем ошибки: добавляем текущую разницу (предсказание - последнее значение ряда)
#     errors.append(predicted_value - time_series.iloc[-1])
#
# # Построение графика обновленного прогноза
# plt.figure(figsize=(14, 7))
# plt.plot(time_series.index, time_series, label='Фактический временной ряд', color='blue')
# plt.plot(forecast_idx, manual_forecast_corrected, label=f'Обновленный ручной прогноз ARMA({p},{q})', color='purple', linestyle='--')
# plt.xlabel('Индекс')
# plt.ylabel('Концентрация RH')
# plt.title(f'Обновленный ручной прогноз временного ряда ARMA({p},{q})')
# plt.legend()
# plt.show()
