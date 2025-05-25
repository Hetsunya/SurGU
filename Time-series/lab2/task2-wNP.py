import numpy as np
import matplotlib.pyplot as plt

# Определение функций
def f1(x):
    return np.sin(np.abs(2 * x)) 

def f2(x):
    return np.abs(x) - np.sin(x)  

def f3(x):
    return np.log(np.abs(x - 1)) 

def f4(x):
    return 4 * x**2 * np.exp(2 * x) 

def f5(x):
    return np.sqrt(np.abs(x) + 1)

# Вычисление взаимной корреляции с помощью NumPy
def cross_correlation_numpy(x, y, max_lag):
    return np.correlate(x, y, mode='full')[len(x)-max_lag-1:len(x)+max_lag]

# Основная часть кода
x_values = np.linspace(-5, 5, 1000)
functions = [f1, f2, f3, f4, f5]

for i in range(len(functions)):
    for j in range(i + 1, len(functions)):
        y1 = functions[i](x_values)
        y2 = functions[j](x_values)

        cross_corr_result = cross_correlation_numpy(y1, y2, 50)
        lags = np.arange(-50, 51)

        # Построение графиков
        plt.figure(figsize=(10, 6))

        plt.subplot(2, 1, 1)
        plt.plot(x_values, y1, label=f'Function {i + 1}')
        plt.plot(x_values, y2, label=f'Function {j + 1}')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(lags, cross_corr_result, label='Cross-correlation')
        plt.xlabel('Lag')
        plt.ylabel('Correlation')
        plt.legend()

        plt.tight_layout()
        plt.show()
