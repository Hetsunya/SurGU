from ultralytics import YOLO

# Параметры
data_yaml = "coco8.yaml"  # Путь к файлу данных для обучения
epochs = 100  # Количество эпох
imgsz = 640  # Размер изображений
new_model_path = "new_model.pt"  # Путь для сохранения новой модели
finetuned_model_path = "yolo11n_finetuned.pt"  # Путь для сохранения дообученной модели


# 1. Обучение новой модели
def train_new_model():
    model = YOLO("yolo11n.yaml")  # Создание новой модели
    results = model.train(data=data_yaml, epochs=epochs, imgsz=imgsz)

    if results:
        # Проверка на наличие результатов
        try:
            model.save(new_model_path)  # Сохранение обученной модели
            print("Новая модель обучена и сохранена по пути:", new_model_path)
        except Exception as e:
            print("Ошибка при сохранении новой модели:", e)
    else:
        print("Не удалось обучить новую модель. Проверьте данные.")


# 2. Обучение предобученной модели (дообучение)
def finetune_pretrained_model():
    model = YOLO("yolo11n.pt")  # Загрузка предобученной модели
    results = model.train(data=data_yaml, epochs=epochs, imgsz=imgsz)

    if results:
        try:
            model.save(finetuned_model_path)  # Сохранение дообученной модели
            print("Предобученная модель дообучена и сохранена по пути:", finetuned_model_path)
        except Exception as e:
            print("Ошибка при сохранении дообученной модели:", e)
    else:
        print("Не удалось дообучить предобученную модель. Проверьте данные.")


# 3. Обучение предобученной модели без дообучения (просто загрузка)
def load_pretrained_model():
    model = YOLO("yolo11n.pt")  # Загрузка предобученной модели
    print("Предобученная модель загружена, но не обучалась.")
    return model


# Запуск обучения
if __name__ == "__main__":
    train_new_model()  # Обучаем новую модель
    finetune_pretrained_model()  # Дообучаем предобученную модель
    load_pretrained_model()  # Загружаем предобученную модель без обучения
