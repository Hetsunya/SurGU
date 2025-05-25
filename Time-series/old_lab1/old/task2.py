import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import kpss, adfuller

# Загрузка данных
data = pd.read_csv('../AirQualityUCI.csv', sep=';', dtype={'Date': str, 'Time': str}, na_values=['NA', 'NaN'])

# Обработка даты и времени
data['DateTime'] = pd.to_datetime(data["Date"] + " " + data["Time"], format='%d/%m/%Y %H.%M.%S')

# Список столбцов с данными о качестве воздуха
columns = ['CO(GT)', 'PT08.S1(CO)', 'NMHC(GT)', 'PT08.S2(NMHC)',            
           'C6H6(GT)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',           
           'PT08.S5(O3)', 'T', 'RH', 'AH']

# Функция для обработки данных и проведения тестов стационарности
def process_data_and_tests(data, column):
    # Проверка типа данных и преобразование в строку при необходимости
    if data[column].dtype != 'object':
        data[column] = data[column].astype(str)

    # Замена запятых на точки и преобразование в тип float
    data[column] = data[column].str.replace(',', '.').astype(float)

    # Удаление строк с -200
    data = data[data[column] != -200]

    # Тест Дики-Фуллера
    adf_result = adfuller(data[column].dropna())
    print(f'--- ADF ({column}) ---')
    print('ADF статистика:', adf_result[0])
    print('p-value:', adf_result[1])
    print('Критические значения:', adf_result[4])
    if adf_result[1] < 0.05:
        print("=> Ряд стационарен (нулевая гипотеза отвергнута)")
    else:
        print("=> Ряд нестационарен (нулевая гипотеза не отвергнута)")

    # Тест KPSS
    kpss_result = kpss(data[column].dropna())
    print(f'--- KPSS ({column}) ---')
    print('KPSS статистика:', kpss_result[0])
    print('p-value:', kpss_result[1])
    print('Критические значения:', kpss_result[3])
    if kpss_result[1] < 0.05:
        print("=> Ряд нестационарен (нулевая гипотеза отвергнута)")
    else:
        print("=> Ряд стационарен (нулевая гипотеза не отвергнута)")

    return data

# Обработка данных и тесты для каждого столбца
for column in columns:
    data = process_data_and_tests(data.copy(), column)

# Выборка данных для графика
data_sampled = data
# Извлечение данных для графика
date_v = data_sampled['DateTime']
co = data_sampled['CO(GT)']

# Построение графика
plt.figure(figsize=(20, 10))
plt.plot(date_v, co)
plt.title('Временной ряд CO(GT)')
plt.xlabel('Дата и время')
plt.ylabel('CO(GT)')
plt.grid(True)
plt.show()