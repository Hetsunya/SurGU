import numpy as np
import matplotlib.pyplot as plt

# Определяем функцию и её аналитическую производную
def f(x):
    return np.cos(np.sqrt(np.abs(x))) - x

def analytical_derivative(x):
    sqrt_abs_value = np.sqrt(np.abs(x))
    # Если x = 0, то возвращаем NaN, иначе вычисляем производную
    derivative_part = np.sin(sqrt_abs_value) / (2 * sqrt_abs_value) if x != 0 else np.nan
    return -derivative_part * np.sign(x) - 1

# Численная производная (2-й порядок точности)
def first_derivative_2nd_order(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

# Численная производная (4-й порядок точности)
def first_derivative_4th_order(f, x, h):
    return (8 * (f(x + h) - f(x - h)) - (f(x + 2 * h) - f(x - 2 * h))) / (12 * h)

# Оценка погрешности методом Рунге
def runge_correction(value_h, value_h2, p):
    return abs(value_h - value_h2) / (2**p - 1)

# Задаем экспериментальные точки и шаги
experiments = [
    {"x_tilde": -1, "h": 0.1},
    # {"x_tilde": -0.5, "h": 0.01},
    {"x_tilde": 0, "h": 0.05},
    # {"x_tilde": 0.5, "h": 0.02},
    {"x_tilde": 1, "h": 0.2},
    # {"x_tilde": 0.679192, "h": 0.05}
]

x_values = np.linspace(-5, 5, 5000)  # Точки для построения графиков
f_values = f(x_values)
analytical_values = np.array([analytical_derivative(x) for x in x_values])

x_tilde_points = []
for exp in experiments:
    x_tilde = exp["x_tilde"]
    h = exp["h"]

    numerical_2nd = first_derivative_2nd_order(f, x_tilde, h)
    numerical_2nd_h2 = first_derivative_2nd_order(f, x_tilde, h / 2)
    error_2nd = runge_correction(numerical_2nd, numerical_2nd_h2, 2)

    numerical_4th = first_derivative_4th_order(f, x_tilde, h)
    numerical_4th_h2 = first_derivative_4th_order(f, x_tilde, h / 2)
    error_4th = runge_correction(numerical_4th, numerical_4th_h2, 4)

    analytical_value = analytical_derivative(x_tilde)

    print(f"\nЭксперимент для x_tilde = {x_tilde}, h = {h}:")
    print(f"  Аналитическое значение: {analytical_value}")
    print(f"  Численное значение (2-й порядок): {numerical_2nd}")
    print(f"  Оценка погрешности (2-й порядок): {error_2nd}")
    print(f"  Численное значение (4-й порядок): {numerical_4th}")
    print(f"  Оценка погрешности (4-й порядок): {error_4th}")

    x_tilde_points.append((x_tilde, analytical_value))

# Визуализация
plt.figure(figsize=(10, 6))
plt.plot(x_values, f_values, label="f(x)", color="blue")
plt.plot(x_values, analytical_values, label="Аналитическая производная", color="red")

for x_tilde, value in x_tilde_points:
    plt.scatter(x_tilde, value, color="green", zorder=5, label=f"x_tilde={x_tilde:.2f}")
    plt.text(x_tilde, value, f"({x_tilde:.2f}, {value:.2f})", color="green", fontsize=9, ha='right')

plt.title("График функции и её первой производной")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()
