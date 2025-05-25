import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные
data_path = 'lab3_data4.txt'
data = pd.read_csv(data_path, header=None, delimiter='\t')

# Присваиваем имена столбцам для удобства
data.columns = ['Тишина', 'Агрессивная', 'Белый шум', 'Классическая', 'Ритмичная']

# Преобразуем данные во временные ряды, где значение интервала - это время между ударами сердца
time_series = {col: data[col].cumsum() for col in data.columns}

# Создаем фигуру для графиков
plt.figure(figsize=(15, 10))

# Для каждого вида музыки рисуем отдельный график временного ряда
for i, (name, series) in enumerate(time_series.items()):
    plt.subplot(len(time_series), 1, i + 1)
    plt.vlines(series[10:50], 0, 1, label=name)
    plt.title(name)
    plt.ylim(0, 1.5)
    plt.legend()

plt.tight_layout()
plt.show()
