import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_path = 'lab5_data4.txt'
data = pd.read_csv(data_path, delimiter=';', encoding='cp1251')


plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(data['Канал0'], label='Канал 0')
plt.title('Сигнал с Канала 0')
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(data['Канал1'], label='Канал 1')
plt.title('Сигнал с Канала 1')
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

fft_channel0 = np.fft.fft(data['Канал0'])
fft_channel1 = np.fft.fft(data['Канал1'])

freqs = np.fft.fftfreq(len(data['Канал0']))

amplitude_channel0 = np.abs(fft_channel0)
amplitude_channel1 = np.abs(fft_channel1)
phase_channel0 = np.angle(fft_channel0)
phase_channel1 = np.angle(fft_channel1)

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.plot(freqs[:len(data['Канал0']) // 2], amplitude_channel0[:len(data['Канал0']) // 2], label='Канал 0')
plt.plot(freqs[:len(data['Канал1']) // 2], amplitude_channel1[:len(data['Канал1']) // 2], label='Канал 1', alpha=0.7)
plt.title('Амплитудно-частотная характеристика')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(freqs[:len(data['Канал0']) // 2], phase_channel0[:len(data['Канал0']) // 2], label='Канал 0')
plt.plot(freqs[:len(data['Канал1']) // 2], phase_channel1[:len(data['Канал1']) // 2], label='Канал 1', alpha=0.7)
plt.title('Фазо-частотная характеристика')
plt.xlabel('Частота')
plt.ylabel('Фаза')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

#AЧХ - МОДУЛЬ ОТ ДФТ
#ФЧХ - какой то угол

# АЧХ показывает, как амплитуда сигнала меняется в зависимости от частоты.
# Это важно для определения того, какие частоты присутствуют в сигнале и какова их амплитуда.

# По вертикальной оси отложена амплитуда (модуль результата ДФТ), а по горизонтальной оси — частота. 
# Пики на графике указывают на частоты, на которых сигнал имеет наибольшую амплитуду, иными словами, 
# это главные составляющие сигнала.


# ФЧХ показывает, как фаза сигнала меняется в зависимости от частоты. 
# Это важно для понимания сдвига фазы между различными частотными компонентами сигнала.

# По вертикальной оси отложена фаза (аргумент комплексного числа, полученного в результате ДФТ), 
# а по горизонтальной оси — частота. График показывает угол фазы для каждой частотной компоненты сигнала.