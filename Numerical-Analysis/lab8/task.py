import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.cos(np.sqrt(np.abs(x))) - x

def rectangle_method(a, b, n, method='mid'):  # method: 'left', 'right', or 'mid'
    h = (b - a) / n
    if method == 'left':
        x = np.linspace(a, b - h, n)
    elif method == 'right':
        x = np.linspace(a + h, b, n)
    elif method == 'mid':
        x = np.linspace(a + h / 2, b - h / 2, n)
    else:
        raise ValueError("Invalid method. Choose 'left', 'right', or 'mid'.")

    # print(f"x = {x} | f(x) = {f(x)} | f(x) * h = {h * np.sum(f(x))}")
    print(f"x = {x} | f(x) = {f(x)} | f(x) * h = {h * f(x)}")
    return h * np.sum(f(x))

def aitken_extrapolation(I_n, I_2n, I_4n):
    return (I_2n**2 - I_n * I_4n) / (2 * I_2n - I_n - I_4n)

# Параметры интегрирования
a, b = -10, 10  # Пределы интегрирования
n = 5  # Начальное число разбиений

# Вычисление интегралов для n, 2n и 4n разбиений
I_n = rectangle_method(a, b, n, method='left')
I_2n = rectangle_method(a, b, 2 * n, method='left')
I_4n = rectangle_method(a, b, 4 * n, method='left')

# Оценка точности по Эйткену
I_aitken = aitken_extrapolation(I_n, I_2n, I_4n)

# Вывод результатов
print(f"I_n (n={n}): {I_n}")
print(f"I_2n (n={2*n}): {I_2n}")
print(f"I_4n (n={4*n}): {I_4n}")
print(f"Эйткеновская оценка: {I_aitken}")

# Визуализация
x = np.linspace(a, b, 5000)
y = f(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='f(x)', color='blue')

# Отрисовка прямоугольников
x_rect = np.linspace(a + (b - a) / (2 * n), b - (b - a) / (2 * n), n)
h = (b - a) / n
for xi in x_rect:
    plt.gca().add_patch(plt.Rectangle((xi - h / 2, 0), h, f(xi), color='orange', alpha=0.5))

plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.title('Метод прямоугольников')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid()
plt.show()
