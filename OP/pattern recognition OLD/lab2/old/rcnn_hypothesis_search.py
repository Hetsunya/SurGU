
import os
import cv2
import torch
import torchvision
from torchvision.ops import nms
from PIL import Image
import numpy as np
from torchvision.models.detection import fasterrcnn_resnet50_fpn


# Загрузка предобученной R-CNN модели
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Преобразование изображения в нужный формат для модели
def transform_image(image):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
    return transform(image)

# Функция для запуска R-CNN и получения гипотез
def rcnn_predict(image_path):
    image = Image.open(image_path)
    transformed_image = transform_image(image)
    transformed_image = transformed_image.unsqueeze(0)

    with torch.no_grad():
        predictions = model(transformed_image)

    return predictions[0]

# Папка для результатов
result_folder = "result_rcnn"
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# Путь к папке с изображениями
image_folder = "recog_2"
image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Основная логика
for image_path in image_paths:
    predictions = rcnn_predict(image_path)
    boxes = predictions['boxes'].cpu().numpy()  # Получение предложенных регионов
    scores = predictions['scores'].cpu().numpy()  # Уверенность для каждого региона
    labels = predictions['labels'].cpu().numpy()  # Метки классов для каждого региона

    print(f"Обработано изображение: {image_path}")
    print(f"Количество гипотез: {len(boxes)}")

    # Отбор гипотез с порогом уверенности
    threshold = 0.3
    final_boxes = boxes[scores > threshold]
    final_scores = scores[scores > threshold]
    final_labels = labels[scores > threshold]

    # Фильтрация только для искомого класса (кошка — класс 17 в COCO)
    cat_boxes = final_boxes[final_labels == 17]
    cat_scores = final_scores[final_labels == 17]

    # Применение NMS
    if len(cat_boxes) > 0:
        boxes_tensor = torch.tensor(cat_boxes, dtype=torch.float32)
        scores_tensor = torch.tensor(cat_scores, dtype=torch.float32)

        keep = nms(boxes_tensor, scores_tensor, iou_threshold=0.3)
        final_proposals = boxes_tensor[keep].numpy()
    else:
        final_proposals = []

    # Загрузка оригинального изображения для отображения
    original_image = cv2.imread(image_path)

    # Рисование рамок для каждого финального прямоугольника
    for (x1, y1, x2, y2) in final_proposals:
        cv2.rectangle(original_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Сохранение результата
    result_image_path = os.path.join(result_folder, os.path.basename(image_path))
    cv2.imwrite(result_image_path, original_image)
    print(f"Сохранено результатное изображение: {result_image_path}")
    print(f"Отобрано финальных гипотез: {len(final_proposals)}")
