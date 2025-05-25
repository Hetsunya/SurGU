import pandas as pd
from src.neural_network import NeuralNetwork
import numpy as np

# Загрузка данных
data = pd.read_csv('data/2lab_data.csv')
X = data.iloc[:, :6].values  # Первые 6 столбцов — входные данные
y = data.iloc[:, 6:].values  # Остальные столбцы — целевые значения

train_size = int(0.8 * len(X))  # 80% для обучения
X_train, X_test = X[:train_size], X[train_size:]  # Обучающая и тестовая выборки
y_train, y_test = y[:train_size], y[train_size:]

# Создание сети и обучение
nn_3 = NeuralNetwork(n_neurons=3, n_inputs=6)
nn_3.fit_2(X_train, y_train, learning_rate=0.00001, epochs=100)

# Преобразуем список предсказаний в массив NumPy
predictions_1 = np.array(nn_3.predict(X_test))

# Убедитесь, что предсказания имеют правильную форму
# Преобразуем предсказания в форму (20, 3), если это необходимо
if predictions_1.ndim == 1:
    predictions_1 = predictions_1[:, np.newaxis]  # Преобразуем в 2D, если это одномерный массив

# Если у вас y_test имеет форму (20, 3), сделайте транспонирование для правильного соответствия
if predictions_1.shape[0] != y_test.shape[0]:
    predictions_1 = predictions_1.T  # Меняем форму, чтобы соответствовать (20, 3)

# Расчет MSE
mse = np.mean((predictions_1 - y_test) ** 2)

print(f"\nMSE for network: {mse}")

# Печать итоговых весов
print("\nFinal weights for network:")
for i, neuron in enumerate(nn_3.neurons):
    print(f"Weights {i + 1} нейрона: {neuron.weights}")
