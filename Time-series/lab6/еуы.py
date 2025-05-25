import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, freqz

# Параметры фильтра
fs = 200  # Частота дискретизации, Гц
f0 = 50    # Центральная частота (Гц)
Q = 30     # Добротность

# Расчет коэффициентов фильтра
b, a = iirnotch(f0 / (fs / 2), Q)

# АЧХ фильтра
w, h = freqz(b, a, worN=800)
freq = w * fs / (2 * np.pi)  # Преобразуем ось частоты в Гц

# График АЧХ
plt.figure(figsize=(8, 4))
plt.plot(freq, 20 * np.log10(abs(h)), label="АЧХ")
plt.title("Амплитудно-частотная характеристика (АЧХ)")
plt.xlabel("Частота (Гц)")
plt.ylabel("Амплитуда (дБ)")
plt.axvline(f0, color='r', linestyle='--', label=f"f0 = {f0} Гц")
plt.grid()
plt.legend()
plt.show()
