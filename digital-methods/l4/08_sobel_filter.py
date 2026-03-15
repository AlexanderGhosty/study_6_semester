import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

image = cv2.imread('input.jpg')
if image is None: raise RuntimeError("Could not open input.jpg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
filtered_image_x = cv2.filter2D(gray_image, -1, sobel_x)
sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
filtered_image_y = cv2.filter2D(gray_image, -1, sobel_y)
edge_image = cv2.addWeighted(filtered_image_x, 0.5, filtered_image_y, 0.5, 0)

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(12, 6), dpi=100)
plt.subplot(1,2,1), plt.imshow(rgb_image)
plt.title('Исходное изображение'), plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2), plt.imshow(edge_image, cmap='gray')
plt.title('Фильтрованное изображение'), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.savefig('result_08.png', bbox_inches='tight')
print("08_sobel_filter.py completed")
