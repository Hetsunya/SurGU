import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima.model import ARIMA

# Загрузка данных
data = pd.read_csv('../AirQualityUCI.csv', sep=';', dtype={'Date': str, 'Time': str}, na_values=['NA', 'NaN'])

# Обработка даты и времени
data['DateTime'] = pd.to_datetime(data["Date"] + " " + data["Time"], format='%d/%m/%Y %H.%M.%S')

# Список столбцов с данными о качестве воздуха
columns = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'PT08.S2(NMHC)', 
           'C6H6(GT)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',
           'PT08.S5(O3)', 'T', 'RH', 'AH']

# Функция для обработки данных, проведения теста ADF и поиска стационарного ряда
def process_data_and_find_stationary(data, column):
    # Проверка типа данных и преобразование в строку при необходимости
    if data[column].dtype != 'object':
        data[column] = data[column].astype(str)

    # Замена запятых на точки и преобразование в тип float
    data[column] = data[column].str.replace(',', '.').astype(float)

    # Удаление строк с -200
    data = data[data[column] != -200]

    # Тест Дики-Фуллера
    result = adfuller(data[column].dropna())
    # print(f'--- {column} ---')
    # print('ADF статистика:', result[0])
    # print('p-value:', result[1])
    # print('Критические значения:', result[4])
    
    # Интерпретация результатов
    if result[1] < 0.05:
        print("=> Ряд стационарен (нулевая гипотеза отвергнута)")
        return data[column]  # Возвращаем стационарный ряд
    else:
        print("=> Ряд нестационарен (нулевая гипотеза не отвергнута)")
        # Попробуем сделать ряд стационарным с помощью первого дифференцирования
        data[column] = data[column].diff().dropna()
        return data[column]  # Возвращаем дифференцированный ряд

# Поиск стационарного ряда
stationary_series = None
for column in columns:
    print(column)
    series = process_data_and_find_stationary(data.copy(), column)
    if stationary_series is None:  # Проверяем, является ли Series пустым
        stationary_series = series
        stationary_column = column

# Вывод информации о стационарном ряде
print(f"\nНайден стационарный ряд: {stationary_column}")

# Определение лага с помощью PACF
# plot_pacf(stationary_series, lags=20)
# plt.xlabel('Лаг')
# plt.show()

# Выбор лага (например, lag = 2) на основе графика PACF

# Разделение данных на обучающую и тестовую выборки
train_data = stationary_series[:-30]
test_data = stationary_series[-30:]

# Модель AR(2)
model = ARIMA(train_data, order=(2, 1, 2))  # Изменили порядок на (2, 0, 0) для AR(2)
model_fit = model.fit()

# Прогнозирование
predictions = model_fit.predict(start=len(train_data), end=len(stationary_series)-1)

# Построение графика прогнозирования
# Построение графика прогнозирования на subplots
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))

# График исходного ряда
axes[0].plot(stationary_series, label='Original')
axes[0].set_title('Исходный ряд')
axes[0].set_xlabel('Дата и время')
axes[0].set_ylabel(stationary_column)
axes[0].grid(True)
axes[0].legend()

# График прогнозирования
axes[1].plot(predictions, color='red', label='Predictions')
axes[1].set_title('Прогнозирование AR(2)')
axes[1].set_xlabel('Дата и время')
axes[1].set_ylabel(stationary_column)
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()
