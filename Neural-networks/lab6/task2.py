import os
import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

data_dir = "data6"
target_size = (150, 150)
batch_size = 32
epochs = 10

def load_data(data_dir, target_size):
    images = []
    labels = []
    
    for folder_name in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
            
        for file_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, file_name)
            
            with Image.open(image_path) as image:
                image = image.convert('L')  # Преобразуем в grayscale
                image = image.resize(target_size)
                img_array = img_to_array(image)
                images.append(img_array)
                
                if folder_name == "6":
                    labels.append(1)  # Ваш вариант
                else:
                    labels.append(0)  # Не ваш вариант
    
    images = np.array(images) / 255.0
    labels = np.array(labels)
    
    return images, labels

print("Загрузка данных...")
images, labels = load_data(data_dir, target_size)

print("Форма изображений:", images.shape)

X_train, X_val, y_train, y_val = train_test_split(
    images, labels, test_size=0.2, random_state=42
)

model = Sequential([
    Input(shape=(target_size[0], target_size[1], 1)),
    Conv2D(8, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=0.001),
    metrics=['accuracy']
)

history = model.fit(
    X_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(X_val, y_val)
)

loss, accuracy = model.evaluate(X_val, y_val)
print("Потери:", loss)
print("Точность:", accuracy)

result_dir = "result"
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

# Сохраняем результаты для валидационной выборки
print("Сохранение результатов...")
predictions = model.predict(X_val)

for i in range(len(X_val)):
    image = X_val[i]
    true_label = "Ваш вариант" if y_val[i] == 1 else "Не ваш вариант"
    predicted_label = "Ваш вариант" if predictions[i][0] > 0.5 else "Не ваш вариант"
    
    plt.imshow(image.squeeze(), cmap='gray')  # Используем squeeze для удаления канала и cmap='gray' для монохромных изображений
    plt.title(f"True: {true_label}, Predicted: {predicted_label}")
    plt.savefig(f"{result_dir}/test_result_{i}.png")
    plt.close()

print(f"Результаты работы модели сохранены в файлы в папке '{result_dir}'")