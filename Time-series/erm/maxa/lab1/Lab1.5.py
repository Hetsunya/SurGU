import pandas as pd
import matplotlib.pyplot as plt

file_path = '../EuStockMarkets.csv'
data = pd.read_csv(file_path)

def plot_histograms(data, columns, title):
    fig, ax = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(title, fontsize=16)
    ax = ax.ravel()
    for i, col in enumerate(columns):
        data[col].hist(ax=ax[i], bins=50, alpha=0.7, color='blue')
        ax[i].set_title(f'Гистограмма {col}')
        ax[i].set_xlabel('Значение')
        ax[i].set_ylabel('Частота')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

plot_histograms(data, ['DAX', 'SMI', 'CAC', 'FTSE'], 'Гистограммы абсолютных значений')

data_diff = data[['DAX', 'SMI', 'CAC', 'FTSE']].diff().dropna()
print(data_diff [:5])
plot_histograms(data_diff, ['DAX', 'SMI', 'CAC', 'FTSE'], 'Гистограммы разностей')


#Гистограммы абсолютных значений показали, 
#что распределения индексов имеют различные диапазоны и формы, 
#что отражает их индивидуальные характеристики. 
#Гистограммы разностей, которые представляют собой дневные возвраты, показывают,
#что данные имеют изменчивость во времени, что является признаком волатильности на финансовых рынках.