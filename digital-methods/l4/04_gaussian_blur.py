import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

image = cv2.imread('input.jpg')
if image is None:
    raise RuntimeError("Could not open input.jpg")
# Blur with specific kernel size
blurred1 = cv2.GaussianBlur(image, (15, 15), 0)
blurred2 = cv2.GaussianBlur(image, (35, 35), 0)

plt.figure(figsize=(18, 6), dpi=100)
plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 3, 2), plt.imshow(cv2.cvtColor(blurred1, cv2.COLOR_BGR2RGB))
plt.title('Gaussian Blur (15x15)'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(blurred2, cv2.COLOR_BGR2RGB))
plt.title('Gaussian Blur (35x35)'), plt.xticks([]), plt.yticks([])
plt.savefig('result_04.png', bbox_inches='tight')
print("04_gaussian_blur.py completed")
