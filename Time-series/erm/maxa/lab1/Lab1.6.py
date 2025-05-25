import pandas as pd
import matplotlib.pyplot as plt

file_path = '../EuStockMarkets.csv'
data = pd.read_csv(file_path)

def plot_scatter(data, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x], data[y], alpha=0.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

plot_scatter(data, 'DAX', 'SMI', 'Точечный график DAX против SMI', 'DAX', 'SMI')

plt.figure(figsize=(10, 6))
plt.scatter(data.index, data['DAX'], alpha=0.5, label='DAX', color='blue')
plt.scatter(data.index, data['SMI'], alpha=0.5, label='SMI', color='red')
plt.title('Изменения в DAX и SMI со временем')
plt.xlabel('Время (Индекс DataFrame)')
plt.ylabel('Значение индекса')
plt.legend()
plt.show()


#На основе предыдущих диаграмм рассеяния между DAX и SMI,
#можно увидеть, что точки на графике формируют четкую линию вверх и вправо, 
#что указывает на сильную положительную корреляцию. Это означает, что когда значение одного индекса увеличивается,
#значение другого, как правило, тоже увеличивается.

#Диаграмма рассеяния, отслеживающая изменения значений DAX и SMI со временем,
#показывает, как оба индекса изменяются по мере прохождения времени. 
#Если точки на этой диаграмме образуют некую траекторию,
#это может указывать на общие тенденции роста или падения на протяжении всего временного ряда.