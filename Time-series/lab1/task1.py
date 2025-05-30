pimport pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('EuStockMarkets.csv')

'''
rownames — названия строк.  
DAX — ежедневные цены закрытия немецкого фондового индекса DAX (Deutscher Aktienindex).  
SMI — ежедневные цены закрытия швейцарского фондового индекса SMI (Swiss Market Index).  
CAC*— ежедневные цены закрытия французского фондового индекса CAC 40 (Cotation Assistée en Continu).  
FTSE — ежедневные цены закрытия британского фондового индекса FTSE 100 (Financial Times Stock Exchange 100 Index).  
'''

print("\nВопрос 1: Существуют ли в наборе данных взаимосвязанные столбцы?")
correlation_matrix = df.corr()
print("Матрица корреляции:")
print(correlation_matrix)

print("\nВопрос 2: Среднее значение и дисперсия")
mean_values = df.mean()
variance_values = df.var()
print("\nСреднее значение:")
print(mean_values)
print("\nДисперсия:")
print(variance_values)

print("\nВопрос 3: Изменяется ли диапазон доступных значений?")
max_values = df.max()
min_values = df.min()
range_values = max_values - min_values
print("\nМаксимальные значения:")
print(max_values)
print("\nМинимальные значения:")
print(min_values)
print("\nИзменение диапазона значений:")
print(range_values)

print("\nВопрос 4: Однородны ли данные")
std_deviation_values = df.std()
print("\nСтандартное отклонение:")
print(std_deviation_values)

print("\nВопрос 5: Построить гистограмму абсолютных значений и гистограмму разностей")
absolute_histogram = df.abs().hist(bins=20, figsize=(10, 6))
plt.suptitle('Гистограмма абсолютных значений')
plt.show()

difference_histogram = df.diff().hist(bins=20, figsize=(10, 6))
plt.suptitle('Гистограмма разностей')
plt.show()

print("\nВопрос 6: Построить две диаграммы рассеяния")
plt.scatter(df['DAX'], df['SMI'])
plt.title('Диаграмма рассеяния между DAX и SMI')
plt.xlabel('DAX')
plt.ylabel('SMI')
plt.show()

plt.scatter(df.index, df['DAX'], label='DAX')
plt.scatter(df.index, df['SMI'], label='SMI')
plt.title('Диаграмма рассеяния временных изменений DAX и SMI')
plt.xlabel('Время')
plt.ylabel('Значения')
plt.legend()
plt.show()
print("\nВопрос 7: Ковариация и ковариационная матрица")
covariance = df[['DAX', 'SMI']].cov().iloc[0, 1]
covariance_matrix = df.cov()
print("\nКовариация DAX и SMI:")
print(covariance)
print("\nКовариационная матрица:")
print(covariance_matrix)

# Вопрос 8: Найти и продемонстрировать интересную ложную корреляцию
# https://www.tylervigen.com/spurious-correlations


# Вопрос 1: Взаимосвязь столбцов
# Корреляция: измеряет линейную зависимость между двумя переменными. Значение от -1 до 1, где 1 - идеальная положительная корреляция, -1 - идеальная отрицательная, а 0 - отсутствие корреляции.
# Матрица корреляции: таблица, показывающая коэффициенты корреляции между всеми парами переменных в наборе данных.
# Вопрос 2: Среднее значение и дисперсия
# Среднее значение: среднее арифметическое значений в наборе данных, которое дает представление о центральной тенденции.
# Дисперсия: измеряет, насколько сильно данные разбросаны вокруг среднего значения. Большая дисперсия указывает на большую степень разброса.
# Вопрос 3: Изменение диапазона значений
# Диапазон: разница между максимальным и минимальным значениями в наборе данных. Анализ диапазона помогает выявить потенциальные выбросы или изменения в поведении данных с течением времени.
# Вопрос 4: Однородность данных
# Стандартное отклонение: квадратный корень из дисперсии, дает представление о типичном отклонении от среднего значения.
# Вопрос 5: Гистограммы
# Гистограмма абсолютных значений: показывает распределение абсолютных значений данных, что полезно для понимания общей изменчивости.
# Гистограмма разностей: показывает распределение разностей между последовательными значениями, что помогает выявить тенденции или сезонные эффекты.
# Вопрос 6: Диаграммы рассеяния
# Диаграмма рассеяния между двумя акциями: помогает выявить потенциальные корреляции или зависимости между двумя акциями.
# Диаграмма рассеяния временных изменений: отображает, как значения каждой акции изменяются с течением времени.
# Вопрос 7: Ковариация
# Ковариация: измеряет, как две переменные изменяются вместе. Положительная ковариация указывает, что переменные имеют тенденцию двигаться в одном направлении, а отрицательная - в противоположных направлениях.
# Ковариационная матрица: таблица, показывающая ковариацию между всеми парами переменных в наборе данных.
