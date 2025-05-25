import numpy as np
import pywt
import matplotlib.pyplot as plt

# Загрузка данных из файла
data = np.genfromtxt('lab5_data4.txt', delimiter=';', skip_header=1)

# Извлечение сигнала (предположим, что Канал0 - целевой сигнал)
signal = data[:, 1]

# Добавление белого гауссовского шума
mean = 0
variance = 0.01  # Настройте дисперсию по необходимости
noise = np.random.normal(mean, np.sqrt(variance), len(signal))
noisy_signal = signal + noise

# Функция для выполнения и отображения DWT и IDWT
def perform_wavelet_transform(wavelet_name):
    # Выполнение дискретного вейвлет-преобразования (DWT)
    coeffs = pywt.wavedec(noisy_signal, wavelet_name)
    
    # Построение графиков коэффициентов вейвлета по шагам
    plt.figure(figsize=(12, 8))
    for i, coeff in enumerate(coeffs):
        plt.subplot(len(coeffs), 1, i+1)
        plt.plot(coeff)
        plt.title(f'Коэффициенты уровня {i} - Вейвлет {wavelet_name}')
    plt.tight_layout()
    plt.show()

    # Выполнение обратного дискретного вейвлет-преобразования (IDWT)
    reconstructed_signal = pywt.waverec(coeffs, wavelet_name)

    # Вычисление среднеквадратичной ошибки (MSE)
    mse = np.mean((signal - reconstructed_signal) ** 2)
    print(f'Среднеквадратичная ошибка (MSE) с вейвлетом {wavelet_name}: {mse}')

    # Построение графиков исходного, зашумленного и восстановленного сигналов
    plt.figure(figsize=(14, 6))
    plt.plot(signal, label='Исходный сигнал')
    plt.plot(noisy_signal, label='Зашумленный сигнал', linestyle='dashed')
    plt.plot(reconstructed_signal, label='Восстановленный сигнал', linestyle='dotted')
    plt.legend()
    plt.title(f'Сравнение сигналов - Вейвлет {wavelet_name}')
    plt.show()

# Выполнение для вейвлета Морле
perform_wavelet_transform('morl')

# Выполнение для другого вейвлета (например, Хаара)
perform_wavelet_transform('haar')
