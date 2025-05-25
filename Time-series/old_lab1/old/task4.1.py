import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima

# Загрузка данных
data = pd.read_csv("../AirQualityUCI.csv", delimiter=';')
data['CO(GT)'] = data['CO(GT)'].replace(',', '.', regex=True).astype(float)

# Удаление выбросов -200
data = data[data['CO(GT)'] != -200]

# Обработка пропущенных значений (заполнение медианой)
data['CO(GT)'].fillna(data['CO(GT)'].median(), inplace=True)

# Обработка даты и времени
data['DateTime'] = pd.to_datetime(data["Date"] + " " + data["Time"], format='%d/%m/%Y %H.%M.%S')

# Автоматический подбор параметров
auto_model = auto_arima(data['CO(GT)'], seasonal=True)
print(auto_model.summary())

# Создание и обучение модели ARIMA
model = ARIMA(data['CO(GT)'], order=auto_model.order)
results = model.fit()

# Предсказание n = 1000
n = 1000
start = len(data)  #  Используем порядковый номер последней строки
forecast = results.predict(start=start, end=start + n - 1, dynamic=True)

# Создание индекса для прогноза 
forecast_index = pd.RangeIndex(start=start, stop=start + n)  
forecast = pd.Series(forecast, index=forecast_index)

# Построение графика
plt.figure(figsize=(16, 5))
plt.plot(data['CO(GT)'], label='Actual Data')
plt.plot(forecast, label='ARIMA Forecast', linestyle='--', color='red')
plt.title('ARIMA Model Forecast')
plt.xlabel('Index')
plt.ylabel('CO(GT)')
plt.grid(True) # Добавление сетки
plt.legend()
plt.show()