from scipy.signal import convolve
import matplotlib.pyplot as plt
import numpy as np

# Определение функции f(x) с использованием NumPy для работы с массивами
def f(x):
    return np.where((x > 0) & (x < 1), 1, 0)

# Шаг дискретизации
step = 0.01

# Создаем массив x для интервала от -1 до 2 с шагом 0.01
x = np.arange(0, 4, step)

# Вычисляем значения функции f(x) для этого массива
f_values = f(x)

# Используем функцию convolve из scipy.signal для вычисления свертки
convolved = convolve(convolve(f_values, f_values, mode='full') * step, convolve(f_values, f_values, mode='full') * step,mode='full') * step# умножаем на шаг для масштабирования

# Рассчитываем новые значения x для свертки
# Удвоенный размер минус один, потому что это свертка двух одинаковых массивов
conv_x = np.linspace(2*x[0], 2*x[-1], len(convolved))

# Построение графика свертки
plt.figure(figsize=(10,5))
plt.plot(conv_x, convolved)
plt.title('График свертки функции f(x)')
plt.xlabel('x')
plt.ylabel('Свертка (f * f)(x)')
plt.grid(True)
plt.show()
