import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Загрузка данных
data = pd.read_csv('../Daily_minimum_temps.csv')
# data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%y')
data['Temp'] = pd.to_numeric(data['Temp'], errors='coerce')
data['Temp'] = data['Temp'].astype(float)

# Подготовка данных
def create_sequences(data, n_steps):
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:i + n_steps])
        y.append(data[i + n_steps])
    return np.array(X), np.array(y)

n_steps = 3
temp_values = data['Temp'].values
X, y = create_sequences(temp_values, n_steps)

# Преобразуем входы в форму [samples, timesteps, features]
X = X.reshape((X.shape[0], X.shape[1], 1))

# Построение модели
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(n_steps, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Обучение модели
model.fit(X, y, epochs=50, batch_size=32, verbose=1)

# Пример предсказания
x_input = np.array([15.8, 15.8, 17.4])  # Последние три температуры
x_input = x_input.reshape((1, n_steps, 1))
y_pred = model.predict(x_input)
print("Прогноз:", y_pred[0][0])
