import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import iirnotch

def load_data(file_path, delimiter=';', skip_header=1):
    """
    Загрузка данных из файла.

    Parameters:
    file_path (str): Путь к файлу.
    delimiter (str, optional): Разделитель данных в файле. По умолчанию ';'.
    skip_header (int, optional): Количество строк заголовка для пропуска. По умолчанию 1.

    Returns:
    ndarray: Загруженные данные.
    """
    return np.genfromtxt('lab5_data6.txt', delimiter=';', skip_header=1, encoding='cp1251')


def scale_signal(signal):
    """
    Масштабирование сигнала так, чтобы его среднее значение было 0.

    Parameters:
    signal (ndarray): Входной сигнал.

    Returns:
    ndarray: Масштабированный сигнал.
    """
    signal_mean = np.mean(signal)
    return signal - signal_mean

def calculate_filter_coeffs(f0, Q, fs):
    """
    Расчет коэффициентов фильтра.

    Parameters:
    f0 (float): Частота, которую необходимо подавить (в Гц).
    Q (float): Добротность фильтра.
    fs (float): Частота дискретизации (в Гц).

    Returns:
    ndarray, ndarray: Коэффициенты числителя и знаменателя фильтра.
    """
    w0 = f0 / (fs / 2)
    # b, a = iirnotch(w0, Q)
    b, a = iirnotch(f0 / (fs / 2), Q)

    return b, a

def filter_signal(signal, b, a):
    """
    Фильтрация сигнала.

    Parameters:
    signal (ndarray): Входной сигнал.
    b (ndarray): Коэффициенты числителя фильтра.
    a (ndarray): Коэффициенты знаменателя фильтра.

    Returns:
    ndarray: Отфильтрованный сигнал.
    """

    return np.convolve(signal, b / a)

def plot_signals(signal, filtered_signal):
    """
    Визуализация сигнала до и после фильтрации.

    Parameters:
    signal (ndarray): Оригинальный сигнал.
    filtered_signal (ndarray): Отфильтрованный сигнал.

    Returns:
    None
    """
    plt.figure()
    plt.plot(signal, label='Original Signal')
    plt.plot(filtered_signal[:len(signal)],'--' , label='Filtered Signal')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.title('Signal before and after filtering')
    plt.legend()
    plt.grid()
    plt.show()

def plot_frequency_spectrum(signal, fs, title):
    """
    Построение спектра сигнала.

    Parameters:
    signal (ndarray): Сигнал.
    fs (float): Частота дискретизации.
    title (str): Заголовок графика.

    Returns:
    None
    """
    freqs = np.fft.rfftfreq(len(signal), 1/fs)
    spectrum = np.abs(np.fft.rfft(signal))
    plt.figure()
    plt.plot(freqs, spectrum)
    plt.title(title)
    plt.xlabel("Частота (Гц)")
    plt.ylabel("Амплитуда")
    plt.grid()
    plt.show()

from scipy.signal import freqz

def plot_filter_response(b, a, fs, title="Frequency Response"):
    """
    Построение амплитудно-частотной характеристики фильтра.

    Parameters:
    b (ndarray): Коэффициенты числителя фильтра.
    a (ndarray): Коэффициенты знаменателя фильтра.
    fs (float): Частота дискретизации.
    title (str): Заголовок графика.

    Returns:
    None
    """
    w, h = freqz(b, a, worN=8000)
    plt.figure()
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), 'b')
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    # Параметры режекторного фильтра
    f0 = 0.5  # Частота, которую мы хотим подавить (в Гц)
    Q = 0.1   # "Добротность" фильтра
    fs = 1.0  # Частота дискретизации (в Гц), здесь частота дискретизации равна 1000 Гц

    # Загрузка данных из файла
    data = load_data('lab5_data6.txt')
    signal = data[:, 1]  # Данные из канала 0

    # Предварительное масштабирование сигнала
    signal = scale_signal(signal)

    # Расчет коэффициентов фильтра
    b, a = calculate_filter_coeffs(f0, Q, fs)

    # Фильтрация сигнала
    # filtered_signal = filter_signal(signal, b, a)
    # ИЛИ
    from scipy.signal import lfilter
    filtered_signal = lfilter(b, a, signal)

    # Визуализация сигнала до и после фильтрации
    plot_signals(signal, filtered_signal)

    # plot_frequency_spectrum(signal, fs, "Спектр оригинального сигнала")
    # plot_frequency_spectrum(filtered_signal, fs, "Спектр отфильтрованного сигнала")

    # Вывод графиков АЧХ фильтра
    plot_filter_response(b, a, fs, "Filter Frequency Response")


