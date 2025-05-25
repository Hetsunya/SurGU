import cv2
import numpy as np
import os
from scipy.signal import convolve2d

POOL_SIZE = 2

image = cv2.imread("img.jpeg", cv2.IMREAD_GRAYSCALE)

padded_image = np.pad(image, ((1, 1), (1, 1)), mode='constant', constant_values=0)

kernel_zeros = np.zeros([3, 3])

kernel_ones = np.ones((3, 3))

kernel_custom = np.array([[1, 0, -1],
                          [2, 0, -2],
                          [1, 0, -1]])

def median_pooling(image, pool_size=POOL_SIZE):
    pooled_image = np.zeros((image.shape[0] // pool_size, image.shape[1] // pool_size), dtype=np.uint8)
    for i in range(0, image.shape[0] // pool_size * pool_size, pool_size):
        for j in range(0, image.shape[1] // pool_size * pool_size, pool_size):
            pooled_image[i // pool_size, j // pool_size] = np.median(image[i:i+pool_size, j:j+pool_size])
    return pooled_image

convolved_zeros = convolve2d(padded_image, kernel_zeros, mode='valid')
convolved_ones = convolve2d(padded_image, kernel_ones, mode='valid')
convolved_custom = convolve2d(padded_image, kernel_custom, mode='valid')
pooled_image = median_pooling(image)


# Сохранение результатов
output_folder = "convolution_results"
os.makedirs(output_folder, exist_ok=True)

cv2.imwrite(os.path.join(output_folder, "convolved_zeros.png"), convolved_zeros)
cv2.imwrite(os.path.join(output_folder, "convolved_ones.png"), convolved_ones)
cv2.imwrite(os.path.join(output_folder, "convolved_custom.png"), convolved_custom)
cv2.imwrite(os.path.join(output_folder, "pooled_image.png"), pooled_image)

print("Исходное изображение:")
print(image, image.shape)
print("Свертка с ядром, заполненным нулями:")
print(convolved_zeros, convolved_zeros.shape)
print("\nСвертка с ядром, заполненным единицами:")
print(convolved_ones, convolved_ones.shape)
print("\nСвертка с произвольным ядром:")
print(convolved_custom, convolved_custom.shape)
print(f"\nПулинг с медианным окном {POOL_SIZE}x{POOL_SIZE}:")
print(pooled_image, pooled_image.shape)
