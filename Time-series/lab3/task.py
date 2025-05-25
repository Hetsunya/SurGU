import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('lab3_data6.txt', sep='\t', header=None, names=['Nothing', 'Aggressive', 'White Noise', 'Classical', 'Rhythmic'])

time_series = []

# Для каждой колонки (типа музыки):
for col in data.columns:
    # Преобразуем интервалы между ударами в частоту сердечных сокращений (ударов в минуту)
    heart_rate = 60000 / data[col]
    # Создаем временной ряд с равномерным шагом времени
    time = pd.Series(np.arange(len(heart_rate)), index=pd.date_range(start='2023-11-01', periods=len(heart_rate), freq='ms'))
    time_series.append(pd.Series(heart_rate, index=time))

# Построение графиков для каждого типа музыки
plt.figure(figsize=(12, 8))
for i, ts in enumerate(time_series):
    plt.subplot(len(time_series), 1, i+1)
    plt.plot(ts, label=data.columns[i])
    plt.xlabel('Время')
    plt.ylabel('ЧСС')
    plt.title(f'Сердечный ритм при прослушивании {data.columns[i]}')
    plt.legend()

    # Calculate and print statistics for each time series
    print(f'Statistics for {data.columns[i]}:')
    print(ts.describe())

plt.tight_layout()
plt.show()
