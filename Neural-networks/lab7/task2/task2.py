import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from sklearn.model_selection import train_test_split

# Генерация данных
data = np.arange(0, 2000, 1)  # Ряд данных
n_steps = 3
X, y = [], []

for i in range(len(data) - n_steps):
    X.append(data[i:i + n_steps])
    y.append(data[i + n_steps])

X = np.array(X)
y = np.array(y)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Изменение формы данных для RNN
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# Создание модели
model = Sequential()
model.add(SimpleRNN(50, activation='relu', input_shape=(n_steps, 1)))  # Слой RNN
model.add(Dense(1))  # Выходной слой

# Компиляция модели
model.compile(optimizer='adam', loss='mse')

# Обучение модели
model.fit(X_train, y_train, epochs=300, verbose=1)

# Тестирование модели
loss = model.evaluate(X_test, y_test)
print(f'Loss: {loss}')

# Пример нескольких предсказаний на тестовых данных
print("\nSeveral test predictions:")
for i in range(len(X_test)):  # Выведем предсказания для 5 последовательностей из тестовой выборки
    test_input = X_test[i].reshape((1, n_steps, 1))
    predicted = model.predict(test_input)
    print(f'Test Input: {X_test[i].flatten()}, True Value: {y_test[i]}, Predicted: {predicted.flatten()[0]}')
