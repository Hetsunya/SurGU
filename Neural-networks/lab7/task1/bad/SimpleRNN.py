import numpy as np


class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize network parameters
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.001
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.001
        self.Why = np.random.randn(output_size, hidden_size) * 0.001
        self.bh = np.zeros((hidden_size, 1))
        self.by = np.zeros((output_size, 1))
        self.h_prev = np.zeros((hidden_size, 1))

    def forward(self, x):
        self.h_prev = np.zeros((self.hidden_size, 1))  # Сброс состояния для каждого нового примера
        for i in range(x.shape[0]):
            # x[i] должен быть одномерным массивом с input_size элементами
            x_step = x[i].reshape(self.input_size, 1)
            self.h_next = np.tanh(np.dot(self.Wxh, x_step) + np.dot(self.Whh, self.h_prev) + self.bh)
            self.h_prev = self.h_next
        y = np.dot(self.Why, self.h_next) + self.by
        return y, self.h_next

    # def forward(self, x):
    #     # Убедитесь, что x имеет правильную форму (n_steps, input_size)
    #     for i in range(x.shape[0]):
    #         # x_step = x[i].reshape(self.input_size, 1)  # Изменяем размерность для совместимости
    #         x_step = x[i].reshape(self.input_size, 1)
    #         self.h_next = np.tanh(np.dot(self.Wxh, x_step) + np.dot(self.Whh, self.h_prev) + self.bh)
    #         self.h_prev = self.h_next  # Обновляем предыдущее состояние
    #
    #     y = np.dot(self.Why, self.h_next) + self.by
    #     return y, self.h_next

    def backward(self, x, y_true, learning_rate=0.01):
        y_pred, _ = self.forward(x.reshape(-1, self.input_size))

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

            # Обновление состояния
            self.h_prev = self.h_next

            # Обновление параметров
            # self.Wxh -= learning_rate * dWxh
            self.Wxh -= learning_rate * dWxh
            self.Whh -= learning_rate * dWhh
            self.Why -= learning_rate * dWhy
            self.bh -= learning_rate * np.sum(dbh, axis=1, keepdims=True)
            self.by -= learning_rate * np.sum(dby, axis=1, keepdims=True)

    def train(self, X_train, y_train, epochs=100, learning_rate=0.01):
        for epoch in range(epochs):
            total_loss = 0
            for i, (x, y_true) in enumerate(zip(X_train, y_train)):
                # Обеспечим, чтобы x имел форму (n_steps, input_size)
                x = x.reshape(-1, self.input_size)
                y_true = y_true.reshape(-1, 1)  # Преобразуем y_true в (output_size, 1)
                self.backward(x, y_true, learning_rate)
                y_pred, _ = self.forward(x)
                # loss = np.mean((y_pred - y_true) ** 2)
                loss = np.mean((y_pred - y_true) ** 2)

                total_loss += loss
            print(f'Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(X_train):.4f}')

    # def train(self, X_train, y_train, epochs=100, learning_rate=0.01):
    #     print(X_train)
    #     print(y_train)
    #     for epoch in range(epochs):
    #         total_loss = 0  # Переменная для суммирования потерь за эпоху
    #         for i, (x, y_true) in enumerate(zip(X_train, y_train)):
    #             self.backward(x.reshape(-1, self.input_size), y_true, learning_rate)
    #             # Прямое распространение для получения предсказания
    #             y_pred, _ = self.forward(x)
    #             # Вычисление потерь (разница между предсказанием и истинным значением)
    #             loss = np.mean((y_pred - y_true) ** 2)  # Используем среднеквадратичную ошибку
    #             total_loss += loss  # Суммируем потери за итерацию
    #             # print(f"target:{y_true}, predict{y_pred}")
    #         # Вывод информации после каждой эпохи
    #         print(f'Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(X_train):.4f}')

    def predict(self, X_test):
        predictions = []
        for x in X_test:
            y_pred, _ = self.forward(x)
            predictions.append(y_pred)
        return predictions
