from .neuron import Neuron


class NeuralNetwork:
    def __init__(self, n_neurons, n_inputs):
        self.neurons = [Neuron(n_inputs) for _ in range(n_neurons)]

    def predict(self, x):
        return [neuron.predict(x) for neuron in self.neurons]

    # Обучение по формуле (1)
    def fit_1(self, X, y, learning_rate=0.001, epochs=100):
        print(len(X))
        print(len(y))
        print(X)
        print(y)
        for epoch in range(epochs):
            total_error = 0
            for i in range(len(X)):
                for neuron, target in zip(self.neurons, y[i]):
                    output = neuron.predict(X[i])
                    error = target - output
                    neuron.update_weights_1(X[i], error, learning_rate)
                    total_error += error**2
            #     print(f"i = {i}", f'Epoch {epoch+1}, Total Error: {total_error}', f"Error {error}",
            #           f"Веса {neuron.weights}", f"Предикт {output}", f"Таргет {target}" )
            # # Общий вывод по эпохе
            # print(f"Epoch {epoch+1}, Total Error: {total_error}")

    # Обучение по формуле (4)
    def fit_2(self, X, y, learning_rate=0.000001, epochs=1000):
        for epoch in range(epochs):
            total_error = 0
            for i in range(len(X)):
                for j, neuron in enumerate(self.neurons):
                    output = neuron.predict(X[i])
                    error = y[i][j] - output  # Используем целевое значение для конкретного нейрона
                    neuron.update_weights_2(X[i], error, learning_rate)
                    total_error += error ** 2
                    print(f"i = {i}", f'Epoch {epoch + 1}, Total Error: {total_error}',
                          f"Error {error}", f"Веса {neuron.weights}",
                          f"Предикт {output}", f"Таргет {y[i][j]}")
            # Общий вывод по эпохе
            print(f"Epoch {epoch+1}, Total Error: {total_error}")
