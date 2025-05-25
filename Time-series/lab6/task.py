import numpy as np
from scipy.signal import iirnotch, lfilter
import matplotlib.pyplot as plt

# Параметры сигнала
fs = 1000  # Частота дискретизации (Гц)
f0 = 50   # Частота помехи (Гц)
Q = 30    # Фактор добротности

# Генерация тестового ЭКГ сигнала с помехой
t = np.linspace(0, 1, fs, endpoint=False)
ecg_signal = 0.5 * np.sin(2 * np.pi * 5 * t) + 0.1 * np.sin(2 * np.pi * f0 * t)

# Создание режекторного фильтра
b, a = iirnotch(f0, Q, fs)

# Применение фильтра к ЭКГ сигналу
filtered_ecg = lfilter(b, a, ecg_signal)

# Вычисление БПФ для исходного и отфильтрованного сигнала
fft_ecg = np.fft.fft(ecg_signal)
fft_filtered = np.fft.fft(filtered_ecg)
freqs = np.fft.fftfreq(len(ecg_signal), d=1/fs)

# Построение графиков
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, ecg_signal, label='Исходный ЭКГ сигнал')
plt.plot(t, filtered_ecg, label='Отфильтрованный ЭКГ сигнал')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.title('ЭКГ сигнал во временной области')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(freqs[:fs//2], np.abs(fft_ecg)[:fs//2], label='Исходный ЭКГ сигнал')
plt.plot(freqs[:fs//2], np.abs(fft_filtered)[:fs//2], label='Отфильтрованный ЭКГ сигнал')
plt.xlabel('Частота (Гц)')
plt.ylabel('Амплитуда')
plt.title('Амплитудно-частотная характеристика (АЧХ)')
plt.xlim(0, 100)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()