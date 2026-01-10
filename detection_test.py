import cv2
import numpy as np
import matplotlib.pyplot as plt

camera = cv2.VideoCapture(0)
caffe_model = 'models/Res10_300x300_ssd_iter_140000.caffemodel'
prototxt_file = 'models/Resnet_SSD_deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffe_model)

THRESHOLD = 0.5



def adjusted_detect_face(frame):
    (h, w) = frame.shape[:2]

    # 1. Pre-process the frame: resize to 300x300 and subtract mean RGB values
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    # 2. Pass the blob through the network
    net.setInput(blob)
    detections = net.forward()

    best_confidence = THRESHOLD
    best_detection = None

    # 3. Loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # choose best detection
        if confidence > best_confidence:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            best_detection = ([startX, startY, endX, endY, confidence])

    return best_detection

def capture_frame():
    ret, frame = camera.read()
    if not ret:
        raise RuntimeError("Failed to capture image from camera.")
    return frame

def draw_frame(frame,face_rect):
    if not face_rect:
        cv2.imshow("Face Detection", frame)
        return frame
    (startX, startY, endX, endY, conf)= face_rect

    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Draw the confidence label
    text = f"{conf * 100:.2f}%"
    y = startY - 10 if startY - 10 > 10 else startY + 10
    cv2.putText(frame, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
    cv2.imshow("Face Detection", frame)
    return frame

if __name__ == "__main__":
    while True:
        frame = capture_frame()
        face_rect = adjusted_detect_face(frame)
        frame_with_detections = draw_frame(frame, face_rect)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()