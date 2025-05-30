import pandas as pd

file_path = '../EuStockMarkets.csv'
data = pd.read_csv(file_path)

correlation_matrix = data[['DAX', 'SMI', 'CAC', 'FTSE']].corr()

print(correlation_matrix)
#Да, существуют. Ранее рассчитанная корреляционная матрица показала очень высокие коэффициенты
#корреляции между всеми индексами (от 0.915 до 0.991),
#что говорит о тесной взаимосвязи между ними. 
#Это означает, что изменения в одном индексе, вероятно, сопровождаются аналогичными изменениями в других индексах.