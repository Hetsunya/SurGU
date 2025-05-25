import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from neural_network import create_neural_network, train_neural_network, evaluate_neural_network, split_data

# 1. Загружаем изображение
image = Image.open('kotik.jpg')
pixel_colors = np.array(image)
if pixel_colors.shape[2] == 4:
    pixel_colors = pixel_colors[:, :, :3]

# 2. Определяем целевой цвет
target_color = np.array([242, 158, 194])

def is_target_color(color):
    return np.all(np.abs(color - target_color) < 20)

# 3. Создаём маску целевого цвета
mask_target_color = np.array([[is_target_color(color) for color in row] for row in pixel_colors])
pixels_with_target_color = pixel_colors[mask_target_color]
pixels_without_target_color = pixel_colors[~mask_target_color]

# 4. Создаём датасет
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

# 5. Разделение данных
train_data, test_data = split_data(list(zip(shuffled_training_data_array, target_labels)), train_fraction=0.8)

# 6. Обучение
neural_net = create_neural_network(1, 3)
print("Initial Weights:", neural_net.neurons[0].weights)
print("Initial Bias:", neural_net.neurons[0].bias)

evaluate_neural_network(neural_net, test_data)
evaluate_neural_network(neural_net, train_data)

train_neural_network(neural_net, train_data, learning_rate=0.01, epochs=50)

print("Trained Weights:", neural_net.neurons[0].weights)
print("Trained Bias:", neural_net.neurons[0].bias)
evaluate_neural_network(neural_net, test_data)
evaluate_neural_network(neural_net, train_data)

# 7. Визуализация
pixel_colors_normalized = pixel_colors / 255.0
height, width, _ = pixel_colors.shape
pixels_flat = pixel_colors_normalized.reshape(-1, 3)

predictions = []
for pixel in pixels_flat:
    pred = neural_net.neurons[0].predict(pixel)
    pred_class = 1 if pred > 0.5 else 0
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