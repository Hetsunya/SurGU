import numpy as np
import matplotlib.pyplot as plt
import pywt

# Загрузка данных для двух каналов
with open('lab5_data4.txt', 'r') as file:
    data = np.loadtxt(file, delimiter=';', skiprows=1, usecols=(1, 2))

# Добавление белого гауссовского шума к каждому каналу
np.random.seed(0)
noise = np.random.normal(loc=0, scale=0.05, size=data.shape)
noisy_data = data + noise

# Визуализация сигналов до и после добавления шума
channels = ['Канал 1', 'Канал 2']
for i in range(2):
    plt.figure(figsize=(10, 5))
    plt.plot(data[:, i], label=f'Исходный {channels[i]}')
    plt.plot(noisy_data[:, i], label=f'Зашумленный {channels[i]}', linestyle='--')
    plt.legend()
    plt.title(f'Сигнал до и после добавления шума - {channels[i]}')
    plt.show()

    # Вейвлет-преобразование с использованием вейвлета 
    
    wavelet = 'sym5'
    coeffs = pywt.wavedec(noisy_data[:, i], wavelet, level=4)

    # Визуализация коэффициентов
    plt.figure(figsize=(10, 5))
    for level, coef in enumerate(coeffs, 1):
        plt.plot(coef, label=f'Уровень {level}')
    plt.legend()
    plt.title(f'Вейвлет-коэффициенты - {channels[i]}')
    plt.show()

    # Обратное вейвлет-преобразование
    reconstructed_signal = pywt.waverec(coeffs, wavelet)

    # Убедимся, что размеры сигналов совпадают
    if len(data[:, i]) != len(reconstructed_signal):
        reconstructed_signal = np.append(reconstructed_signal, [reconstructed_signal[-1]] * (len(data[:, i]) - len(reconstructed_signal)))

    # Визуализация сравнения исходного сигнала с восстановленным
    plt.figure(figsize=(10, 5))
    plt.plot(data[:, i], label=f'Исходный {channels[i]}')
    plt.plot(reconstructed_signal, label=f'Восстановленный {channels[i]}', linestyle='--')
    plt.legend()
    plt.title(f'Сравнение исходного и восстановленного сигнала - {channels[i]}')
    plt.show()

    # Вычисление MSE между исходным и восстановленным сигналом
    mse = np.mean((data[:, i] - reconstructed_signal)**2)
    print(f'MSE для {channels[i]}: {mse:.6f}')
