import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

image = cv2.imread('input.jpg')
if image is None:
    raise RuntimeError("Could not open input.jpg")
# Crop
height, width = image.shape[:2]
start_row, start_col = int(height * .25), int(width * .25)
end_row, end_col = int(height * .75), int(width * .75)
cropped = image[start_row:end_row, start_col:end_col]
# Resize
resized = cv2.resize(cropped, (300, 300), interpolation=cv2.INTER_CUBIC)

cv2.imwrite('output_02_cropped.jpg', cropped)
cv2.imwrite('output_02_resized.jpg', resized)

plt.figure(figsize=(12, 6), dpi=100)
plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 3, 2), plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
plt.title('Cropped'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
plt.title('Resized'), plt.xticks([]), plt.yticks([])
plt.savefig('result_02.png', bbox_inches='tight')
print("02_crop_resize.py completed")
