import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class Neuron:
    def __init__(self, weights, activation='sigmoid'):
        self.weights = np.array(weights, dtype=float)
        self.activation = activation
        self.output = 0
        self.delta = 0

    def predict(self, x):
        return np.dot(x, self.weights)

    def activate(self, x):
        if self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-x))
        return x

    def sigmoid_derivative(self, output):
        return output * (1 - output)

    def update_weights(self, x, learning_rate):
        self.weights += learning_rate * self.delta * np.array(x)


class NeuralNetwork:
    def __init__(self, use_random_weights=False):
        if use_random_weights:
            # Случайные веса в диапазоне [-1, 1]
            self.hidden_layer = [
                Neuron(np.random.uniform(-1, 1, 3)),
                Neuron(np.random.uniform(-1, 1, 3)),
                Neuron(np.random.uniform(-1, 1, 3))
            ]
            self.output_layer = [
                Neuron(np.random.uniform(-1, 1, 3)),
                Neuron(np.random.uniform(-1, 1, 3))
            ]
        else:
            # Фиксированные веса из задания
            self.hidden_layer = [
                Neuron([1, 4, -3]), Neuron([5, -2, 4]), Neuron([2, -3, 1])
            ]
            self.output_layer = [
                Neuron([2, 4, -2]), Neuron([-3, 2, 3])
            ]

    def feedforward(self, x):
        hidden_outputs = [neuron.activate(neuron.predict(x)) for neuron in self.hidden_layer]
        final_outputs = [neuron.activate(neuron.predict(hidden_outputs)) for neuron in self.output_layer]
        return hidden_outputs, final_outputs

    def backpropagation(self, x, y, learning_rate):
        hidden_outputs, final_outputs = self.feedforward(x)
        for i, neuron in enumerate(self.output_layer):
            error = y[i] - final_outputs[i]
            neuron.delta = error * neuron.sigmoid_derivative(final_outputs[i])
        for i, neuron in enumerate(self.hidden_layer):
            error = sum(output_neuron.delta * output_neuron.weights[i] for output_neuron in self.output_layer)
            neuron.delta = error * neuron.sigmoid_derivative(hidden_outputs[i])
        for neuron in self.output_layer:
            neuron.update_weights(hidden_outputs, learning_rate)
        for neuron in self.hidden_layer:
            neuron.update_weights(x, learning_rate)

    def fit(self, X, y, learning_rate=0.1, tolerance=1e-6, max_epochs=1000):
        for epoch in range(max_epochs):
            total_error = 0
            for i in range(len(X)):
                self.backpropagation(X[i], y[i], learning_rate)
                outputs = self.predict(X[i])
                errors = [(y[i][j] - outputs[j]) ** 2 for j in range(len(outputs))]
                total_error += sum(errors)
            mse = total_error / len(X)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, MSE: {mse}")
            if mse < tolerance:
                print(f"Training stopped at epoch {epoch} due to tolerance level.")
                break
        self.print_weights()

    def predict(self, X):
        _, final_outputs = self.feedforward(X)
        return final_outputs

    def print_weights(self):
        print("\nFinal weights after training:")
        print("Hidden layer:")
        for i, neuron in enumerate(self.hidden_layer):
            print(f"Neuron {i+1}: {neuron.weights}")
        print("Output layer:")
        for i, neuron in enumerate(self.output_layer):
            print(f"Neuron {i+1}: {neuron.weights}")


def normalize_data(y):
    y_normalized = y.copy().astype(float)
    y1_max, y2_max = y[:, 0].max(), y[:, 1].max()
    y1_min, y2_min = y[:, 0].min(), y[:, 1].min()
    y_normalized[:, 0] = (y[:, 0] - y1_min) / (y1_max - y1_min)
    y_normalized[:, 1] = (y[:, 1] - y2_min) / (y2_max - y2_min)
    return y_normalized, (y1_min, y1_max), (y2_min, y2_max)


def denormalize_predictions(predictions, y1_bounds, y2_bounds):
    y1_min, y1_max = y1_bounds
    y2_min, y2_max = y2_bounds
    return [predictions[0] * (y1_max - y1_min) + y1_min, predictions[1] * (y2_max - y2_min) + y2_min]


def calculate_accuracy(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def print_predictions(X, y_true, y_pred, y1_bounds, y2_bounds, title="Predictions"):
    mae = calculate_accuracy(y_true, y_pred)
    print(f"\n{title}:")
    print(f"MAE: {mae}")
    for i in range(min(5, len(X))):
        print(f"Input: {X[i]}, Predicted: {y_pred[i]}, Target: {y_true[i]}")
    print(f"\n{title} (denormalized):")
    for i in range(min(5, len(X))):
        pred_denorm = denormalize_predictions(y_pred[i], y1_bounds, y2_bounds)
        target_denorm = denormalize_predictions(y_true[i], y1_bounds, y2_bounds)
        print(f"Input: {X[i]}, Predicted: {pred_denorm}, Target: {target_denorm}")


# Основной код
file_path = "data/3lab_data.csv"
print(f"Loading file: {file_path}")
data = pd.read_csv(file_path, sep=',')
print("Data head:")
print(data.head())
print("Columns:", data.columns.tolist())

if len(data.columns) != 5:
    print("Incorrect column count. Assuming manual column names...")
    data.columns = ['x1', 'x2', 'x3', 'y1', 'y2']

X = data[['x1', 'x2', 'x3']].values
y = data[['y1', 'y2']].values

y_normalized, y1_bounds, y2_bounds = normalize_data(y)
X_train, X_test, y_train, y_test = train_test_split(X, y_normalized, test_size=0.2, random_state=42)
print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")

network = NeuralNetwork(use_random_weights=True)
network.print_weights()
y_pred_before = np.array([network.predict(x) for x in X_test])
print_predictions(X_test, y_test, y_pred_before, y1_bounds, y2_bounds, "Predictions before training")
network.fit(X_train, y_train, learning_rate=0.01, tolerance=1e-4, max_epochs=1000)
y_pred_after = np.array([network.predict(x) for x in X_test])
print_predictions(X_test, y_test, y_pred_after, y1_bounds, y2_bounds, "Predictions after training")