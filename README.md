
#  Polygonal ROI-Based Real-Time Object Detection and Alert System 

## Overview
This project is a **Real-Time Security Monitoring System** that utilizes the YOLO object detection model to detect specified objects (like persons, vehicles, etc.) in a live video feed from an RTSP camera. The user can define a **polygonal Region of Interest (ROI)**, and if a person is detected within this region, an alarm sound is triggered, and snapshots of the detected object are saved. The video feed, with detected objects and their labels, is displayed in real-time for security monitoring purposes.

## Features
- **Object Detection**: Detects multiple objects (e.g., person, car, truck, bus) using YOLO.
- **Polygonal ROI**: Define a custom region of interest (ROI) by drawing a polygon over the video feed.
- **Alarm Trigger**: Plays an alarm sound when a person is detected inside the ROI.
- **Image Capture**: Saves photos of detected persons within the defined ROI.
- **Real-time Video Feed**: Displays video feed with detected objects and their labels.

## Dependencies
Ensure that the following libraries are installed:
- OpenCV (`cv2`)
- PyTorch (`torch`)
- Numpy (`numpy`)
- Pygame (`pygame`)

You can install the required libraries using pip:

```bash
pip install opencv-python torch numpy pygame
```

## Setup

1. **Alarm Sound**: Update the path to your alarm sound file in the code. Modify the following line:
    ```python
    path_alarm = r"C:\path\to\your\alarm.wav"
    ```

2. **RTSP URL**: Replace the placeholder `rtsp_url` with the RTSP URL of your CCTV camera:
    ```python
    rtsp_url = "rtsp://your_camera_url_here"
    ```

3. **Saving Detected Photos**: The script saves images of detected persons in the `Detected Photos/` folder. Ensure this folder exists, or modify the save path accordingly in the code:
    ```python
    cv2.imwrite(f"Detected Photos/detected{count}.jpg", frame_detected)
    ```

4. **Target Classes**: The script detects objects belonging to specific target classes, which can be modified in the code:
    ```python
    target_classes = [ 'person']
    ```

## Running the Script

1. After setting up the necessary paths and configurations, you can run the script:
    ```bash
    python your_script_name.py
    ```

2. The video feed will open in a window titled "Video". Left-click on the video window to mark points for the polygonal ROI. Right-click to clear the selected ROI points.

3. The alarm will trigger, and images will be saved when a person is detected within the defined polygonal ROI.

4. Press the 'q' key to exit the video stream.

## Key Functions

- **draw_polygon**: Captures mouse clicks to define the points of the polygonal ROI.
- **inside_polygon**: Checks if the center of a detected object lies within the defined ROI.
- **preprocess**: Resizes the frame for YOLO input.
- **Object Detection**: The script performs real-time detection using YOLO, draws bounding boxes around detected objects, and labels them.

## Customization

- **Number of Photos**: You can adjust the number of detected photos saved by modifying the `number_of_photos` variable:
    ```python
    number_of_photos = 10
    ```

- **Target Object**: Modify the `target_classes` list to detect different object classes like bicycles, motorcycles, etc.

## Troubleshooting

- If the video stream does not appear or fails to capture frames, double-check the RTSP URL and ensure the connection is stable. 
- If the alarm does not play, verify the correct path to the alarm sound file.
