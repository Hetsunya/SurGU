import numpy as np
import matplotlib.pyplot as plt

# Функция для вычисления коэффициентов ряда Тейлора для e^x
def taylor_series_expansion(x, n):
    """
    Вычислить сумму первых n членов ряда Тейлора для e^x.
    :param x: Точка, в которой нужно оценить ряд
    :param n: Количество членов ряда Тейлора
    :return: Сумма первых n членов ряда Тейлора для e^x
    """
    return sum([(x**i) / np.math.factorial(i) for i in range(n)])

# Функция для сравнения - фактическая функция e^x
def actual_exp_function(x):
    return np.exp(x)

# Точки для оценки функций
x_values = np.linspace(0, 2, 400)
taylor_values_3 = taylor_series_expansion(x_values, 3)
taylor_values_5 = taylor_series_expansion(x_values, 5)
taylor_values_10 = taylor_series_expansion(x_values, 10)
taylor_values_25 = taylor_series_expansion(x_values, 25)
taylor_values_50 = taylor_series_expansion(x_values, 50)
actual_values = actual_exp_function(x_values)
print()

# Построение графика
plt.figure(figsize=(14, 8))
plt.plot(x_values, actual_values, label='Фактическая e^x')
plt.plot(x_values, taylor_values_3, label='Ряд Тейлора - 3 члена')
plt.plot(x_values, taylor_values_5, label='Ряд Тейлора - 5 членов')
plt.plot(x_values, taylor_values_10, label='Ряд Тейлора - 10 членов')
plt.plot(x_values, taylor_values_25, label='Ряд Тейлора - 25 членов')
plt.plot(x_values, taylor_values_50, label='Ряд Тейлора - 50 членов')
plt.title('Приближение e^x с помощью ряда Тейлора')
plt.xlabel('x')
plt.ylabel('e^x')
plt.legend()
plt.grid(True)
plt.show()
