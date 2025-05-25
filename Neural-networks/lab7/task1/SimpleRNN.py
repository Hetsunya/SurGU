import numpy as np


class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # # Initialize network parameters
        # self.Wxh = np.random.randn(hidden_size, input_size) * 0.001
        # self.Whh = np.random.randn(hidden_size, hidden_size) * 0.001
        # self.Why = np.random.randn(output_size, hidden_size) * 0.001
        # self.bh = np.zeros((hidden_size, 1))
        # self.by = np.zeros((output_size, 1))
        # self.h_prev = np.zeros((hidden_size, 1))
        # Инициализация параметров сети
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.001  # Вес от входа к скрытому слою
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.001  # Вес между скрытыми состояниями
        self.Why = np.random.randn(output_size, hidden_size) * 0.001  # Вес от скрытого слоя к выходу
        self.bh = np.zeros((hidden_size, 1))  # Смещение скрытого слоя
        self.by = np.zeros((output_size, 1))  # Смещение выходного слоя
        self.h_prev = np.zeros((hidden_size, 1))  # Начальное скрытое состояние

    def forward(self, x):
        for i in range(x.shape[0]):
            x_step = x[i].reshape(self.input_size, 1)  # Преобразуем шаг входных данных в столбец
            self.h_next = np.tanh(np.dot(self.Wxh, x_step) + np.dot(self.Whh, self.h_prev) + self.bh)
            self.h_prev = self.h_next  # Обновляем предыдущее скрытое состояние

        y = np.dot(self.Why, self.h_next) + self.by  # Прогноз на основе последнего скрытого состояния
        return y, self.h_next

    def backward(self, x, y_true, learning_rate=0.01):
        # Прямое распространение
        y_pred, _ = self.forward(x)

        # Обратное распространение
        dy = y_pred - y_true
        dWhy = np.dot(dy, self.h_next.T)
        dby = dy
        dh_next = np.dot(self.Why.T, dy)

        for i in reversed(range(x.shape[0])):
            x_step = x[i].reshape(self.input_size, 1)
            dh_raw = (1 - self.h_next * self.h_next) * dh_next
            dbh = dh_raw
            dWxh = np.dot(dh_raw, x_step.T)
            dWhh = np.dot(dh_raw, self.h_prev.T)
            self.h_prev = self.h_next  # Обновляем состояние

            # Обновление параметров
            self.Wxh -= learning_rate * dWxh
            self.Whh -= learning_rate * dWhh
            self.Why -= learning_rate * dWhy
            self.bh -= learning_rate * np.sum(dbh, axis=1, keepdims=True)
            self.by -= learning_rate * np.sum(dby, axis=1, keepdims=True)

    def train(self, X_train, y_train, epochs=100, learning_rate=0.01):
        print(X_train)
        print(y_train)
        for epoch in range(epochs):
            total_loss = 0  # Переменная для суммирования потерь за эпоху
            for i, (x, y_true) in enumerate(zip(X_train, y_train)):
                self.backward(x, y_true, learning_rate)
                # Прямое распространение для получения предсказания
                y_pred, _ = self.forward(x)
                # Вычисление потерь (разница между предсказанием и истинным значением)
                loss = np.mean((y_pred - y_true) ** 2)  # Используем среднеквадратичную ошибку
                total_loss += loss  # Суммируем потери за итерацию
                # print(f"target:{y_true}, predict{y_pred}")
            # Вывод информации после каждой эпохи
            print(f'Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(X_train):.4f}')

    def predict(self, X_test):
        predictions = []
        for x in X_test:
            y_pred, _ = self.forward(x)
            predictions.append(y_pred)
        return predictions