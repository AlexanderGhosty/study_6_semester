import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

image = cv2.imread('input.jpg')
if image is None:
    raise RuntimeError("Could not open input.jpg")
cv2.imwrite('output_01.jpg', image)

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(6, 6), dpi=100)
plt.imshow(rgb_image)
plt.title('Basic Read & Save')
plt.xticks([]), plt.yticks([])
plt.savefig('result_01.png', bbox_inches='tight')
print("01_read_save.py completed")
