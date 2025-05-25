import numpy as np

def sigmoid(x):
    """Сигмоидная функция с ограничением для избежания переполнения."""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.uniform(-0.1, 0.1, num_inputs) 
        self.bias = np.random.uniform(-0.01, 0.01)
        self.accuracy = 1e-5

    def predict(self, x):
        """Предсказание для одного входа."""
        summator = np.dot(x, self.weights) + self.bias
        return sigmoid(summator)

    def predict_batch(self, inputs):
        """Векторизованное предсказание для батча входов."""
        summator = np.dot(inputs, self.weights) + self.bias
        return sigmoid(summator)

    def update_weights_backprop(self, x, target, learning_rate):
        """Обновление весов для одного входа."""
        x = np.array(x)
        prediction = self.predict(x)
        error = target - prediction
        gradient = error * prediction * (1 - prediction)
        self.weights += learning_rate * gradient * x
        self.bias += learning_rate * gradient

    def train(self, inputs, target, learning_rate):
        """Обучение для одного входа."""
        self.update_weights_backprop(inputs, target, learning_rate)

    def get_weights(self):
        """Получение весов и смещения."""
        return self.weights, self.bias

class NeuralNetwork:
    def __init__(self, num_neurons, num_inputs_per_neuron):
        """Инициализация сети с заданным числом нейронов."""
        self.neurons = [Neuron(num_inputs_per_neuron) for _ in range(num_neurons)]

    def predict(self, inputs):
        """Предсказание для одного входа."""
        return [neuron.predict(inputs) for neuron in self.neurons]

    def predict_batch(self, inputs):
        """Векторизованное предсказание для батча входов."""
        return np.array([neuron.predict_batch(inputs) for neuron in self.neurons]).T  # (batch_size, num_neurons)

    def train(self, training_set, learning_rate, epochs, batch_size=None):
        """Обучение сети (с или без батчей)."""
        training_set = list(training_set)  # Копируем, чтобы не менять оригинал
        for epoch in range(epochs):
            total_loss = 0.0
            np.random.shuffle(training_set)  # Перемешиваем данные
            
            if batch_size is None:
                # Одиночное обучение
                for inputs, target in training_set:
                    predictions = self.predict(inputs)
                    errors = [target - pred for pred in predictions]
                    total_loss += 0.5 * sum(error ** 2 for error in errors)
                    for neuron, error in zip(self.neurons, errors):
                        neuron.train(inputs, target, learning_rate)
            else:
                # Батчевое обучение
                for i in range(0, len(training_set), batch_size):
                    batch = training_set[i:i + batch_size]
                    batch_inputs = np.array([x for x, _ in batch])  # (batch_size, num_inputs)
                    batch_targets = np.array([t for _, t in batch])  # (batch_size,)
                    
                    # Векторизованное предсказание
                    predictions = self.predict_batch(batch_inputs)  # (batch_size, num_neurons)
                    errors = batch_targets - predictions[:, 0]  # (batch_size,)
                    total_loss += 0.5 * np.sum(errors ** 2)
                    
                    # Градиент для сигмоиды
                    gradient = errors * predictions[:, 0] * (1 - predictions[:, 0])  # (batch_size,)
                    
                    # Обновление весов и bias
                    for j in range(len(batch)):
                        self.neurons[0].weights += learning_rate * gradient[j] * batch_inputs[j]
                        self.neurons[0].bias += learning_rate * gradient[j]
            
            mse = total_loss / len(training_set)
            print(f"Epoch {epoch + 1}, Mean Squared Error: {mse}")

    def evaluate(self, test_data):
        """Оценка точности сети."""
        correct_predictions = 0
        total_samples = len(test_data)
        for inputs, target in test_data:
            predictions = self.predict(inputs)
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