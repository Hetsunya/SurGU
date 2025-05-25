import pywt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.signal import argrelextrema

# Загрузка тестовых данных
data = pywt.data.ecg()

# Функция для построения графика сигнала
def plot_signal(signal, title):
    plt.figure(figsize=(10, 5))
    plt.plot(signal)
    plt.title(title)
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.show()

# Функция для построения скейлограммы
def plot_scalogram(wavelet, scales, cfs, frequencies):
    power = (np.abs(cfs)) ** 2
    plt.figure(figsize=(12, 7))
    plt.imshow(power, origin='lower', cmap='viridis',
               extent=[-1 + 1 / len(data), len(data) - 1 / len(data), 1, 128],
               aspect='auto')
    plt.title('Скейлограмма')
    plt.xlabel('Время')
    plt.ylabel('Масштаб')
    plt.show()

# Функция для построения трёхмерной поверхности спектра
def plot_3d_surface(X, Y, power):
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, power, rstride=1, cstride=1, cmap='coolwarm',
                           linewidth=0, antialiased=False)
    ax.set_xlabel('Время')
    ax.set_ylabel('Масштаб')
    ax.set_zlabel('Энергия')
    plt.title('Трехмерная поверхность спектра')
    plt.show()

# Функция для построения цветовой карты вейвлет-преобразования
def plot_color_map(X, Y, power):
    plt.figure(figsize=(12, 7))
    plt.pcolormesh(X, Y, power, shading='auto', cmap='viridis')
    plt.colorbar(label='Энергия')
    plt.title('Цветовая карта вейвлет-преобразования')
    plt.xlabel('Время')
    plt.ylabel('Масштаб')
    plt.show()

# Функция для построения сечений вейвлет-спектра
def plot_sections(selected_scales, data, cfs, scales):
    for scale in selected_scales:
        index = np.where(scales == scale)[0][0]
        plt.figure(figsize=(10, 5))
        plt.plot(data, label='Исходный сигнал')
        plt.plot(np.real(cfs[index]), label=f'Вейвлет-сечение при a={scale}')
        plt.legend()
        plt.title(f'Сечение вейвлет-спектра при a={scale}')
        plt.xlabel('Время')
        plt.ylabel('Амплитуда')
        plt.show()

# Функция для построения скелетона
def plot_skeleton(X, Y, power):
    extrema_indices = argrelextrema(power, np.greater, axis=0)
    x_extrema = X[extrema_indices]
    y_extrema = Y[extrema_indices]
    z_extrema = power[extrema_indices]

    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_extrema, y_extrema, z_extrema, color='r', marker='o')
    ax.plot_wireframe(X, Y, power, color='gray')
    ax.set_xlabel('Время')
    ax.set_ylabel('Масштаб')
    ax.set_zlabel('Энергия')
    plt.title('Линии локальных экстремумов (скелетон)')
    plt.show()

# Функция для добавления шума
def add_noise(signal, noise_level):
    noisy_data = signal + noise_level * np.random.randn(len(signal))
    return noisy_data

# Функция для прямого ДВП
def compute_dwt(signal, wavelet, level):
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    plt.figure(figsize=(15, 20))
    for i, coeff in enumerate(coeffs):
        plt.subplot(len(coeffs), 1, i+1)
        plt.plot(coeff, '-')
        plt.title(f'Уровень {i}')
    plt.tight_layout()
    plt.show()
    return coeffs

# Функция для обратного ДВП
def reconstruct_signal(coeffs, wavelet):
    rec_signal = pywt.waverec(coeffs, wavelet)
    return rec_signal

# Функция для сравнения сигналов
def compare_signals(original_signal, reconstructed_signal):
    mse = np.mean((original_signal - reconstructed_signal)**2)
    print(f'MSE: {mse:.4f}')

# Основная функция
def main():
    # Задание 1
    plot_signal(data, 'Тестовый сигнал')

    wavelet = 'shan1.5-1.0'  # Используем вейвлет Shannon с параметрами B=1.5 и C=1.0
    scales = np.arange(1, 128)
    [cfs, frequencies] = pywt.cwt(data, scales, wavelet)

    plot_scalogram(wavelet, scales, cfs, frequencies)

    X, Y = np.mesh