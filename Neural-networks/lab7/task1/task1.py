import numpy as np
from SimpleRNN import SimpleRNN
from sklearn.model_selection import train_test_split

# Генерация данных для обучения
data = np.arange(0, 3000, 1)  # Увеличиваем диапазон данных
n_steps = 3
X, y = [], []

# Создание выборки
for i in range(len(data) - n_steps):
    X.append(data[i:i + n_steps])
    y.append(data[i + n_steps])

X = np.array(X)
y = np.array(y)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# Настройка RNN
input_size = 1
hidden_size = 15  # Увеличиваем размер скрытого слоя
output_size = 1
rnn = SimpleRNN(input_size, hidden_size, output_size)

# Изменяем размерность для RNN
# X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], input_size)
# X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], input_size)

# Обучение модели
rnn.train(X_train, y_train.reshape(-1, 1), epochs=2000, learning_rate=0.001)

# Проверим размер тестовой выборки
print(f"Test set size: {X_test.shape[0]}")

# Тестирование модели на нескольких примерах
n_tests = X_test.shape[0] # Ограничиваем количество тестов размером выборки
for i in range(n_tests):
    test_input = X_test[i].reshape(1, n_steps, input_size)
    predicted = rnn.predict(test_input)
    print(f'Test Input: {X_test[i].flatten()}, Target: {y_test[i]}, Predicted: {predicted}')
