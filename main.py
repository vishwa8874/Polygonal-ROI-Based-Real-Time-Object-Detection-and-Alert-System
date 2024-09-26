import cv2
import torch
import numpy as np
import pygame

path_alarm = r"C:\Users\91960\Downloads\target-detector-yolov5-main (2)\target-detector-yolov5-main\Alarm\alarm.wav"

pygame.init()
pygame.mixer.music.load(path_alarm)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

rtsp_url = ""  # Make sure this URL is correct
cap = cv2.VideoCapture(rtsp_url)

# Target classes to detect
target_classes = [ 'person']
count = 0
number_of_photos = 10

pts = []

def draw_polygon(event, x, y, flags, param):
    global pts
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        pts.append([x, y])
    elif event == cv2.EVENT_RBUTTONDOWN:
        pts = []

def inside_polygon(point, polygon):
    result = cv2.pointPolygonTest(polygon, (point[0], point[1]), False)
    return result == 1

cv2.namedWindow('Video')
cv2.setMouseCallback('Video', draw_polygon)

def preprocess(img):
    height, width = img.shape[:2]
    ratio = height / width
    img = cv2.resize(img, (640, int(640 * ratio)))
    return img

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Error: Failed to grab frame. Stream may be disconnected or URL may be incorrect.")
        break

    frame_detected = frame.copy()

    frame = preprocess(frame)

    results = model(frame)

    rendered_images = results.render()

    if len(rendered_images) > 0:
        frame_detected = rendered_images[0]
    else:
        print("No detections found.")
        frame_detected = frame

    for index, row in results.pandas().xyxy[0].iterrows():
        center_x = None
        center_y = None

        if row['name'] in target_classes:
            name = str(row['name'])
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)

            cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            if len(pts) >= 4:
                frame_copy = frame.copy()
                cv2.fillPoly(frame_copy, np.array([pts]), (0, 255, 0))
                frame = cv2.addWeighted(frame_copy, 0.1, frame, 0.9, 0)

                if center_x is not None and center_y is not None and inside_polygon((center_x, center_y), np.array([pts])) and name == 'person':
                    mask = np.zeros_like(frame_detected)
                    points = np.array([[x1, y1], [x1, y2], [x2, y2], [x2, y1]])
                    points = points.reshape((-1, 1, 2))
                    mask = cv2.fillPoly(mask, [points], (255, 255, 255))
                    frame_detected = cv2.bitwise_and(frame_detected, mask)

                    if count < number_of_photos:
                        cv2.imwrite(f"Detected Photos/detected{count}.jpg", frame_detected)
                    
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
                    
                    cv2.putText(frame, "Target", (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, "Person Detected", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    count += 1

    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()