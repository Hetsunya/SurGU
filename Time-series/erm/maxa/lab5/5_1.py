import numpy as np
import matplotlib.pyplot as plt
import time

# Параметры функции
N = 1024
A_0 = 1.0  # Амплитуда
w_0 = 2 * np.pi  # Угловая частота
phi_0 = 2  # Начальная фаза

# Создаем массив значений x
x = np.linspace(0, 2 * np.pi, N)

# Функция f(x)
y = A_0 * np.sin(w_0 * x + phi_0)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Исходный сигнал')
plt.title('График исходного сигнала')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

# Функция для прямого преобразования Фурье, вычисляет коэффициенты фурье сигнала
# Преобразует сигнал из временной области в частотную.
def dft(signal):
    N = len(signal) # Определение длины сигнала
    X = np.zeros(N, dtype=complex) # Массив для хранения результатов преобразования
    for k in range(N): # Перебирает каждую частоту спектра, для которой мы хотим вычислить амплитуду. k - индекс частоты
        for n in range(N): # Вычисляет сумму произведений каждого элемента исходного сигнала на соответствующий комплексный экспоненциальный множитель для текущей частоты. n - индекс временного сигнала
            X[k] += signal[n] * np.exp(-2j * np.pi * k * n / N) # Расчет коэффициентов преобразования. Это выражение используется для расчета комплексных амплитуд каждой частоты в спектре сигнала.
    return X

start = time.time()
X_k = dft(y)
result = time.time() - start
print("Время выполнения DFT:", result)

frequencies = np.arange(len(X_k))
half_len = N // 2
plt.figure(figsize=(10, 6))
plt.plot(frequencies[:half_len], np.abs(X_k[:half_len]/ np.max(np.abs(X_k)[:half_len])))
plt.title('Спектр сигнала после прямого преобразования Фурье')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

# Преобразует сигнал обратно из частотной области в временную
def idft(X_k):
    N = len(X_k) # Определение количества точек в спектре, N - длина входного частотного массива
    x_n = np.zeros(N, dtype=complex) # Инициализация массива для восстановленного временного сигнала, заполненного начальными значениями 0 + 0j
    for n in range(N): # Внешний цикл по каждой точке временного сигнала
        for k in range(N): # Внутренний цикл по каждой частоте в спектре
            # Добавление вклада текущей частоты k к временной точке n
            # Вклад определяется умножением амплитуды частоты на комплексную экспоненту с положительным показателем степени
            x_n[n] += X_k[k] * np.exp(2j * np.pi * k * n / N) 
    return x_n / N # Возвращение восстановленного сигнала с нормализацией, делением на N для коррекции амплитуды

y_reconstructed = idft(X_k)

plt.figure(figsize=(10, 6))
plt.plot(x, y_reconstructed.real, label='Восстановленный сигнал', linestyle='--')
plt.plot(x, y, label='Исходный сигнал', alpha=0.5)
plt.title('Сравнение исходного и восстановленного сигналов')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()

X_k_np = np.fft.fft(y)

plt.figure(figsize=(10, 6))
plt.plot(frequencies[:half_len], np.abs(X_k_np[:half_len]) / np.max(np.abs(X_k_np)[:half_len]))
plt.title('Спектр сигнала после прямого преобразования Фурье с NumPy')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

y_reconstructed_np = np.fft.ifft(X_k_np)

plt.figure(figsize=(10, 6))
plt.plot(x, y_reconstructed_np.real, label='Восстановленный с NumPy', linestyle='--')
plt.plot(x, y, label='Исходный сигнал', alpha=0.5)
plt.title('Сравнение исходного и восстановленного с NumPy сигналов')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()
