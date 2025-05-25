import numpy as np

class Neuron:
    weight: np.ndarray
    bias: float

    def __init__(self, w: np.ndarray = None, b: float = None):
        self.weight = w if w is not None else np.random.uniform(0.01, 0.09, 2)
        self.bias = b if b is not None else 1.0
        self.inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        self.test_set = np.array([0, 0, 1, 0])
        self.accuracy = 1e-2  

    def _threshold_function(self, x: float) -> int:
        return 1 if x >= 0 else 0

    def predict(self, x: np.ndarray) -> int:
        u = np.dot(x, self.weight) + self.bias
        return self._threshold_function(u)

    def train(self):
        for inputs, expected in zip(self.inputs, self.test_set):
            error = expected - self.predict(inputs)
            self.weight += self.accuracy * error * inputs
            self.bias += self.accuracy * error

    def test(self) -> bool:
        return all(self.predict(inputs) == expected for inputs, expected in zip(self.inputs, self.test_set))

    def run(self):
        print(f"Начальные веса: {self.weight}")
        print("Предсказания до обучения:")
        for inputs in self.inputs:
            print(f"Ввод: {inputs}, Предсказание: {self.predict(inputs)}")
        
        epoch = 0
        while not self.test():
            self.train()
            epoch += 1

        print(f"\nВеса после обучения: {self.weight}")
        print("Предсказания после обучения:")
        for inputs in self.inputs:
            print(f"Ввод: {inputs}, Предсказание: {self.predict(inputs)}")


neuron = Neuron()
neuron.run()
