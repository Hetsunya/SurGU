from ultralytics import YOLO

# Построить новую модель
model = YOLO("yolo11n.yaml")
# Загрузить предобученную модель (рекомендуется для дальнейшего обучения)
model = YOLO("yolo11n.pt")
# Обучить модель на данных датасета небольшого COCO8
results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

# Продемонстрировать обнаружение объекта на изображенях из папки с прошлой лабы
results = model(["recog_2/10.jpg", "recog_2/9.jpg"])
for result in results:
  result.show()