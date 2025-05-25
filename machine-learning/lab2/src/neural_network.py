import numpy as np

class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.uniform(0.001, 0.02, num_inputs)  # Как в старом коде
        self.bias = np.random.uniform(-0.01, 0.01)  # Уменьшенный диапазон
        self.accuracy = 1e-5

    def predict(self, x):
        """Предсказание для одного входа (без активации для регрессии)."""
        return np.dot(x, self.weights) + self.bias

    def predict_batch(self, inputs):
        """Векторизованное предсказание для батча входов (без активации)."""
        return np.dot(inputs, self.weights) + self.bias

    def update_weights_backprop(self, x, target, learning_rate):
        """Обновление весов для текущего метода (простая регрессия)."""
        x = np.array(x)
        prediction = self.predict(x)
        error = target - prediction
        gradient = error
        self.weights += learning_rate * gradient * x
        self.bias += learning_rate * gradient

    def update_weights_1(self, x, error, learning_rate):
        """Обновление весов по формуле (1) (нормализованный градиент)."""
        self.weights += learning_rate * error * np.array(x) / np.sum(self.weights)
        self.bias += learning_rate * error

    def update_weights_2(self, x, error, learning_rate):
        """Обновление весов по формуле (4) (Уидроу-Хофф)."""
        grad = -2 * error * np.array(x)
        self.weights -= learning_rate * grad
        self.bias -= learning_rate * (-2 * error)

    def train(self, inputs, target, learning_rate):
        """Обучение для одного входа (для текущего метода)."""
        self.update_weights_backprop(inputs, target, learning_rate)

    def get_weights(self):
        """Получение весов и смещения."""
        return self.weights, self.bias

class NeuralNetwork:
    def __init__(self, num_neurons, num_inputs_per_neuron):
        """Инициализация сети."""
        self.neurons = [Neuron(num_inputs_per_neuron) for _ in range(num_neurons)]

    def predict(self, inputs):
        """Предсказание для одного входа."""
        return [neuron.predict(inputs) for neuron in self.neurons]

    def predict_batch(self, inputs):
        """Векторизованное предсказание для батча входов."""
        return np.array([neuron.predict_batch(inputs) for neuron in self.neurons]).T  # (batch_size, num_neurons)

    def train(self, training_set, learning_rate, epochs, batch_size=None):
        """Обучение сети (текущий метод)."""
        training_set = list(training_set)
        for epoch in range(epochs):
            total_loss = 0.0
            np.random.shuffle(training_set)
            
            if batch_size is None:
                for inputs, target in training_set:
                    predictions = self.predict(inputs)
                    errors = [target - pred for pred in predictions]
                    total_loss += 0.5 * sum(error ** 2 for error in errors)
                    for neuron, error in zip(self.neurons, errors):
                        neuron.train(inputs, target, learning_rate)
            else:
                for i in range(0, len(training_set), batch_size):
                    batch = training_set[i:i + batch_size]
                    batch_inputs = np.array([x for x, _ in batch])
                    batch_targets = np.array([t for _, t in batch])
                    predictions = self.predict_batch(batch_inputs)
                    errors = batch_targets - predictions[:, 0]
                    total_loss += 0.5 * np.sum(errors ** 2)
                    gradient = errors
                    for j in range(len(batch)):
                        self.neurons[0].weights += learning_rate * gradient[j] * batch_inputs[j]
                        self.neurons[0].bias += learning_rate * gradient[j]
            
            # mse = total_loss / len(training_set)
            # print(f"Epoch {epoch + 1}, Mean Squared Error: {mse}")

    def fit_1(self, X, y, learning_rate=0.00001, epochs=200):
        """Обучение по формуле (1)."""
        for epoch in range(epochs):
            total_error = 0
            for i in range(len(X)):
                for neuron, target in zip(self.neurons, [y[i]]):
                    output = neuron.predict(X[i])
                    error = target[0] - output  # y[i] — массив, берём первый элемент
                    neuron.update_weights_1(X[i], error, learning_rate)
                    total_error += error ** 2
            # mse = total_error / len(X)
            # print(f"Epoch {epoch + 1}, Mean Squared Error: {mse}")

    def fit_2(self, X, y, learning_rate=0.000001, epochs=200):
        """Обучение по формуле (4)."""
        for epoch in range(epochs):
            total_error = 0
            for i in range(len(X)):
                for neuron, target in zip(self.neurons, [y[i]]):
                    output = neuron.predict(X[i])
                    error = target[0] - output  # y[i] — массив, берём первый элемент
                    neuron.update_weights_2(X[i], error, learning_rate)
                    total_error += error ** 2
            # mse = total_error / len(X)
            # print(f"Epoch {epoch + 1}, Mean Squared Error: {mse}")

    def evaluate(self, test_data):
        """Оценка MSE на тестовых данных."""
        total_loss = 0.0
        for inputs, target in test_data:
            predictions = self.predict(inputs)
            errors = [target - pred for pred in predictions]
            total_loss += 0.5 * sum(error ** 2 for error in errors)
        mse = total_loss / len(test_data)
        print(f"Mean Squared Error: {mse}")
        return mse

def split_data(data, train_fraction):
    """Разделяет данные на тренировочные и тестовые."""
    num_samples = len(data)
    train_size = int(train_fraction * num_samples)
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data