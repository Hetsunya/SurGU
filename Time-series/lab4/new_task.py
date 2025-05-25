import math
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

#sin(0) = 0
#cos(0) = 1
#-sin(0) = 0
#-cos(0) = -1
#sin(0) = 0
def taylor_coeff(n):
    return (-1)**n / math.factorial(2*n + 1)

def taylor_series(x, num_terms):
    return sum(taylor_coeff(n) * x**(2*n + 1) for n in range(num_terms))

for i in range(3):
    print(taylor_coeff(i))

x_values = np.linspace(-4, 4, 1000)
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(x_values, np.sin(x_values), label='sin(x)', color='blue')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Оригинальная функция sin(x)')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
for num_terms in [3, 5, 10, 25, 50]:
    y_values = [taylor_series(x, num_terms) for x in x_values]
    plt.plot(x_values, y_values, label=f'Ряд Тейлора ({num_terms} членов)')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Аппроксимация sin(x) рядом Тейлора (числовое разложение)')
plt.legend()
plt.grid(True)

x_sym = sp.symbols('x')
f = sp.sin(x_sym)

print(sp.series(f, x_sym, 0, 6))

plt.subplot(3, 1, 3)
for num_terms in [3, 5, 10, 25, 50]:
    taylor_expansion = sp.series(f, x_sym, 0, num_terms*2).removeO()
    y_values_sympy = sp.lambdify(x_sym, taylor_expansion, "numpy")(x_values)
    plt.plot(x_values, y_values_sympy, label=f'Ряд Тейлора SymPy ({num_terms} членов)', linestyle='--')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Аппроксимация sin(x) рядом Тейлора (через SymPy)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
