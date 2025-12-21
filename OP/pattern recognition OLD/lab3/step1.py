import os

# Установка зависимостей
os.system("pip install torch torchvision opencv-python numpy matplotlib")
os.system("pip install pycocotools")

# Клонирование репозитория CenterNet
if not os.path.exists("CenterNet"):
    os.system("git clone https://github.com/xingyizhou/CenterNet.git")

# Установка зависимостей из репозитория
os.chdir("CenterNet")
os.system("pip install -r requirements.txt")

print("Установка завершена. Репозиторий CenterNet клонирован.")