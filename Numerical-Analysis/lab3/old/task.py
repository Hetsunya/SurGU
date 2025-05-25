import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.cos(np.sqrt(np.abs(x))) - x


def f_prime(x):
    # Производная функции
    if x == 0:
        return -1  # Устанавливаем производную в точке x=0 равной -1
    return -0.5 * np.sin(np.sqrt(np.abs(x))) / np.sqrt(np.abs(x)) - 1


def numerical_derivative(func, x, h=1e-5):
    return (func(x + h) - func(x - h)) / (2 * h)


def newton_method(x0, epsilon=1e-4, max_iter=1000):
    x_k = x0
    for k in range(max_iter):
        # Используем разностный аналог для производной
        f_prime_k = numerical_derivative(f, x_k)

        if f_prime_k == 0:  # Избежание деления на ноль
            print("Производная равна нулю. Метод не может продолжаться.")
            return None

        x_next = x_k - f(x_k) / f_prime_k

        if abs(x_next - x_k) < epsilon:
            print(f"Решение: x = {x_next}")
            print(f"Количество итераций: {k + 1}")
            print(f"f(x) = {f(x_next)}")
            print(f"f'(x) = {f_prime_k}")
            return x_next

        x_k = x_next

    print("Метод не сошелся за максимальное количество итераций.")
    return None


# Графический метод для локализации
x_values = np.linspace(-10, 10, 400)
y_values = f(x_values)

plt.plot(x_values, y_values, label='f(x) = cos(sqrt(abs(x))) - x')
plt.axhline(0, color='red', lw=1, linestyle='--')
plt.axvline(0, color='green', lw=1, linestyle='--')
plt.title('График функции для локализации экстремума')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid()
plt.show()

# Пример использования
x0 = 0.5  # Начальное приближение
newton_method(x0)
