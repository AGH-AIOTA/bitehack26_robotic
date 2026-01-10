import numpy as np
import time
import cv2

camera = cv2.VideoCapture(0)
caffe_model = 'models/Res10_300x300_ssd_iter_140000.caffemodel'
prototxt_file = 'models/Resnet_SSD_deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffe_model)

THRESHOLD = 0.5



def detect_face(frame):
    (h, w) = frame.shape[:2]

    # 1. Pre-process the frame: resize to 300x300 and subtract mean RGB values
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    # 2. Pass the blob through the network
    net.setInput(blob)
    detections = net.forward()

    best_confidence = THRESHOLD
    best_detection = None
    face_rect = None
    confidence = 0.0

    # 3. Loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # choose best detection
        if confidence > best_confidence:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face_rect = ([startX, startY, endX, endY])
            best_confidence = confidence

    return face_rect, confidence

def capture_frame():
    ret, frame = camera.read()
    if not ret:
        raise RuntimeError("Failed to capture image from camera.")
    return frame

def draw_frame(frame, face_rect, confidence):
    if face_rect is None:
        cv2.imshow("Face Detection", frame)
        return

    startX, startY, endX, endY = face_rect

    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    text = f"{confidence * 100:.2f}%"
    y = startY - 10 if startY - 10 > 10 else startY + 10
    cv2.putText(frame, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)


if __name__ == "__main__":
    while True:
        frame = capture_frame()
        current_time = time.time()
        face_rect, confidence = detect_face(frame)
        draw_frame(frame, face_rect, confidence)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

