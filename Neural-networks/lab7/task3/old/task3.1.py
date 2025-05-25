import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split

# Загрузка данных
data = pd.read_csv('../Daily_minimum_temps.csv')  # замените на ваш файл
# Преобразуем столбец температур в float
data['Temp'] = pd.to_numeric(data['Temp'], errors='coerce')
data = data.dropna(subset=['Temp'])

# Дополнительные признаки
data['Date'] = pd.to_datetime(data['Date'])
data['DayOfWeek'] = data['Date'].dt.dayofweek
data['Month'] = data['Date'].dt.month

# Преобразование температур в float
temperatures = data['Temp'].astype(float).values
day_of_week = data['DayOfWeek'].values
month = data['Month'].values

# Формирование последовательностей с учётом дополнительных признаков
def create_sequences(data, day_of_week, month, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        seq_data = data[i:i + seq_length + 1]  # три предыдущие температуры и одна следующая
        seq_dow = day_of_week[i:i + seq_length]  # дни недели для этих значений
        seq_month = month[i:i + seq_length]  # месяцы для этих значений
        sequences.append((seq_data, seq_dow, seq_month))
    return sequences

sequence_length = 3
sequences = create_sequences(temperatures, day_of_week, month, sequence_length)

# Разделение на входные данные и целевые значения
X_temp = np.array([seq[0][:-1] for seq in sequences])  # первые три температуры
X_dow = np.array([seq[1] for seq in sequences])  # дни недели
X_month = np.array([seq[2] for seq in sequences])  # месяцы
y = np.array([seq[0][-1] for seq in sequences])  # четвертое значение

# Разделение на обучающую и тестовую выборки
X_temp_train, X_temp_test, X_dow_train, X_dow_test, X_month_train, X_month_test, y_train, y_test = train_test_split(
    X_temp, X_dow, X_month, y, test_size=0.2, shuffle=False
)

# Изменение формы для подачи в RNN (samples, timesteps, features)
X_temp_train = np.expand_dims(X_temp_train, -1)
X_temp_test = np.expand_dims(X_temp_test, -1)

# Модель biRNN с дополнительными признаками и регуляризацией
def create_model(input_shape_temp, input_shape_dow, input_shape_month):
    temp_input = Input(shape=input_shape_temp, name="temperature_input")
    dow_input = Input(shape=input_shape_dow, name="dayofweek_input")
    month_input = Input(shape=input_shape_month, name="month_input")

    # LSTM слой для температур
    x = Bidirectional(LSTM(512, return_sequences=False, kernel_regularizer=l2(0.001)))(temp_input)
    x = Dropout(0.2)(x)

    # Dense слои для других признаков
    dow_dense = Dense(32, activation='relu')(dow_input)
    month_dense = Dense(32, activation='relu')(month_input)

    # Объединение всех признаков
    concat = tf.keras.layers.concatenate([x, dow_dense, month_dense])
    outputs = Dense(1)(concat)

    model = Model(inputs=[temp_input, dow_input, month_input], outputs=outputs)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

# Создание и обучение модели
model = create_model((sequence_length, 1), (sequence_length,), (sequence_length,))
model.fit([X_temp_train, X_dow_train, X_month_train], y_train, epochs=75, batch_size=128, validation_data=([X_temp_test, X_dow_test, X_month_test], y_test))

# Оценка модели
loss, mae = model.evaluate([X_temp_test, X_dow_test, X_month_test], y_test)
print(f"Test MAE: {mae}")

# Пример предсказания
def predict_next_temperature(temps, dow, month):
    temps = np.expand_dims(temps, axis=0)
    temps = np.expand_dims(temps, -1)
    dow = np.expand_dims(dow, axis=0)
    month = np.expand_dims(month, axis=0)
    predicted_temp = model.predict([temps, dow, month])
    return predicted_temp[0][0]

# Пример предсказания для 3 значений
for i in range(5):
    example_temps = X_temp_test[i].squeeze()
    example_dow = X_dow_test[i].squeeze()
    example_month = X_month_test[i].squeeze()

print(f"Температуры для предсказания: {example_temps}")
predicted_temp = predict_next_temperature(example_temps, example_dow, example_month)
print(f"Предсказанная температура: {predicted_temp}")
print(f"Таргет температура: {y_test[0]}")
