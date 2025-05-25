import numpy as np
import matplotlib.pyplot as plt


# def f(x):
#     return np.cos(np.sqrt(np.abs(x))) - x

def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)


# Численная первая производная (разностный аналог)
def f_prime(x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


# Численная вторая производная (разностный аналог)
def f_double_prime(x, h=1e-5):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


def newton_method_with_plot(x0, epsilon=1e-6, max_iter=100):
    x = x0
    trajectory = [x]
    for k in range(max_iter):
        f_prime_val = f_prime(x)
        f_double_prime_val = f_double_prime(x)

        if f_double_prime_val == 0:
            print("Вторая производная равна нулю. Метод не может продолжаться.")
            return None, k, trajectory

        x_new = x - f_prime_val / f_double_prime_val
        trajectory.append(x_new)

        if abs(x_new - x) < epsilon:
            x = x_new
            break

        x = x_new

    return x, k + 1, trajectory


x_vals = np.linspace(-10, 10, 10000)
y_vals = f(x_vals)

x0 = 0.5
epsilon = 1e-4

extremum, iterations, trajectory = newton_method_with_plot(x0, epsilon)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, label="f(x)", color="blue")
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.scatter(extremum, f(extremum), color='red', label="Экстремум", zorder=5)
plt.title("График функции и экстремум")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()
plt.show()

if extremum is not None:
    print(f"Экстремум найден: x = {extremum:.6f}")
    print(f"Количество итераций: {iterations}")
    print(f"f(x) = {f(extremum):.6f}")
    print(f"f'(x) = {f_prime(extremum):.6f}")
    print(f"Точность: ε = {epsilon}")
else:
    print("Метод Ньютона не смог найти экстремум.")
