import os
import cv2
import torch
import torchvision
from torchvision import transforms
from torchvision.ops import nms
from PIL import Image
import numpy as np
import pandas as pd

# Загрузка предобученной модели (например, ResNet)
model = torchvision.models.resnet50(weights=torchvision.models.ResNet50_Weights.IMAGENET1K_V1)
model.eval()

# Преобразование изображений для модели
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Функция для классификации с получением вероятностей
def classify(image):
    img_tensor = preprocess(image)
    img_tensor = img_tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top_prob, predicted = torch.max(probabilities, 0)
    return predicted.item(), top_prob.item()

# Функция для Selective Search
def selective_search(image_path):
    image = cv2.imread(image_path)
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(image)
    ss.switchToSingleStrategy()
    rects = ss.process()  # Возвращает список прямоугольников
    return image, rects

# Папка для результатов
result_folder = "result"
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# Путь к папке с изображениями
image_folder = "recog_2"
image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Список для хранения результатов
results = []

# Основная логика
for image_path in image_paths:
    image, proposals = selective_search(image_path)
    print(f"Обработано изображение: {image_path}")
    print(f"Количество гипотез: {len(proposals)}")

    filtered_proposals = []
    threshold = 0.3  # Порог уверенности классификации

    # Инициализация счетчиков
    TP, TN, FP, FN = 0, 0, 0, 0  # True Positives, True Negatives, False Positives, False Negatives

    # Обработка каждого прямоугольника
    for (x, y, w, h) in proposals:
        proposal_img = image[y:y+h, x:x+w]
        proposal_pil = Image.fromarray(cv2.cvtColor(proposal_img, cv2.COLOR_BGR2RGB))
        class_id, confidence = classify(proposal_pil)

        # Проверяем, превышает ли уверенность порог и является ли это нужным классом
        if class_id == 281:  # 281 - ID кошки в ImageNet
            if confidence > threshold:
                filtered_proposals.append((x, y, w, h, confidence))
                TP += 1  # Правильное положительное
            else:
                FN += 1  # Пропуск объекта
        else:
            FP += 1  # Ложное положительное

    # Применяем Non-Maximum Suppression (NMS)
    if filtered_proposals:
        boxes = torch.tensor([[x, y, x + w, y + h] for (x, y, w, h, conf) in filtered_proposals], dtype=torch.float32)
        scores = torch.tensor([conf for (x, y, w, h, conf) in filtered_proposals], dtype=torch.float32)

        keep = nms(boxes, scores, iou_threshold=0.3)  # Применение NMS с порогом IoU
        final_proposals = [filtered_proposals[i] for i in keep]
    else:
        final_proposals = []

    # Рисуем рамки для всех гипотез с подписью confidence
    for (x, y, w, h, conf) in final_proposals:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = f"{conf:.2f}"
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Сохраняем результатное изображение
    result_image_path = os.path.join(result_folder, os.path.basename(image_path))
    cv2.imwrite(result_image_path, image)
    print(f"Сохранено результатное изображение: {result_image_path}")
    print(f"Отобрано финальных гипотез: {len(final_proposals)}")

    # Подсчет общего количества объектов и Accuracy
    total_objects = TP + FN  # Общее количество объектов на изображении
    accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0

    # Сохранение результатов для текущего изображения
    results.append({
        'Image': os.path.basename(image_path),
        'Total Proposals': len(proposals),
        'Filtered Proposals': len(final_proposals),
        'TP': TP,
        'TN': TN,
        'FP': FP,
        'FN': FN,
        'Accuracy': accuracy
    })

# Создание DataFrame и сохранение в CSV
results_df = pd.DataFrame(results)
csv_file_path = os.path.join(result_folder, 'results.csv')
results_df.to_csv(csv_file_path, index=False)
print(f"Результаты сохранены в {csv_file_path}")
