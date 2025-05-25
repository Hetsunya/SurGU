import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Загрузка данных
data = pd.read_csv('../AirQualityUCI.csv', sep=';', dtype={'Date': str, 'Time': str}, na_values=['NA', 'NaN'])

# Обработка даты и времени
data['DateTime'] = pd.to_datetime(data["Date"] + " " + data["Time"], format='%d/%m/%Y %H.%M.%S')

# Список столбцов с данными о качестве воздуха
columns = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'PT08.S2(NMHC)', 
           'C6H6(GT)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',
           'PT08.S5(O3)', 'T', 'RH', 'AH']

# Функция для обработки данных и проведения теста ADF
def process_data_and_adf_test(data, column):
    # Проверка типа данных и преобразование в строку при необходимости
    if data[column].dtype != 'object':
        data[column] = data[column].astype(str)

    # Замена запятых на точки и преобразование в тип float
    data[column] = data[column].str.replace(',', '.').astype(float)

    # Удаление строк с -200
    data = data[data[column] != -200]

    # Тест Дики-Фуллера
    result = adfuller(data[column].dropna())
    print(f'--- {column} ---')
    print('ADF статистика:', result[0])
    print('p-value:', result[1])
    print('Критические значения:', result[4])
    
    # Интерпретация результатов
    if result[1] < 0.05:
        print("=> Ряд стационарен (нулевая гипотеза отвергнута)")
    else:
        print("=> Ряд нестационарен (нулевая гипотеза не отвергнута)")
    
    return data

# Обработка данных и ADF тест для каждого столбца
for column in columns:
    data = process_data_and_adf_test(data.copy(), column)

# Выборка данных для CO(GT)
data_co = data[['DateTime', 'CO(GT)']].set_index('DateTime')

# Апроксимация скользящим средним с разными окнами
data_co['MA3'] = data_co['CO(GT)'].rolling(window=3).mean()
data_co['MA5'] = data_co['CO(GT)'].rolling(window=5).mean()
data_co['MA10'] = data_co['CO(GT)'].rolling(window=10).mean()
data_co['MA50'] = data_co['CO(GT)'].rolling(window=50).mean()

# Построение графиков апроксимации на отдельных subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12)) 


# График MA3
axes[0, 0].plot(data_co['MA3'], label='MA3')
axes[0, 0].set_title('MA3')

# График MA5
axes[0, 1].plot(data_co['MA5'], label='MA5')
axes[0, 1].set_title('MA5')

# График MA10
axes[1, 0].plot(data_co['MA10'], label='MA10')
axes[1, 0].set_title('MA10')

# График MA10
# График MA50
axes[1, 1].plot(data_co['MA50'], label='MA50')
axes[1, 1].set_title('MA50')


# Общие настройки для всех графиков
for ax in axes.flat:
    ax.set_xlabel('Дата и время')
    ax.set_ylabel('CO(GT)')
    ax.grid(True)
    ax.legend()

# Настройка расположения графиков
plt.tight_layout()

# Построение графика исходного отдельно
plt.figure(figsize=(12, 6))
plt.plot(data_co['CO(GT)'], label='Исходный ряд')
plt.title('Исходный ряд')
plt.xlabel('Дата и время')
plt.ylabel('CO(GT)')
plt.grid(True)
plt.legend()

plt.show()

# Разделение данных на обучающую и тестовую выборки
train_data = data_co[:-30]
test_data = data_co[-30:]

# Модель MA(1)  
model = ARIMA(train_data['CO(GT)'], order=(0, 0, 1))
model_fit = model.fit()

# Прогнозирование
predictions = model_fit.predict(start=len(train_data), end=len(data_co)-1)

# Построение графика прогнозирования
plt.figure(figsize=(12, 6))
plt.plot(data_co['CO(GT)'], label='Original')
plt.plot(predictions, color='red', label='Predictions')
plt.title('Прогнозирование MA(1)')
plt.xlabel('Дата и время')
plt.ylabel('CO(GT)')
plt.legend()
plt.grid(True)
plt.show()