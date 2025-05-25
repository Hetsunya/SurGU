import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

##

##
# Раздел констант
a = -6  # начальная точка интервала
b = 6  # конечная точка интервала
N = 3 # число узлов (можно варьировать)

# Исходная функция
def f(x):
    return np.cos(np.sqrt(np.abs(x))) - x

# Узловые точки
x_nodes = np.linspace(a, b, N)
y_nodes = f(x_nodes)

# Кубический сплайн
spline = CubicSpline(x_nodes, y_nodes)

# Точки для построения графика
x_dense = np.linspace(a, b, 5999999)
y_dense = f(x_dense)
y_spline = spline(x_dense)

# Построение графиков
plt.figure(figsize=(10, 6))
plt.plot(x_dense, y_dense, label="Исходная функция", color="blue", lw=2)
plt.plot(x_dense, y_spline, label="Кубический сплайн", color="red", linestyle="--", lw=2)
plt.scatter(x_nodes, y_nodes, color="black", label="Узловые точки", zorder=5)

# Настройки графика
plt.title("Кубическая интерполяция сплайном")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()
