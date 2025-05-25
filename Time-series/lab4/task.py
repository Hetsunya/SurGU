import math
import matplotlib.pyplot as plt
import numpy as np


def taylor_coeff(a, n):
  return math.comb(a, n) if n <= a else 0

def taylor_series(a, x, num_terms):
  return sum(taylor_coeff(a, n) * x**n for n in range(num_terms))

a = 6
x_values = np.linspace(-20, 20, 1000)
plt.figure(figsize=(8, 6))

# График оригинальной функции
plt.subplot(2, 1, 1)
plt.plot(x_values, (1 + x_values)**a, label=f"(1+x)^{a}")
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Оригинальная функция (1+x)^{a}')
plt.legend()
plt.grid(True)

# График аппроксимаций ряда Тейлора
plt.subplot(2, 1, 2)
for num_terms in [3, 5, 10]:
  y_values = [round(taylor_series(a, x, num_terms), 5) for x in x_values]
  plt.plot(x_values, y_values, label=f'Ряд Тейлора ({num_terms} членов)')

plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Аппроксимация функции (1+x)^{a} рядом Тейлора')
plt.legend()
plt.grid(True)

plt.tight_layout()  # Улучшение расположения графиков
plt.show()
