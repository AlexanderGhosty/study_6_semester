import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

image = cv2.imread('input.jpg')
if image is None: raise RuntimeError("Could not open input.jpg")
kernel_size = (15, 15)
sigma = 0.0
kernel = cv2.getGaussianKernel(kernel_size[0], sigma)
gaussian_kernel = np.outer(kernel, kernel)
blurred_image = cv2.filter2D(image, -1, gaussian_kernel)

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
rgb_filtered_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(12, 6), dpi=100)
plt.subplot(1,2,1), plt.imshow(rgb_image)
plt.title('Исходное изображение'), plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2), plt.imshow(rgb_filtered_image)
plt.title('Фильтрованное изображение'), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.savefig('result_07.png', bbox_inches='tight')
print("07_gaussian_filter.py completed")
