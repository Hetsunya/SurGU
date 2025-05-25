import numpy as np
import matplotlib.pyplot as plt
from sympy import *

# Определение функции
def f(x):
    return np.cos(np.sqrt(np.abs(x))) - x

# Итерационная функция g(x) для метода простых итераций
# def g(x):
#     return np.cos(np.sqrt(np.abs(x)))

# # Итерационная функция g(x) для метода простых итераций
# def g(x):
#     return np.cos(x)

def g(x):
    return (np.cos(np.sqrt(np.abs(x))) + x) / 2



# Построение графика с итерациями
def plot_iterations(iter_values):
    x_vals = np.linspace(-1, 1, 10000)
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals, label='f(x) = cos(sqrt(|x|)) - x', color='blue')
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')

    # Отображение точек итераций
    for i, x in enumerate(iter_values):
        plt.scatter(x, f(x), color='red')
        plt.text(x, f(x), f'{i+1}', fontsize=8, ha='right')

    plt.title('График функции f(x) и итерационные точки')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Метод простых итераций
def simple_iteration_method(x0, eps=1e-4, max_iter=1000):
    iter_values = []

    print(f"Начальная точка: x0 = {x0:.6f}")

    for k in range(max_iter):
        x1 = g(x0)  # Следующая итерация

        print(f"Итерация {k+1}: x0 = {x0:.6f}, g(x0) = {x1:.6f}, f({x1}) = {f(x1):.6f}")

        # Проверка на достижение точности
        if abs(x1 - x0) < eps:
            print(f"Решение найдено: x = {x1:.6f}, f(x) = {f(x1):.6f}, количество итераций = {k+1}, точность = {eps}")
            iter_values.append(x1)
            plot_iterations(iter_values)
            return x1, k+1

        x0 = x1  # Обновление текущей точки

    print(f"Решение не найдено за {max_iter} итераций, точность = {eps}")
    plot_iterations(iter_values)
    return None, max_iter

# Начальная точка и вызов метода
x0 = 0.1  # Начальная точка
simple_iteration_method(x0)
