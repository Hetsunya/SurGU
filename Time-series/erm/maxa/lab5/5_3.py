import numpy as np
import time
import matplotlib.pyplot as plt

def fft_recursive(x):
    N = len(x) #  Получение размера входного массива
    if N <= 1: #  Базовый случай рекурсии: если массив состоит из одного элемента, возвращаем его же
        return x
    even = fft_recursive(x[0::2]) # FFT к чётным индексам массива
    odd = fft_recursive(x[1::2]) # FFT к нечётным индексам массива
    T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)] # Вычисление весовых коэффициентов для нечётных элементов
    # Объединение чётных и нечётных элементов с учетом весовых коэффициентов для получения окончательного результата FFT
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]

# Параметры функции
N = 1024
A_0 = 1.0  # Амплитуда
w_0 = 2 * np.pi  # Угловая частота
phi_0 = 0.5  # Начальная фаза

# Создаем массив значений x
x = np.linspace(0, 2 * np.pi, N)

# Функция f(x)
y = A_0 * np.sin(w_0 * x + phi_0)


start_time_recursive = time.time()
fft_result_recursive = fft_recursive(y)
time_recursive = time.time() - start_time_recursive
fft_numpy = np.fft.fft(y)
are_similar = np.allclose(fft_result_recursive, fft_numpy)
print("Результаты схожи:", are_similar)
print(time_recursive)



X_k = fft_recursive(y)
frequencies = np.arange(len(X_k))
half_len = N // 2
plt.figure(figsize=(10, 6))
plt.plot(frequencies[:half_len], np.abs(X_k[:half_len]) / np.max(np.abs(X_k)[:half_len]))
plt.title('Спектр сигнала после быстрого прямого преобразования Фурье')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()

X_k1 = np.fft.fft(y)
frequencies = np.arange(len(X_k1))
half_len = N // 2
plt.figure(figsize=(10, 6))
plt.plot(frequencies[:half_len], np.abs(X_k1[:half_len]) / np.max(np.abs(X_k1)[:half_len]))
plt.title('Спектр сигнала после быстрого прямого преобразования Фурье')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.show()
#  рекурсивный алгоритм, как описано в вашем примере, значительно уменьшает количество необходимых вычислений
# Это достигается за счет разделения исходного массива на меньшие части (четные и нечетные индексы), рекурсивного их преобразования и последующего комбинирования с использованием специфических весовых коэффициентов.
# Результаты для четных и нечетных элементов объединяются с учетом вычисленных весовых коэффициентов. Для первой половины результата к четным элементам прибавляются весовые коэффициенты, а для второй половины — вычитаются. Это дает окончательный результат БПФ.