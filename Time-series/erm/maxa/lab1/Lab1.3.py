import pandas as pd

file_path = '../EuStockMarkets.csv'
data = pd.read_csv(file_path)

half = len(data) // 2
first_half = data[:half]
second_half = data[half:]

range_first_half = first_half[['DAX', 'SMI', 'CAC', 'FTSE']].agg(['min', 'max'])
range_second_half = second_half[['DAX', 'SMI', 'CAC', 'FTSE']].agg(['min', 'max'])

print("Первая половина данных:\n", range_first_half)
print("Вторая половина данных:\n", range_second_half)

#Да, изменяется. Минимальные и максимальные значения в первой и второй половине данных показывают,
#что диапазон значений увеличивается во второй половине набора данных.
#Это может указывать на увеличение волатильности рынка или на долгосрочные тренды роста стоимости индексов.