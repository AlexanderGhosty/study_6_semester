import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

image = cv2.imread('input.jpg')
if image is None:
    raise RuntimeError("Could not open input.jpg")
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
# Rotate by 45 degrees
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))

plt.figure(figsize=(12, 6), dpi=100)
plt.subplot(1, 2, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 2, 2), plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
plt.title('Rotated 45 degrees'), plt.xticks([]), plt.yticks([])
plt.savefig('result_03.png', bbox_inches='tight')
cv2.imwrite('output_03_rotated.jpg', rotated)
print("03_rotate.py completed")
