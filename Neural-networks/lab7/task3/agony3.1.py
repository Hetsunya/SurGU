import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import Huber

# Загрузка данных
data = pd.read_csv('Daily_minimum_temps.csv')

# Проверка значений и замена некорректных значений на NaN
data['Temp'] = pd.to_numeric(data['Temp'], errors='coerce')  # Преобразуем к числовому формату
data.dropna(inplace=True)  # Удаляем строки с NaN

# Преобразование данных в массив
temps = data['Temp'].values.reshape(-1, 1)

print(temps)

# Класс для нормализации данных
class Normalize:
    def __init__(self, data: np.ndarray) -> None:
        self.data: np.ndarray = np.copy(data)
        self.__mean: np.ndarray = data.mean(axis=0)
        self.__std_dev: np.ndarray = data.std(axis=0)
        print(f"self.data = {self.data}"
              f"self.__mean = {self.__mean}"
              f"self.__std_dev = {self.__std_dev}")

    def normalizeData(self) -> np.ndarray:
        return (self.data - self.__mean) / self.__std_dev

    def DeNormalizeData(self, normalized_data: np.ndarray) -> np.ndarray:
        return normalized_data * self.__std_dev + self.__mean

# Инициализация нормализатора
normalizer = Normalize(temps)

# Нормализация данных
temps_scaled = normalizer.normalizeData()

# Функция для подготовки данных для модели
def create_dataset(data, look_back=3):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])  # Используем 3 предыдущих значения
        y.append(data[i + look_back, 0])  # 4-е значение (цель)
    return np.array(X), np.array(y)

# Подготовка данных
look_back = 3
X, y = create_dataset(temps_scaled, look_back)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Преобразование данных для подачи в LSTM
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))


from tensorflow.keras.layers import Bidirectional

# Создание модели с двунаправленным LSTM (biRNN)
model = Sequential([
    Bidirectional(LSTM(128, return_sequences=False), input_shape=(X_train.shape[1], X_train.shape[2])),  # Двунаправленный LSTM
    Dropout(0.2),
    Dense(1)
])


early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Компиляция модели
model.compile(optimizer='adam', loss=Huber(delta=1.0))

# Обучение модели с ранней остановкой
history = model.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test),
                     batch_size=4, callbacks=[early_stopping])


# Предсказание на тестовых данных
predicted = model.predict(X_test)

# Обратная денормализация
predicted = normalizer.DeNormalizeData(predicted)
y_test = normalizer.DeNormalizeData(y_test.reshape(-1, 1))

# Оценка модели
mse = mean_squared_error(y_test, predicted)
mae = mean_absolute_error(y_test, predicted)
print(f'MSE: {mse:.4f}')
print(f'MAE: {mae:.4f}')

# Вывод первых 10 реальных и предсказанных значений
for i in range(10):
    print(f"Реальные значения: {y_test[i][0]:.2f}, Предсказанные значения: {predicted[i][0]:.2f}")

# График процесса обучения
plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Loss на обучающей выборке', color='blue')
plt.plot(history.history['val_loss'], label='Loss на валидационной выборке', color='orange')
plt.xlabel('Эпоха')
plt.ylabel('Loss')
plt.yscale('log')  # Логарифмическая шкала
plt.title('Процесс обучения модели')
plt.legend()
plt.show()

# График сравнения реальных значений и предсказаний
plt.figure(figsize=(14, 7))
plt.plot(range(len(y_test)), y_test, label='Реальные значения', color='green')
plt.plot(range(len(predicted)), predicted, label='Предсказания', color='red')
plt.fill_between(range(len(y_test)), y_test.flatten(), predicted.flatten(), color='gray', alpha=0.2, label='Разница')
plt.xlabel('Наблюдение')
plt.ylabel('Температура')
plt.title('Сравнение реальных значений и предсказаний')
plt.legend()
plt.show()
