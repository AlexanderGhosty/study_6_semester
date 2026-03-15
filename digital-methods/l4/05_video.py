import cv2

cap = cv2.VideoCapture('input.mp4')
if not cap.isOpened():
    print("Error opening video file")
    exit(1)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_05.mp4', fourcc, fps, (320, 240))

count = 0
while cap.isOpened() and count < 60: # Limit to 60 frames for speed
    ret, frame = cap.read()
    if not ret:
        break
    
    # Resize frame
    resized_frame = cv2.resize(frame, (320, 240))
    out.write(resized_frame)
    count += 1

cap.release()
out.release()
print("05_video.py completed")
