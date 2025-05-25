import pyautogui
import time

# Задаем интервал между скриншотами (в секундах)
interval = 10

# Задаем количество скриншотов, которые нужно сделать
num_screenshots = 7

# Переменная-счетчик для номерации скриншотов
count = 1

# Цикл для создания серии скриншотов
while count <= num_screenshots:
    # Отображаем текущее время перед созданием скриншота
    print("Создание скриншота", count, "в", time.strftime("%H:%M:%S"))

    # Создаем скриншот и сохраняем его в файл
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot_" + str(count) + ".png")

    # Увеличиваем счетчик
    count += 1

    # Ждем указанный интервал времени
    time.sleep(interval)