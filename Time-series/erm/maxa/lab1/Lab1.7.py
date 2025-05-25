import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Загрузка данных
file_path = '../EuStockMarkets.csv'
data = pd.read_csv(file_path)

# Вычисление ковариационной матрицы
cov_matrix = data[['DAX', 'SMI']].cov()

# Вывод ковариационной матрицы
print("Ковариационная матрица:")
print(cov_matrix)

# Отображение графика ковариационной матрицы
plt.figure(figsize=(8, 6))
sns.heatmap(cov_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('График ковариационной матрицы')
plt.show()
