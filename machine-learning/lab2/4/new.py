import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# Сигмоидная функция
def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Ограничение для избежания переполнения

class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.uniform(-1, 1, num_inputs)
        self.bias = np.random.uniform(-0.1, 0.1)  # Увеличим диапазон bias
        self.accuracy = 1e-5

    def predict(self, x):
        summator = np.dot(x, self.weights) + self.bias
        return sigmoid(summator)  # Применяем сигмоиду

    def update_weights_backprop(self, x, target, learning_rate):
        x = np.array(x)
        prediction = self.predict(x)
        error = target - prediction
        # Градиент для сигмоиды: error * prediction * (1 - prediction)
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
    return NeuralNetwork(num_neurons, num_inputs_per_neuron)

def train_neural_network(neural_net, training_set, learning_rate, epochs):
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
    correct_predictions = 0
    total_samples = len(test_data)
    for inputs, target in test_data:
        predictions = [neuron.predict(inputs) for neuron in neural_net.neurons]
        predicted_class = 1 if np.mean(predictions) > 0.5 else 0  # Порог 0.5 для сигмоиды
        if predicted_class == target:
            correct_predictions += 1
    accuracy = correct_predictions / total_samples
    print(f"Accuracy: {accuracy * 100:.2f}%")
    return accuracy

def split_data(data, train_fraction):
    num_samples = len(data)
    train_size = int(train_fraction * num_samples)
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data

# Подготовка данных
image = Image.open('kotik.jpg')
pixel_colors = np.array(image)
if pixel_colors.shape[2] == 4:
    pixel_colors = pixel_colors[:, :, :3]

target_color = np.array([242, 158, 194])

def is_target_color(color):
    return np.all(np.abs(color - target_color) < 20)

mask_target_color = np.array([[is_target_color(color) for color in row] for row in pixel_colors])
pixels_with_target_color = pixel_colors[mask_target_color]
pixels_without_target_color = pixel_colors[~mask_target_color]

# Создание датасета
df_with_target_color = pd.DataFrame(pixels_with_target_color.reshape(-1, 3), columns=['R', 'G', 'B'])
df_with_target_color['our color'] = 1
df_without_target_color = pd.DataFrame(pixels_without_target_color.reshape(-1, 3), columns=['R', 'G', 'B'])
df_without_target_color['our color'] = 0

# Балансировка
n_samples = min(len(df_with_target_color), len(df_without_target_color))
df_with_target_color_balanced = df_with_target_color.sample(n_samples, random_state=42)
df_without_target_color_balanced = df_without_target_color.sample(n_samples, random_state=42)
training_data = pd.concat([df_with_target_color_balanced, df_without_target_color_balanced], ignore_index=True)
shuffled_training_data = training_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Нормализация
shuffled_training_data_array = np.array(shuffled_training_data[['R', 'G', 'B']]) / 255.0
target_labels = np.array(shuffled_training_data['our color'])

print("Class balance:", np.bincount(target_labels))

# Разделение данных
train_data, test_data = split_data(list(zip(shuffled_training_data_array, target_labels)), train_fraction=0.8)

# Обучение
neural_net = create_neural_network(1, 3)
print("Initial Weights:", neural_net.neurons[0].weights)
print("Initial Bias:", neural_net.neurons[0].bias)

evaluate_neural_network(neural_net, test_data)
evaluate_neural_network(neural_net, train_data)

train_neural_network(neural_net, train_data, learning_rate=0.01, epochs=50)  # Увеличили learning_rate и epochs

print("Trained Weights:", neural_net.neurons[0].weights)
print("Trained Bias:", neural_net.neurons[0].bias)
evaluate_neural_network(neural_net, test_data)
evaluate_neural_network(neural_net, train_data)

# Визуализация
pixel_colors_normalized = pixel_colors / 255.0
height, width, _ = pixel_colors.shape
pixels_flat = pixel_colors_normalized.reshape(-1, 3)

predictions = []
for pixel in pixels_flat:
    pred = neural_net.neurons[0].predict(pixel)
    pred_class = 1 if pred > 0.5 else 0  # Порог 0.5 для сигмоиды
    predictions.append(pred_class)

mask = np.array(predictions, dtype='uint8') * 255
mask = mask.reshape(height, width)

output_image = Image.fromarray(mask, mode="L")
plt.figure(figsize=(15, 10))
plt.imshow(output_image, cmap='gray')
plt.title("Predicted Target Color Pixels (White = Target, Black = Not Target)")
plt.show()

red_count = np.sum(predictions)
non_red_count = len(predictions) - red_count
print(f"Target color pixels: {red_count}")
print(f"Non-target color pixels: {non_red_count}")

output_image.save('predicted_mask_neural_net.jpg')