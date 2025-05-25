import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка и очистка данных
data_path = '../AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")
data['RH'] = pd.to_numeric(data['RH'], errors='coerce')  # Преобразуем RH в числовой формат
data_clean = data.dropna(subset=['RH'])

# Выбор временного ряда
timeseries = data_clean['RH'][2500:3250].copy()

# Функция для вычисления скользящего среднего
def moving_average_forecast(series, order):
    forecast = np.full(series.shape, np.nan)  # Инициализация массива прогнозов NaN-значениями
    for end in range(order, len(series)):
        forecast[end] = series[end-order:end].mean()  # Вычисление среднего последних 'order' наблюдений
    return forecast

# Функция для предсказания следующего значения на основе последних 'order' наблюдений в серии
def predict_next_value(series, order):
    return series[-order:].mean()

# Выбор порядка модели MA
q_order = 50

# Применение функции скользящего среднего
ma_forecast = moving_average_forecast(timeseries, q_order)

# Предсказание следующего значения
next_value = predict_next_value(timeseries, q_order)

# Предсказание 10 следующих значений
future_values = []
current_series = timeseries.copy()
for _ in range(10):
    next_val = predict_next_value(current_series, q_order)
    future_values.append(next_val)
    current_series = pd.concat([current_series, pd.Series([next_val])], ignore_index=True)

# Вывод последних значений ряда и 10 предсказанных значений
print("Последние значения ряда:")
print(timeseries)
future_df = pd.DataFrame(future_values, columns=['Предсказанные:'])
print(future_df)

last_known_index = timeseries.index[-1]
forecast_index = np.arange(last_known_index + 1, last_known_index + 11)
forecast_series = pd.Series(future_values, index=forecast_index)

# Объединение исходного временного ряда с предсказанными значениями
combined_series = pd.concat([timeseries, forecast_series])

# Отрисовка графика с фактическими данными и прогнозом
plt.figure(figsize=(14, 7))
plt.plot(combined_series.index, combined_series, label='Фактические данные', color='blue')
plt.plot(forecast_series.index, forecast_series, label='Прогноз', color='red', linestyle='--')
plt.xlabel('Индекс')
plt.ylabel('Концентрация RH')
plt.title('Прогноз концентрации RH с использованием модели скользящего среднего MA(5)')
plt.legend()
plt.show()