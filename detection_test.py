import numpy as np
import time
import cv2
import onnxruntime as ort
import torch
# import functools
#
# torch.load = functools.partial(torch.load, weights_only=False)
#
# from hsemotion_onnx.facial_emotions import HSEmotionRecognizer

camera = cv2.VideoCapture(0)
caffe_model = 'models/Res10_300x300_ssd_iter_140000.caffemodel'
prototxt_file = 'models/Resnet_SSD_deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffe_model)


THRESHOLD = 0.5
last_time = 0
TIME_THRESHOLD = 1.0  # seconds
emotion_model_path = 'models/enet_b0_8_best_afew.onnx'
# emotion_model = HSEmotionRecognizer(model_name='enet_b0_8_best_afew')
try:
    emotion_session = ort.InferenceSession(emotion_model_path)
    print(f"Model załadowany pomyślnie z: {emotion_model_path}")
except Exception as e:
    print(f"BŁĄD: Nie znaleziono pliku modelu w {emotion_model_path}. Upewnij się, że tam jest!")
    exit()
EMOTION_LABELS = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']

def detect_face(frame):
    (h, w) = frame.shape[:2]

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

    return face_rect, best_confidence

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

# def classify_emotion(frame, face_rect):
#     if face_rect is None:
#         return None, None
#
#     startX, startY, endX, endY = face_rect
#
#     face_img = frame[startY:endY, startX:endX]
#
#     if face_img.size == 0:
#         return None, None
#
#     face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
#
#     emotion, scores = emotion_model.predict_emotions(face_img_rgb)
#     # return emotion, scores
#     return emotion, 0.94


def classify_emotion_onnx(frame, face_rect):
    """Ręczny preprocessing i predykcja ONNX"""
    if face_rect is None: return None, 0

    startX, startY, endX, endY = face_rect
    face_img = frame[startY:endY, startX:endX]
    if face_img.size == 0: return None, 0

    # 1. Preprocessing (wymagany dla EfficientNet)
    img = cv2.resize(face_img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0

    # Normalizacja ImageNet (Standard dla hsemotion)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img = (img - mean) / std

    # Zmiana układu z (H, W, C) na (C, H, W) i dodanie wymiaru batcha
    img = img.transpose(2, 0, 1)
    img = np.expand_dims(img, axis=0)

    # 2. Predykcja ONNX
    inputs = {emotion_session.get_inputs()[0].name: img}
    outputs = emotion_session.run(None, inputs)
    scores = outputs[0][0]

    emotion_idx = np.argmax(scores)
    return EMOTION_LABELS[emotion_idx], float(scores[emotion_idx])

def draw_frame_with_emotion(frame,face_rect, confidence, emotion):
    if face_rect is None or emotion is None:
        cv2.imshow("Face & Emotion Detection", frame)
        return

    startX, startY, endX, endY = face_rect

    # Rysowanie ramki twarzy
    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Przygotowanie tekstu (Emocja + Pewność detekcji twarzy)
    label = f"{emotion}: {confidence * 100:.1f}%" if emotion else f"{confidence * 100:.1f}%"

    y = startY - 10 if startY - 10 > 10 else startY + 10
    cv2.putText(frame, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Face & Emotion Detection", frame)

if __name__ == "__main__":
    print("main started")
    last_emotion = None
    while True:
        current_time = time.time()
        frame = capture_frame()
        face_rect, face_confidence = detect_face(frame)
        if face_rect:
            if current_time - last_time > TIME_THRESHOLD or not last_emotion:
                # emotion, emotion_confidence = classify_emotion(frame, face_rect)
                emotion, emotion_confidence = classify_emotion_onnx(frame, face_rect)
                draw_frame_with_emotion(frame, face_rect, emotion_confidence, emotion)
                last_emotion = emotion
                last_time = current_time
            else:
                draw_frame_with_emotion(frame, face_rect, 0.0, last_emotion)
        else:
            cv2.imshow("Face & Emotion Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

