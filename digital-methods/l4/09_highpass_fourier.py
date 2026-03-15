import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

img = cv2.imread('input.jpg', 0)
if img is None: raise RuntimeError("Could not open input.jpg")
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
rows, cols = img.shape  # type: ignore
crow, ccol = int(rows/2), int(cols/2)
mask = np.ones((rows, cols), np.uint8)
r = 30
mask[crow - r:crow + r, ccol - r:ccol + r] = 0
fshift = fshift * mask
f_ishift = np.fft.ifftshift(fshift)
img_back = np.abs(np.fft.ifft2(f_ishift))

plt.figure(figsize=(12, 6), dpi=100)
rgb_image = cv2.cvtColor(cv2.imread('input.jpg'), cv2.COLOR_BGR2RGB)
plt.subplot(1,2,1), plt.imshow(rgb_image)
plt.title('Исходное изображение'), plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2), plt.imshow(img_back, cmap='gray')
plt.title('Изображение, обработанное ФВЧ'), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.savefig('result_09.png', bbox_inches='tight')
print("09_highpass_fourier.py completed")
