import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, lfilter

# Параметры сигнала
fs = 1000  # Частота дискретизации (Гц)
t = np.linspace(0, 1, fs, endpoint=False)  # 1 секунда временного ряда

# Создаем сигнал: полезная синусоида 10 Гц + шум 50 Гц
signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)

# Параметры фильтра
f0 = 50  # Частота шума, которую нужно подавить (Гц)
Q = 30   # Добротность фильтра
b, a = iirnotch(f0 / (fs / 2), Q)  # Расчет коэффициентов фильтра

# Применяем фильтр
filtered_signal = lfilter(b, a, signal)

# Визуализация
plt.figure(figsize=(12, 6))

# Сигнал до фильтрации
plt.subplot(2, 1, 1)
plt.plot(t, signal, label="Оригинальный сигнал")
plt.title("Сигнал до фильтрации")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()

# Сигнал после фильтрации
plt.subplot(2, 1, 2)
plt.plot(t, filtered_signal, label="Фильтрованный сигнал", color="orange")
plt.title("Сигнал после применения режекторного фильтра")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
