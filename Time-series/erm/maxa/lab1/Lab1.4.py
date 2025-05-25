import pandas as pd
from statsmodels.tsa.stattools import adfuller

file_path = '../EuStockMarkets.csv'
data = pd.read_csv(file_path)

def test_stationarity(timeseries, column_name):
    print(f'Результаты теста Дики-Фуллера для {column_name}:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Тестовая статистика', 'p-значение', 'Использовано лагов', 'Количество использованных наблюдений'])
    for key, value in dftest[4].items():
        dfoutput[f'Критическое значение ({key})'] = value
    print(dfoutput)

for column in ['DAX', 'SMI', 'CAC', 'FTSE']:
    test_stationarity(data[column], column)  


#На основе теста Дики-Фуллера мы видим,
#что все временные ряды индексов нестационарны, 
#что указывает на то, что в данных есть тренды или другие временные изменения. 
#Поэтому данные не являются однородными, и это предполагает наличие временных изменений в поведении рынка.