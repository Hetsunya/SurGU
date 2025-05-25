import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def func_linear_1(x):
    return abs(x - 2)

def func_linear_2(x):
   return 1 / abs(x - 2) 

def func_linear_3(x):
    return abs(x) - 2

def func_linear_4(x):
    return -abs(x) + 2

def func_linear_5(x):
    return -abs(x - 2) + 1

# Список функций и их названий
linear_functions = [func_linear_1, func_linear_2, func_linear_3, func_linear_4, func_linear_5]
linear_function_names = ['y = |x - 2|', 'y = 1 / |x - 2|', 'y = |x| - 2', 'y = -|x| + 2', 'y = -|x - 2| + 1']

# Генерация диапазона x
x_linear = np.linspace(-10, 10, 1000)

# Функция для построения графиков и взаимнокорреляции
def plot_linear_functions_and_correlation(func1, func2, x, title1, title2, ax):
    y1 = func1(x)
    y2 = func2(x)
    corr = signal.correlate(y2, y1, mode='full') / len(y1)
    lags = signal.correlation_lags(len(y1), len(y2), mode='full')
    
    ax[0].plot(x, y1, label=title1)
    ax[0].plot(x, y2, label=title2)
    ax[0].legend()
    ax[0].set_title(f'Оригинальные функции: {title1} и {title2}')
    
    ax[1].plot(lags, corr)
    ax[1].set_title(f'Кросс-корреляция между {title1} и {title2}')
    ax[1].set_xlabel('Лаги')
    ax[1].set_ylabel('Кросс-корреляция')

# Функция для отображения графиков в разных окнах
def display_graphs_in_separate_windows(functions, function_names, x_values):
    for i in range(len(functions)):
        for j in range(len(functions)):
            func1 = functions[i]
            func2 = functions[j]
            x = x_values
            title1 = function_names[i]
            title2 = function_names[j]

            # Создание новой фигуры для каждой пары функций
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))

            # Построение графиков функций и их кросс-корреляции
            plot_linear_functions_and_correlation(func1, func2, x, title1, title2, axs)

            # Показываем и закрываем текущий график перед переходом к следующему
            plt.show()
            plt.close(fig)
            

# Вызов функции для отображения графиков в разных окнах
display_graphs_in_separate_windows(linear_functions, linear_function_names, x_linear)

# Свертка между двумя функциями 
#  является интегральной операцией, которая выражает количество перекрытия одной функции, 
# когда она перевернута и сдвинута по отношению к другой. 

# Кросс-корреляция между двумя функциями 
# также измеряет степень схожести между функциями, но без переворачивания одной из функций. 
# Вместо этого, кросс-корреляция напрямую сдвигает одну функцию относительно другой и вычисляет суммы произведений. 