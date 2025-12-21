import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.filters import gaussian
from skimage.segmentation import active_contour

img = imread('img.png')
# img = rgb2gray(img)

s = np.linspace(0, 2 * np.pi, 200)
r = 140 + 75 * np.sin(s)
c = 140 + 75 * np.cos(s)
init = np.array([r, c]).T

snake = active_contour(
    gaussian(img, sigma=6, preserve_range=False),
    init,
    alpha=0.015,
    beta=0.1,
    gamma=0.015,
)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(img, cmap=plt.cm.gray)
ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img.shape[1], img.shape[0], 0])

plt.show()
