import os
import cv2
import torch
import torchvision
from torchvision.ops import nms
from PIL import Image
import numpy as np
import selectivesearch
from torchvision.models.detection import fasterrcnn_resnet50_fpn

# Загрузка модели
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Selective Search для гипотез
def get_proposals(image_path):
    img = cv2.imread(image_path)
    img_lbl, regions = selectivesearch.selective_search(img, scale=500, sigma=0.9, min_size=10)
    proposals = []
    for r in regions:
        x, y, w, h = r['rect']
        proposals.append([x, y, x+w, y+h])
    return np.array(proposals)

# Преобразование изображения
def transform_image(image):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
    return transform(image)

# Классификация регионов
def classify_proposals(image_path, proposals):
    image = Image.open(image_path)
    transformed_image = transform_image(image).unsqueeze(0)

    predictions = []
    with torch.no_grad():
        for box in proposals:
            x1, y1, x2, y2 = map(int, box)
            cropped_img = image.crop((x1, y1, x2, y2))
            cropped_tensor = transform_image(cropped_img).unsqueeze(0)
            pred = model(cropped_tensor)
            predictions.append(pred[0])
    return predictions

# Подсчет метрик
def compute_metrics(pred_boxes, gt_boxes, iou_threshold=0.5):
    TP, FP, FN = 0, 0, 0
    matched_gt = set()

    for pred in pred_boxes:
        max_iou = 0
        max_gt_idx = -1
        for i, gt in enumerate(gt_boxes):
            iou = compute_iou(pred, gt)
            if iou > max_iou:
                max_iou = iou
                max_gt_idx = i

        if max_iou >= iou_threshold and max_gt_idx not in matched_gt:
            TP += 1
            matched_gt.add(max_gt_idx)
        else:
            FP += 1

    FN = len(gt_boxes) - len(matched_gt)
    TN = 0  # TN сложно определить без явных негативных гипотез
    return TP, FP, FN, TN

def compute_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_gt, y1_gt, x2_gt, y2_gt = box2

    xi1 = max(x1, x1_gt)
    yi1 = max(y1, y1_gt)
    xi2 = min(x2, x2_gt)
    yi2 = min(y2, y2_gt)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_gt - x1_gt) * (y2_gt - y1_gt)
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area > 0 else 0

# Папка для результатов
result_folder = "result_rcnn"
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# Путь к изображениям
image_folder = "recog_2"
image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Заглушка для ground truth (замените на реальные данные)
gt_boxes = {
    "image1.jpg": [[50, 50, 150, 150], [200, 200, 300, 300]],  # Пример
    # Добавьте аннотации для всех изображений
}

# Основной цикл
for image_path in image_paths:
    # Поиск гипотез с Selective Search
    proposals = get_proposals(image_path)
    print(f"Обработано изображение: {image_path}")
    print(f"Количество гипотез: {len(proposals)}")

    # Классификация гипотез
    predictions = classify_proposals(image_path, proposals)
    
    # Фильтрация гипотез
    final_proposals = []
    for i, pred in enumerate(predictions):
        boxes = pred['boxes'].cpu().numpy()
        scores = pred['scores'].cpu().numpy()
        labels = pred['labels'].cpu().numpy()

        cat_mask = (labels == 17) & (scores > 0.3)
        cat_boxes = boxes[cat_mask]
        cat_scores = scores[cat_mask]

        if len(cat_boxes) > 0:
            boxes_tensor = torch.tensor(cat_boxes, dtype=torch.float32)
            scores_tensor = torch.tensor(cat_scores, dtype=torch.float32)
            keep = nms(boxes_tensor, scores_tensor, iou_threshold=0.3)
            final_proposals.extend(boxes_tensor[keep].numpy() + proposals[i][:2])

    print(f"Отобрано финальных гипотез: {len(final_proposals)}")

    # Подсчет метрик
    image_name = os.path.basename(image_path)
    gt = gt_boxes.get(image_name, [])
    TP, FP, FN, TN = compute_metrics(final_proposals, gt)
    accuracy = (TP + TN) / (TP + TN + FP + FN + 1e-10)  # Избегаем деления на 0
    print(f"TP: {TP}, FP: {FP}, FN: {FN}, TN: {TN}, Accuracy: {accuracy:.4f}")

    # Отрисовка
    original_image = cv2.imread(image_path)
    for (x1, y1, x2, y2) in final_proposals:
        cv2.rectangle(original_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Сохранение результата
    result_image_path = os.path.join(result_folder, image_name)
    cv2.imwrite(result_image_path, original_image)
    print(f"Сохранено результатное изображение: {result_image_path}")