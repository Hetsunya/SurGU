from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from src.neuron import Neuron

class RedDetectionNeuron(Neuron):
    def predict(self, x):
        return 1 if super().predict(x) > 0.5 else 0

    # Открытие изображения
image = Image.open('data/pic.jpg')
a = np.asarray(image)

# Создание нейрона для распознавания красного
red_neuron = RedDetectionNeuron(3)

# Примерные данные для обучения (можно обучить на большее количество пикселей)
pixels = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]  # RGB цвета
labels = [1, 0, 0]  # Красный цвет как 1, другие как 0

# Обучение нейрона
for _ in range(10000):
    for pixel, label in zip(pixels, labels):
        output = red_neuron.predict(pixel)
        error = label - output
        red_neuron.update_weights_1(pixel, error, learning_rate=0.00001)

# Прогнозирование на пикселях изображения
reshaped_a = a.reshape(-1, 3)
result = [red_neuron.predict(pixel) for pixel in reshaped_a]

# Отображение результата
res_image = np.array(result).reshape(a.shape[:2])
plt.imshow(res_image, cmap='gray')
plt.show()
