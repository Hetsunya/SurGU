import numpy as np
import matplotlib.pyplot as plt

# Раздел констант
a = -10  # начальная точка интервала
b = 10   # конечная точка интервала
N = 5  # число узлов (можно варьировать)

# Исходная функция
def f(x):
    return np.float64(np.cos(np.sqrt(np.abs(x))) - x)

# Точки для построения графика (густая сетка)
x_dense = np.linspace(np.float64(a), np.float64(b), 1000000)
y_dense = f(x_dense)

# Узловые точки
x_nodes = np.linspace(np.float64(a), np.float64(b), N)

# Узловые значения
y_nodes = np.array([y_dense[np.argmin(np.abs(x_dense - x))] for x in x_nodes])

# Функция для построения кубического сплайна
def cubic_spline(x, x_nodes, y_nodes):
    n = len(x_nodes) - 1  # Число отрезков
    h = np.diff(x_nodes)  # Длины интервалов
    alpha = np.zeros(n - 1)  # Вспомогательный массив для системы уравнений

    print(f"\nУзловые точки x_nodes: {x_nodes}")
    print(f"Значения в узлах y_nodes: {y_nodes}")
    print(f"Длины интервалов h: {h}")

    # Вычисление массива alpha для системы уравнений
    for i in range(1, n):
        alpha[i - 1] = (3 / h[i] * (y_nodes[i + 1] - y_nodes[i]) -
                        3 / h[i - 1] * (y_nodes[i] - y_nodes[i - 1]))
        print(f"alpha[{i - 1}] = {alpha[i - 1]} (основано на узлах {i - 1}, {i}, {i + 1})")

    # Решение трёхдиагональной системы методом прогонки
    l = np.ones(n + 1)  # Диагональные элементы матрицы
    mu = np.zeros(n)    # Верхняя диагональ
    z = np.zeros(n + 1) # Правая часть системы

    for i in range(1, n):
        l[i] = 2 * (x_nodes[i + 1] - x_nodes[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i - 1] - h[i - 1] * z[i - 1]) / l[i]
        print(f"Шаг {i}: l[{i}] = {l[i]}, mu[{i}] = {mu[i]}, z[{i}] = {z[i]}")

    # Обратный ход для нахождения коэффициентов c[i]
    c = np.zeros(n + 1)
    b = np.zeros(n)
    d = np.zeros(n)
    a = np.zeros(n)

    for j in range(n - 1, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = ((y_nodes[j + 1] - y_nodes[j]) / h[j] -
                h[j] * (c[j + 1] + 2 * c[j]) / 3)
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])
        a[j] = y_nodes[j]
        print(f"\nКоэффициенты для интервала [{x_nodes[j]}, {x_nodes[j + 1]}]:")
        print(f"  a[{j}] = {a[j]}, b[{j}] = {b[j]}, c[{j}] = {c[j]}, d[{j}] = {d[j]}")
        print(
            f"  Формула: S_{j}(x) = {a[j]:.4f} + {b[j]:.4f}*(x - {x_nodes[j]:.4f}) + {c[j]:.4f}*(x - {x_nodes[j]:.4f})^2 + {d[j]:.4f}*(x - {x_nodes[j]:.4f})^3")

    # Построение значения сплайна
    spline_values = np.zeros_like(x)
    for i in range(n):
        idx = (x >= x_nodes[i]) & (x < x_nodes[i + 1])  # Индексы точек в данном интервале
        dx = x[idx] - x_nodes[i]
        spline_values[idx] = a[i] + b[i] * dx + c[i] * dx**2 + d[i] * dx**3
    spline_values[x == x_nodes[-1]] = y_nodes[-1]  # Последняя точка
    return np.float64(spline_values)

# Построение сплайна
y_spline = cubic_spline(x_dense, x_nodes, y_nodes)

# Построение графиков
plt.figure(figsize=(10, 6))
plt.plot(x_dense, y_dense, label="Исходная функция", color="blue", lw=2)
plt.plot(x_dense, y_spline, label="Кубический сплайн", color="red", linestyle="--", lw=2)
plt.scatter(x_nodes, y_nodes, color="black", label="Узловые точки", zorder=5)

# Настройки графика
plt.title("Кубическая интерполяция сплайном (с выводом информации)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()
