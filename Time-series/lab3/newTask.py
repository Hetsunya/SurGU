import pandas as pd
import matplotlib.pyplot as plt

data_path = 'lab3_data6.txt'
data = pd.read_csv(data_path, header=None, delimiter='\t')

data.columns = ['Тишина', 'Агрессивная', 'Белый шум', 'Классическая', 'Ритмичная']

# print(data.shape)

# print(data)

# Преобразуем данные во временные ряды, перевод мс в с
time_series = {col: data[col].cumsum() / 1000 for col in data.columns}

# print(time_series)

def calculate_avg_bpm(series):
    total_time = series.iloc[-1]
    print(total_time, len(series))
    num_beats = len(series)
    avg_bpm = (num_beats / total_time) * 60
    return avg_bpm


def calculate_bpm(series):
    intervals = series.diff().dropna()
    bpm = 60 / intervals
    return bpm

plt.figure(figsize=(15, 10))

for i, (name, series) in enumerate(time_series.items()):

    plt.subplot(len(time_series), 1, i + 1)
    data = series.dropna()

    print(calculate_avg_bpm(series.dropna()))
    bpm = calculate_bpm(data)

    plt.vlines(data, 0, 1, label=name)
    avg_bpm = bpm.mean()
    plt.title(f"{name}, Avg ЧСС: {avg_bpm:.1f}")
    plt.ylim(0, 1.2)
    plt.legend()


plt.tight_layout()
plt.show()
