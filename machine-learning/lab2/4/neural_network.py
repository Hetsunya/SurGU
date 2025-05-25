import numpy as np

def sigmoid(x):
    """Сигмоидная функция с ограничением для избежания переполнения."""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.uniform(-1, 1, num_inputs)
        self.bias = np.random.uniform(-0.1, 0.1)
        self.accuracy = 1e-5

    def predict(self, x):
        summator = np.dot(x, self.weights) + self.bias
        return sigmoid(summator)

    def update_weights_backprop(self, x, target, learning_rate):
        x = np.array(x)
        prediction = self.predict(x)
        error = target - prediction
        gradient = error * prediction * (1 - prediction)
        self.weights += learning_rate * gradient * x
        self.bias += learning_rate * gradient

    def train(self, inputs, target, learning_rate):
        self.update_weights_backprop(inputs, target, learning_rate)

    def get_weights(self):
        return self.weights, self.bias

class NeuralNetwork:
    def __init__(self, num_neurons, num_inputs_per_neuron):
        self.neurons = [Neuron(num_inputs_per_neuron) for _ in range(num_neurons)]

def create_neural_network(num_neurons, num_inputs_per_neuron):
    """Создаёт нейронную сеть."""
    return NeuralNetwork(num_neurons, num_inputs_per_neuron)

def train_neural_network(neural_net, training_set, learning_rate, epochs):
    """Обучает нейронную сеть."""
    for epoch in range(epochs):
        total_loss = 0.0
        for inputs, target in training_set:
            predictions = [neuron.predict(inputs) for neuron in neural_net.neurons]
            errors = [target - prediction for prediction in predictions]
            total_loss += 0.5 * sum(error ** 2 for error in errors)
            for neuron, error in zip(neural_net.neurons, errors):
                neuron.train(inputs, target, learning_rate)
        mse = total_loss / len(training_set)
        print(f"Epoch {epoch + 1}, Mean Squared Error: {mse}")

def evaluate_neural_network(neural_net, test_data):
    """Оценивает точность нейронной сети."""
    correct_predictions = 0
    total_samples = len(test_data)
    for inputs, target in test_data:
        predictions = [neuron.predict(inputs) for neuron in neural_net.neurons]
        predicted_class = 1 if np.mean(predictions) > 0.5 else 0
        if predicted_class == target:
            correct_predictions += 1
    accuracy = correct_predictions / total_samples
    print(f"Accuracy: {accuracy * 100:.2f}%")
    return accuracy

def split_data(data, train_fraction):
    """Разделяет данные на тренировочные и тестовые."""
    num_samples = len(data)
    train_size = int(train_fraction * num_samples)
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data