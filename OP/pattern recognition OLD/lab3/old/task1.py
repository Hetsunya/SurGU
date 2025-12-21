import pandas as pd
from ultralytics import YOLO

# Параметры
test_images_path = "recog_2/"  # Путь к тестовым изображениям
results_file = "detection_results.csv"  # Имя файла для сохранения результатов


# Функция для оценки модели
def evaluate_model(model_path, model_name):
    model = YOLO(model_path)  # Загрузка модели
    results = model(test_images_path)  # Получение результатов

    # Сбор метрик
    metrics = {
        'model': model_name,
        'mAP': results[0].metrics["mAP_0.5"],  # Получение mAP (по умолчанию на IoU=0.5)
        'precision': results[0].metrics["precision"],  # Точность
        'recall': results[0].metrics["recall"]  # Полнота
    }

    return metrics


# Список моделей для тестирования
models_to_test = [
    {"path": "yolo11n.pt", "name": "Предобученная модель"},
    {"path": "yolo11n_finetuned.pt", "name": "Предобученная модель (дообученная)"},
    {"path": "new_model.pt", "name": "Новая модель (обученная)"}
]

# Сохранение результатов
results_list = []
for model in models_to_test:
    metrics = evaluate_model(model["path"], model["name"])
    results_list.append(metrics)

# Создание DataFrame и сохранение в CSV
results_df = pd.DataFrame(results_list)
results_df.to_csv(results_file, index=False)

print("Результаты сохранены в файл:", results_file)
