import numpy as np
import pandas as pd

class Neuron:
    def __init__(self, weights, activation='sigmoid'):
        self.weights = np.array(weights, dtype=float)
        self.activation = activation

    def predict(self, x):
        return np.dot(x, self.weights)

    def activate(self, x):
        if self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-x))
        return x


class NeuralNetwork:
    def __init__(self):
        self.hidden_layer = [
            Neuron([1, 4, -3]), Neuron([5, -2, 4]), Neuron([2, -3, 1])
        ]
        self.output_layer = [
            Neuron([2, 4, -2]), Neuron([-3, 2, 3])
        ]

    def predict(self, X):
        hidden_outputs = [neuron.activate(neuron.predict(X)) for neuron in self.hidden_layer]
        final_outputs = [neuron.activate(neuron.predict(hidden_outputs)) for neuron in self.output_layer]
        return final_outputs


# Загрузка данных
file_path = "data/3lab_data.csv"
data = pd.read_csv(file_path, sep=',')
X = data[['x1', 'x2', 'x3']].values
y = data[['y1', 'y2']].values

# Инициализация сети
network = NeuralNetwork()

# Проверка предсказаний
print("\nPredictions with specified weights:")
for i in range(min(5, len(X))):
    pred = network.predict(X[i])
    print(f"Input: {X[i]}, Predicted: {pred}, Target: {y[i]}")
