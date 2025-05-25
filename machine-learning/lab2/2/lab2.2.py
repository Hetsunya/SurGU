import pandas as pd
import numpy as np
import timeit

# Чтение данных
df = pd.read_csv('city_temperature.csv', low_memory=False)

# Преобразование типов
int16_temperature = df['AvgTemperature'].astype(np.int16)
float64_temperature = df['AvgTemperature'].astype(np.float64)

# Тестирование int16
int16_time = timeit.timeit(lambda: np.sum(int16_temperature), number=100)
int16_result = np.sum(int16_temperature)
print(f"int16: время = {int16_time/100:.6f} сек, сумма = {int16_result}")

# Тестирование float64
float64_time = timeit.timeit(lambda: np.sum(float64_temperature), number=100)
float64_result = np.sum(float64_temperature)
print(f"float64: время = {float64_time/100:.6f} сек, сумма = {float64_result}")