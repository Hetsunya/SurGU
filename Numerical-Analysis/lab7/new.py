import numpy as np
import matplotlib.pyplot as plt

# Задаём функцию и её аналитическую производную
def f(x):
    return np.cos(np.sqrt(np.abs(x))) - x

def analytical_derivative(x):
    if x == 0:
        return -1
    sqrt_abs_x = np.sqrt(np.abs(x))
    derivative_part = np.sin(sqrt_abs_x) / (2 * sqrt_abs_x)
    return derivative_part - 1

# Численные производные
def first_derivative_2nd_order(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

def first_derivative_4th_order(f, x, h):
    return (8 * (f(x + h) - f(x - h)) - (f(x + 2 * h) - f(x - 2 * h))) / (12 * h)

# Оценка погрешности методом Рунге
def runge_correction(value_h, value_h2, p):
    return abs(value_h - value_h2) / (2**p - 1)

# Параметры экспериментов
x_points = [-2, -1, 0, 1, 2]  # Точки, где ищем производную
h_values = [0.1, 0.05, 0.02, 0.01]  # Разные значения h

# Результаты для визуализации
results = {"x": [], "h": [], "numerical_2nd": [], "numerical_4th": [], "analytical": [], "error_2nd": [], "error_4th": [], "numpy": []}

# Функция для использования NumPy (чтобы вычислить производную по сетке)
def numpy_derivative(f, x, h):
    # Строим сетку значений около x
    x_values = np.array([x - h, x, x + h])
    f_values = f(x_values)
    return np.gradient(f_values, x_values)[1]  # Центральная производная для ближайших точек

for x_tilde in x_points:
    for h in h_values:
        # Численные производные
        numerical_2nd = first_derivative_2nd_order(f, x_tilde, h)
        numerical_2nd_h2 = first_derivative_2nd_order(f, x_tilde, h / 2)
        error_2nd = runge_correction(numerical_2nd, numerical_2nd_h2, 2)

        numerical_4th = first_derivative_4th_order(f, x_tilde, h)
        numerical_4th_h2 = first_derivative_4th_order(f, x_tilde, h / 2)
        error_4th = runge_correction(numerical_4th, numerical_4th_h2, 4)

        # Аналитическое значение
        analytical_value = analytical_derivative(x_tilde)

        # Численное значение с NumPy
        numpy_value = numpy_derivative(f, x_tilde, h)

        # Сохраняем результаты
        results["x"].append(x_tilde)
        results["h"].append(h)
        results["numerical_2nd"].append(numerical_2nd)
        results["numerical_4th"].append(numerical_4th)
        results["analytical"].append(analytical_value)
        results["error_2nd"].append(error_2nd)
        results["error_4th"].append(error_4th)
        results["numpy"].append(numpy_value)

        # Печать результатов для анализа
        print(f"x = {x_tilde}, h = {h}")
        print(f"  Аналитическая производная: {analytical_value}")
        print(f"  Численная (2-й порядок): {numerical_2nd}, ошибка: {error_2nd}")
        print(f"  Численная (4-й порядок): {numerical_4th}, ошибка: {error_4th}")
        print(f"  Численная (NumPy): {numpy_value}")

# Построение графиков
x_values = np.linspace(-5, 5, 5000)
f_values = f(x_values)
analytical_values = np.array([analytical_derivative(x) for x in x_values])

plt.figure(figsize=(12, 6))
plt.plot(x_values, f_values, label="f(x)", color="blue", linestyle="-")
plt.plot(x_values, analytical_values, label="Аналитическая производная", color="red", linestyle="--")

# Отображение результатов
for i, x_tilde in enumerate(x_points):
    plt.plot(
        x_values,
        np.full_like(x_values, results["numerical_2nd"][i]),
        label=f"Численная (2-й порядок) для x={x_tilde}",
        color="orange",
        linestyle='-', linewidth=1
    )
    plt.plot(
        x_values,
        np.full_like(x_values, results["numerical_4th"][i]),
        label=f"Численная (4-й порядок) для x={x_tilde}",
        color="purple",
        linestyle='-.', linewidth=1
    )
    plt.plot(
        x_values,
        np.full_like(x_values, results["numpy"][i]),
        label=f"NumPy производная для x={x_tilde}",
        color="brown",
        linestyle=":", linewidth=1
    )

plt.title("Графики функции и её производных")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()
