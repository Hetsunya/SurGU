import cv2
import selectivesearch
import numpy as np
import os
from torchvision import models, transforms
import torch
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Папки для входных и выходных данных
image_folder = "recog_2/"
output_folder = "output/"
os.makedirs(output_folder, exist_ok=True)

# Загрузка изображений
image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.jpg', '.png'))]

# Загрузка предобученной модели ResNet50
model = models.resnet50(pretrained=True)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Преобразование изображений для классификации
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Функция для классификации региона (кот или не кот)
def classify_region(region, threshold=0.5):
    region = cv2.resize(region, (224, 224))
    input_tensor = preprocess(region).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.softmax(output, dim=1)
        # Предполагаем, что класс "кот" — это класс 281 в ImageNet
        cat_prob = probs[0, 281].item()
    return cat_prob > threshold, cat_prob

# Функция для обработки одного изображения
def process_image(img_path):
    # Загрузка изображения
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Selective Search
    img_lbl, regions = selectivesearch.selective_search(img_rgb, scale=500, sigma=0.9, min_size=10)
    proposals = []
    for r in regions:
        x, y, w, h = r['rect']
        if w > 20 and h > 20:  # Фильтрация слишком маленьких регионов
            proposals.append((x, y, x + w, y + h))

    print(f"Изображение: {img_path}")
    print(f"Количество гипотез (Positive): {len(proposals)}")
    print(f"Количество отсеянных гипотез (Negative): {len(regions) - len(proposals)}")

    # Классификация гипотез и отрисовка рамок
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0
    cat_boxes = []

    for (x_min, y_min, x_max, y_max) in proposals:
        region = img_rgb[y_min:y_max, x_min:x_max]
        is_cat, prob = classify_region(region)
        # Предполагаем, что на изображении есть кот (упрощение)
        # В реальной задаче: проверьте, пересекается ли гипотеза с ground truth bounding box
        # Например, используйте IoU для сравнения с разметкой из COCO/VOC
        ground_truth = True  # Замените на проверку с реальной разметкой
        if is_cat and ground_truth:
            true_positives += 1
            cat_boxes.append((x_min, y_min, x_max, y_max, prob))
        elif is_cat and not ground_truth:
            false_positives += 1
        elif not is_cat and ground_truth:
            false_negatives += 1
        elif not is_cat and not ground_truth:
            true_negatives += 1

    # Отрисовка рамок и вероятностей на изображении
    img_with_boxes = img.copy()
    for (x_min, y_min, x_max, y_max, prob) in cat_boxes:
        # Рисуем зеленый прямоугольник
        cv2.rectangle(img_with_boxes, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        # Добавляем текст с вероятностью
        text = f"{prob:.2f}"
        cv2.putText(img_with_boxes, text, (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Сохранение результата
    output_path = os.path.join(output_folder, f"result_{os.path.basename(img_path)}")
    cv2.imwrite(output_path, img_with_boxes)
    print(f"Сохранено изображение с рамками: {output_path}")

    # Вывод таблицы ошибок
    print("Таблица ошибок:")
    print(f"True Positives (TP): {true_positives}")
    print(f"False Positives (FP): {false_positives}")
    print(f"False Negatives (FN): {false_negatives}")
    print(f"True Negatives (TN): {true_negatives}")
    total = true_positives + false_positives + false_negatives + true_negatives
    accuracy = (true_positives + true_negatives) / total if total > 0 else 0
    print(f"Accuracy: {accuracy:.4f}\n")

    return true_positives, false_positives, false_negatives, true_negatives

# Обработка всех изображений
total_tp, total_fp, total_fn, total_tn = 0, 0, 0, 0
for img_path in image_paths[:10]:  # Ограничиваем 10 изображениями
    tp, fp, fn, tn = process_image(img_path)
    total_tp += tp
    total_fp += fp
    total_fn += fn
    total_tn += tn

# Итоговые результаты
print("Итоговые результаты по всем изображениям:")
print(f"Total True Positives (TP): {total_tp}")
print(f"Total False Positives (FP): {total_fp}")
print(f"Total False Negatives (FN): {total_fn}")
print(f"Total True Negatives (TN): {total_tn}")
total = total_tp + total_fp + total_fn + total_tn
accuracy = (total_tp + total_tn) / total if total > 0 else 0
print(f"Total Accuracy: {accuracy:.4f}")