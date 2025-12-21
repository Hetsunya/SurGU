import cv2
import torch
from CenterNet.models import get_model
from utils.utils import load_pretrained
from utils.image import get_affine_transform, transform_preds
import numpy as np
import matplotlib.pyplot as plt

# Параметры
model_name = "resnet18"  # Можно заменить на "resnet50", "dla34" и т.д.
dataset = "coco"  # Датасет COCO
image_path = "sample.jpg"  # Путь к вашему изображению
output_dir = "output/"

# Загрузка модели
model = get_model(model_name, dataset)
model = load_pretrained(model, f"ctdet_{dataset}_{model_name}_512.pth")
model.eval()

# Загрузка изображения
img = cv2.imread(image_path)
img_h, img_w = img.shape[:2]
center = np.array([img_w / 2., img_h / 2.], dtype=np.float32)
scale = max(img_h, img_w) * 1.0
trans_input = get_affine_transform(center, scale, 0, [512, 512])

# Предобработка изображения
img = cv2.warpAffine(img, trans_input, (512, 512), flags=cv2.INTER_LINEAR)
img = img.astype(np.float32) / 255.0
img = img.transpose(2, 0, 1)  # HWC -> CHW
img = torch.from_numpy(img).float().unsqueeze(0)

# Инференс
with torch.no_grad():
    output = model(img)
    dets = output["hm"].sigmoid_()  # Heatmap с вероятностями

# Визуализация
plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
plt.title("Обнаружение объектов с CenterNet")
plt.savefig(f"{output_dir}result.jpg")
plt.show()

print("Результат сохранен в output/result.jpg")