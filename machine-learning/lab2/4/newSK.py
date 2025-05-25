import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Загружаем изображение
image = Image.open('kotik.jpg')
pixel_colors = np.array(image)
if pixel_colors.shape[2] == 4:  # Убираем альфа-канал, если есть
    pixel_colors = pixel_colors[:, :, :3]

# 2. Определяем целевой цвет и маску
target_color = np.array([242, 158, 194])

def is_target_color(color):
    return np.all(np.abs(color - target_color) < 1)

# Создаём маску целевого цвета
mask_target_color = np.array([[is_target_color(color) for color in row] for row in pixel_colors])
pixels_with_target_color = pixel_colors[mask_target_color]
pixels_without_target_color = pixel_colors[~mask_target_color]

# 3. Создаём датасет
df_with_target_color = pd.DataFrame(pixels_with_target_color.reshape(-1, 3), columns=['R', 'G', 'B'])
df_with_target_color['our color'] = 1
df_without_target_color = pd.DataFrame(pixels_without_target_color.reshape(-1, 3), columns=['R', 'G', 'B'])
df_without_target_color['our color'] = 0

# Балансировка данных (берём равное количество образцов)
n_samples = min(len(df_with_target_color), len(df_without_target_color))
df_with_target_color_balanced = df_with_target_color.sample(n_samples, random_state=42)
df_without_target_color_balanced = df_without_target_color.sample(n_samples, random_state=42)
training_data = pd.concat([df_with_target_color_balanced, df_without_target_color_balanced], ignore_index=True)

# Перетасовка
shuffled_training_data = training_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Нормализация
X = np.array(shuffled_training_data[['R', 'G', 'B']]) / 255.0
y = np.array(shuffled_training_data['our color'])

# Проверка баланса
print("Class balance:", np.bincount(y))

# 4. Разделяем данные
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

# 5. Обучаем модель
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# 6. Оцениваем точность
train_accuracy = accuracy_score(y_train, model.predict(X_train))
test_accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Train Accuracy: {train_accuracy * 100:.2f}%")
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# 7. Предсказываем для всего изображения
pixel_colors_normalized = pixel_colors[:, :, :3] / 255.0
height, width, _ = pixel_colors.shape
pixels_flat = pixel_colors_normalized.reshape(-1, 3)

predictions = model.predict(pixels_flat)
mask = predictions.reshape(height, width) * 255  # 0 -> 0 (чёрный), 1 -> 255 (белый)

# 8. Создаём и выводим маску
output_image = Image.fromarray(mask.astype('uint8'), mode="L")
plt.figure(figsize=(15, 10))
plt.imshow(output_image, cmap='gray')
plt.title("Predicted Target Color Pixels (White = Target, Black = Not Target)")
plt.show()

# 9. Статистика
red_count = np.sum(predictions)
non_red_count = len(predictions) - red_count
print(f"Target color pixels: {red_count}")
print(f"Non-target color pixels: {non_red_count}")

# 10. Сохраняем маску
output_image.save('predicted_mask.jpg')