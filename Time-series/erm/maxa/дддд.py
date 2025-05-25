import pandas as pd
import numpy as np
from scipy.signal import iirnotch, filtfilt, freqz
import matplotlib.pyplot as plt

# Функция для загрузки данных из файла
def load_data(file_path):
    return pd.read_csv(file_path, delimiter=';', encoding='cp1251')

# Функция для создания и применения режекторного фильтра
def notch_filter(data, notch_freq, fs, Q):
    w0 = notch_freq / (fs / 2)  # Нормализованная частота
    b, a = iirnotch(w0, Q)  # Создание коэффициентов фильтра
    y = filtfilt(b, a, data)  # Применение фильтра к данным
    return y

# Загрузка данных из файла
file_path = 'lab5/lab5_data4.txt'  # Путь к вашему файлу
data = load_data(file_path)

# Частота дискретизации
fs = 1.0  # Предполагаемая частота дискретизации в Гц

# Параметры фильтра на основе спектра (подавление частоты 0.01 Гц)
notch_freq = 0.2  # Частота подавления в Гц
Q = 1.0  # Попробуем уменьшить качество фильтра для более широкой полосы подавления

# Применение фильтра к каналу 0
data['filtered_channel0'] = notch_filter(data['Канал0'], notch_freq, fs, Q)

# Применение фильтра к каналу 1
data['filtered_channel1'] = notch_filter(data['Канал1'], notch_freq, fs, Q)

# Построение графиков сигналов до и после фильтрации
plt.figure(figsize=(12, 6))

# График для Канал0
plt.subplot(2, 1, 1)
plt.plot(data['отсчеты'], data['Канал0'], label='Исходный Канал 0')
plt.plot(data['отсчеты'], data['filtered_channel0'], label='Отфильтрованный Канал 0', linestyle='--')
plt.title('Канал 0 до и после применения режекторного фильтра')
plt.xlabel('Номер отсчета')
plt.ylabel('Сигнал')
plt.legend()

# График для Канал1
plt.subplot(2, 1, 2)
plt.plot(data['отсчеты'], data['Канал1'], label='Исходный Канал 1')
plt.plot(data['отсчеты'], data['filtered_channel1'], label='Отфильтрованный Канал 1', linestyle='--')
plt.title('Канал 1 до и после применения режекторного фильтра')
plt.xlabel('Номер отсчета')
plt.ylabel('Сигнал')
plt.legend()

plt.tight_layout()  # Автоматическая настройка расстояний между графиками
plt.show()

# # Построение амплитудно-частотной характеристики (АЧХ) фильтра
# b, a = iirnotch(notch_freq / (fs / 2), Q)
# w, h = freqz(b, a, fs=fs)

# # Определение полосы подавления
# w1 = notch_freq - (notch_freq / Q)
# w2 = notch_freq + (notch_freq / Q)

# plt.figure(figsize=(10, 6))
# plt.plot(w, 20 * np.log10(abs(h)), label=f'Notch filter (f = {notch_freq} Hz, Q = {Q})')
# plt.title('Амплитудно-частотная характеристика (АЧХ) режекторного фильтра')
# plt.xlabel('Частота (Гц)')
# plt.ylabel('Амплитуда (дБ)')
# plt.axvline(notch_freq, color='r', linestyle='--', label='Центральная частота подавления')
# plt.axvline(w1, color='g', linestyle='--', label='ω1')
# plt.axvline(w2, color='b', linestyle='--', label='ω2')
# plt.legend()
# plt.grid()
# plt.show()
