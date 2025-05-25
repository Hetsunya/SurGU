from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.model_zoo import model_zoo

# Настройка конфигурации
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Порог уверенности
predictor = DefaultPredictor(cfg)

import cv2
import os

image_folder = "recog_2/"  # Укажите путь к папке с изображениями
images = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.jpg', '.png'))]

import matplotlib.pyplot as plt
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

# Загрузка изображения
image = cv2.imread(images[0])  # Загрузите одно изображение
outputs = predictor(image)  # Выполнение предсказания

# Визуализация результатов
v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
annotated_image = v.draw_instance_predictions(outputs["instances"].to("cpu"))

# Отображение результата
plt.figure(figsize=(10, 10))
plt.imshow(annotated_image.get_image()[:, :, ::-1])
plt.axis('off')
plt.show()

output_folder = "output/"  # Папка для сохранения результатов
os.makedirs(output_folder, exist_ok=True)

for img_path in images:
    image = cv2.imread(img_path)
    outputs = predictor(image)

    # Визуализация
    v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    annotated_image = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    # Сохранение результата
    output_path = os.path.join(output_folder, os.path.basename(img_path))
    cv2.imwrite(output_path, annotated_image.get_image()[:, :, ::-1])