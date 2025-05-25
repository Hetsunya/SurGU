import pywt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.signal

# Загрузка данных
data = pywt.data.ecg()  # Пример данных ЭКГ

# Построение графика произвольной функции
plt.figure(figsize=(10, 5))
plt.plot(data)
plt.title('Произвольная функция из pywt.data')
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

# Построение скейлограммы
# Скейлограмма — это визуализация коэффициентов непрерывного вейвлет-преобразования (CWT), 
# где по оси абсцисс отложено время, по оси ординат — масштабы вейвлета, а цвет указывает на амплитуду (величину) 
# вейвлет-коэффициентов. Это помогает анализировать, какие частоты присутствуют в сигнале в разные моменты времени.
# Масштабы — это параметр, который определяет уровень детализации или разрешения анализа сигнала.
scales = np.arange(1, 128)
coeffs, freqs = pywt.cwt(data, scales=scales, wavelet='morl', sampling_period=1/256)
plt.figure(figsize=(10, 5))
plt.imshow(coeffs, extent=[0, len(data), 1, 128], cmap='PRGn', aspect='auto', vmax=abs(coeffs).max(), vmin=-abs(coeffs).max())
plt.title('Скейлограмма')
plt.xlabel('Время')
plt.ylabel('Масштаб')
plt.colorbar()
plt.show()

# Построение трехмерной поверхности двухпараметрического спектра
# Это трехмерная визуализация данных, где оси X и Y представляют время и масштабы соответственно, 
# а ось Z — амплитуду вейвлет-коэффициентов. Это позволяет визуализировать изменения амплитуды вейвлет-коэффициентов в 
# зависимости от времени и масштаба.
X, Y = np.meshgrid(np.arange(coeffs.shape[1]), scales)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, coeffs, cmap='viridis')
ax.set_xlabel('Время')
ax.set_ylabel('Масштаб')
ax.set_zlabel('Амплитуда')
ax.set_title('Трехмерная поверхность двухпараметрического спектра')
plt.show()

# Построение плоскости ab с цветовыми областями вейвлет-преобразования
# Это ещё один способ визуализации скейлограммы, где используется контурное отображение для выделения регионов 
# с различной величиной вейвлет-коэффициентов.
plt.figure(figsize=(10, 5))
plt.contourf(X, Y, coeffs, 20, cmap='RdGy')
plt.title('Плоскость ab с цветовыми областями')
plt.xlabel('Время')
plt.ylabel('Масштаб')
plt.colorbar()
plt.show()

# Построение сечений вейвлет-спектра
# Сечения вейвлет-спектра показывают вейвлет-коэффициенты на определенных масштабах. 
# Это дает представление о характеристиках сигнала на этих масштабах.
scales_to_plot = [5, 10, 20]  # Произвольные значения масштаба a
plt.figure(figsize=(10, 5))
for scale in scales_to_plot:
    plt.plot(coeffs[scale - 1], label=f'Масштаб {scale}')
plt.title('Сечения вейвлет-спектра W(a,b) по масштабам')
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)
plt.show()

# Построение скелетона - линии локальных экстремумов
# Скелетон показывает локальные максимумы вейвлет-преобразования, что может быть полезно для выявления особенностей
# и переходных эффектов в данных.
peaks = [scipy.signal.find_peaks(np.abs(coeffs[scale - 1]))[0] for scale in scales_to_plot]
plt.figure(figsize=(10, 5))
for idx, scale in enumerate(scales_to_plot):
    plt.plot(peaks[idx], coeffs[scale - 1][peaks[idx]], 'o', label=f'Экстремумы масштаба {scale}')
plt.title('Скелетон - линии локальных экстремумов')
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)
plt.show()
