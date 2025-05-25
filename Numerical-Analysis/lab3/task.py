import numpy as np
import matplotlib.pyplot as plt


# График функции и запуск метода Ньютона
x0 = -1.25 # Начальная точка
epsilon = 1e-6
# h = 1e-2
h= 0.005

# Функция f(x)
# def f(x):
#     return np.cos(np.sqrt(np.abs(x))) - x

def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)

def f_numeric(x, h=1e-5):
    return (f(x + h) - f(x)) / h

# Численная первая производная (разностный аналог)
def f_prime_numeric(x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

# Численная вторая производная (разностный аналог)
def f_double_prime_numeric(x, h=1e-5):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h**2)

# Метод Ньютона с визуализацией касательных
def newton_method_numeric_with_visualization(x0, h=h, epsilon=1e-5, max_iter=100):
    x = x0
    x_vals = np.linspace(-10, 10, 10000)
    y_vals = f(x_vals)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label="f(x) = cos(sqrt(|x|)) - x", color="blue")
    plt.axhline(0, color='black', linestyle='--', linewidth=0.5)
    plt.axvline(0, color='black', linestyle='--', linewidth=0.5)
    plt.title("Метод Ньютона с визуализацией касательных")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)

    for k in range(max_iter):
        fx = f(x)
        print(x)
        fx_numeric = f_numeric(x, h)
        fx_prime = f_prime_numeric(x, h)
        fx_double_prime = f_double_prime_numeric(x, h)

        print(f"итерация {k}")
        print(f"x = {x}, f(x) = {f(x)}, fx_prime = {fx_prime}, fx_double_prime = {fx_double_prime}")
        # Проверка на малое значение производной
        if abs(fx_prime) < epsilon:
            break

        # Проверка на деление на ноль
        if fx_double_prime == 0:
            print("Вторая производная равна нулю, метод не применим.")
            plt.legend()
            plt.show()
            return None, k

        # Итерационное обновление
        x_new = x - fx_prime / fx_double_prime
        print(f" x_new = {x - fx_prime / fx_double_prime}")
        #
        # x_new = x - fx_numeric / fx_prime
        # print(f"x new = {x - fx_numeric / fx_prime}")
        # print(f"    Итерация {k+1}: x_new = {x_new:.6f}, f(x) = {f(x_new):.6f}")

        # Построение касательной
        tangent_y_vals = fx + fx_prime * (x_vals - x)
        plt.plot(x_vals, tangent_y_vals, '--', label=f"Касательная на итерации {k+1}")

        # Проверка критерия сходимости
        if abs(x_new - x) < epsilon:
            plt.scatter(x_new, f(x_new), color="red", zorder=5, label=f"Решение x = {x_new:.6f}")
            plt.legend()
            plt.show()
            return x_new, k + 1, f(x_new), fx_prime

        x = x_new

    plt.legend()
    plt.show()
    return x, max_iter, f(x), fx_prime

result = newton_method_numeric_with_visualization(x0=x0, h=h, epsilon=epsilon)

# Вывод результата
if result[0] is not None:
    x_extremum, iterations, f_val, f_prime_val = result
    print(f"Найденное значение x(k): {x_extremum}")
    print(f"Количество итераций k: {iterations}")
    print(f"Значение функции f(x(k)): {f_val}")
    print(f"Значение производной f'(x(k)): {f_prime_val}")
    print(f"Точность ε: {epsilon}")
else:
    print("Метод не сошелся.")
