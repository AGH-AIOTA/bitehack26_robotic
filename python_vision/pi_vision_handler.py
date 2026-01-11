import cv2
import os
import sys
import time
import numpy as np
import onnxruntime as ort
from multiprocessing import Process, Value

# Dodaj import Picamera2
try:
    from picamera2 import Picamera2
    from libcamera import Transform
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False
    print("UWAGA: Picamera2 nie jest zainstalowane. Uruchom:")
    print("sudo apt install python3-picamera2 python3-libcamera")

# --- KONFIGURACJA ---
EMOTION_LABELS = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
THRESHOLD = 0.3
TIME_THRESHOLD = 0.1

# --- FUNKCJE POMOCNICZE (LOGIKA DETEKCJI) ---

def calculate_face_center(face_rect):
    if face_rect is None: return None
    startX, startY, endX, endY = face_rect
    centerX = (startX + endX) // 2
    centerY = (startY + endY) // 2
    return centerX, centerY

def detect_face(net, frame):
    (h, w) = frame.shape[:2]
    # Blob 300x300 dla modelu SSD
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    best_confidence = THRESHOLD
    face_rect = None

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > best_confidence:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # Sprawdzenie czy współrzędne są sensowne
            if startX < w and startY < h and endX > 0 and endY > 0:
                face_rect = [startX, startY, endX, endY]
                best_confidence = confidence

    return face_rect, best_confidence

def classify_emotion_onnx(emotion_session, frame, face_rect):
    if face_rect is None: return -1, 0.0

    startX, startY, endX, endY = face_rect
    h, w = frame.shape[:2]
    
    # Clip (przytnij) współrzędne do wymiarów obrazu, żeby nie wyjść poza tablicę
    startX = max(0, startX)
    startY = max(0, startY)
    endX = min(w, endX)
    endY = min(h, endY)

    face_img = frame[startY:endY, startX:endX]
    if face_img.size == 0: return -1, 0.0

    # Preprocessing
    try:
        img = cv2.resize(face_img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0

        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img = (img - mean) / std

        img = img.transpose(2, 0, 1)
        img = np.expand_dims(img, axis=0)

        # Predykcja ONNX
        inputs = {emotion_session.get_inputs()[0].name: img}
        outputs = emotion_session.run(None, inputs)
        scores = outputs[0][0]
        
        e_x = np.exp(scores - np.max(scores))
        probabilities = e_x / e_x.sum()
        emotion_idx = np.argmax(probabilities)
        confidence = float(probabilities[emotion_idx])
        
        return int(emotion_idx), confidence
    except Exception as e:
        print(f"Błąd w klasyfikacji: {e}")
        return -1, 0.0

# --- INICJALIZACJA I KAMERA (Z PICAMERA2) ---

def initialize_vision():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Ścieżka do modeli
    PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) 
    MODELS_DIR = os.path.join(PROJECT_ROOT, 'python_vision', 'models') 

    # Sprawdzenie ścieżek
    caffe_model = os.path.join(MODELS_DIR, 'Res10_300x300_SSD_iter_140000.caffemodel')
    prototxt_file = os.path.join(MODELS_DIR, 'Resnet_SSD_deploy.prototxt')
    emotion_model_path = os.path.join(MODELS_DIR, 'enet_b0_8_best_afew.onnx')

    if not os.path.exists(MODELS_DIR):
        print(f"BŁĄD: Nie znaleziono folderu {MODELS_DIR}")
        sys.exit(1)

    # 1. Inicjalizacja Kamery (Picamera2 dla RPi5)
    if not PICAMERA2_AVAILABLE:
        print("BŁĄD: Picamera2 nie jest zainstalowane!")
        print("Zainstaluj: sudo apt install python3-picamera2 python3-libcamera")
        sys.exit(1)
    
    print("Inicjalizacja Picamera2...")
    picam2 = Picamera2()
    
    # Konfiguracja - prosty preview w formacie BGR (dla OpenCV)
    config = picam2.create_preview_configuration(
        main={"size": (1280, 720), "format": "RGB888"},
        transform=Transform(hflip=1, vflip=1)  # Odwróć jeśli kamera do góry nogami
    )
    
    picam2.configure(config)
    picam2.start()
    
    # Poczekaj na inicjalizację kamery
    time.sleep(2)
    
    print("Picamera2 zainicjalizowana pomyślnie")
    
    # 2. Inicjalizacja Modeli
    try:
        net = cv2.dnn.readNetFromCaffe(prototxt_file, caffeModel=caffe_model)
        # Przyspieszenie OpenCV na CPU
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        emotion_session = ort.InferenceSession(emotion_model_path)
    except Exception as e:
        print(f"BŁĄD modeli: {e}")
        picam2.close()
        sys.exit(1)

    return picam2, net, emotion_session

def capture_frame(picam2):
    """Pobiera klatkę z Picamera2 i konwertuje do BGR dla OpenCV"""
    try:
        # Picamera2 zwraca obraz w formacie RGB888
        frame = picam2.capture_array()
        if frame is None or frame.size == 0:
            return None
        # Konwersja z RGB (Picamera2) do BGR (OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame
    except Exception as e:
        print(f"Błąd przechwytywania klatki: {e}")
        return None

# --- GŁÓWNA PĘTLA WIZJI ---
import sys
sys.path.append("/home/bajer/bitehack")

from comm.esp_comm import ESP32Communicator
from tts.tts import VoiceSynthesizer

from time import sleep
from enum import Enum
class Face(Enum):
    NORMAL = 1
    BLINK = 2
    SHY = 3
    SAD = 4 
    HAPPY = 5
    SAY = 6
    UWU = 7

def run_vision_pipeline(shared_face_x, shared_face_y, shared_emotion_idx):
    # Inicjalizacja wewnątrz procesu
    camera, face_net, emotion_session = initialize_vision()

    last_emotion_idx = None
    last_time = 0

    voiceSynthesizer = VoiceSynthesizer()
    espComm = ESP32Communicator("/dev/ttyUSB0")
    last_state = "Happiness"

    print("[Vision] Proces uruchomiony. Czekam na klatki...")

    try:
        while True:
            current_time = time.time()
            
            frame = capture_frame(camera)
            if frame is None:
                time.sleep(0.01)  # Krótka pauza jeśli problem z klatką
                continue

            # Detekcja Twarzy
            face_rect, face_confidence = detect_face(face_net, frame)
            if face_rect:
                # Zapis środka twarzy do Shared Memory
                cx, cy = calculate_face_center(face_rect)
                shared_face_x.value = cx
                shared_face_y.value = cy
                
                #print(f"face_confidence: {face_confidence}")
                #print(f'cx: {cx}, cy: {cy}')
                
                # Detekcja Emocji (tylko co jakiś czas, bo jest wolna)
                if current_time - last_time > TIME_THRESHOLD or last_emotion_idx is None:
                    idx, conf = classify_emotion_onnx(emotion_session, frame, face_rect)
                    
                    if idx != -1:
                        shared_emotion_idx.value = idx
                        last_emotion_idx = idx
                        last_time = current_time
                        
                        if last_state == EMOTION_LABELS[idx]:
                            continue
                        last_state = EMOTION_LABELS[idx]

                        # Debug
                        print(f"Widzę: {EMOTION_LABELS[idx]} ({conf:.2f})")

                #EMOTION_LABELS = ['Anger', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
                        if EMOTION_LABELS[idx] in ["Anger", 'Sadness']:
                            espComm.sendFace(Face.SAD.value)
                            sleep(1.5)
                            espComm.sendFace(Face.SAY.value)
                            espComm.sendGift(0)
                            voiceSynthesizer.say("Ale fajny żart")
                        elif EMOTION_LABELS[idx] in ['Fear', 'Surprise']:
                            espComm.sendFace(Face.SHY.value)
                            sleep(1)
                        elif EMOTION_LABELS[idx] == "Happiness":
                            espComm.sendFace(Face.UWU.value)
                            sleep(2)
                        else:
                            pass

                        sleep(0.5)
                        espComm.sendFace(Face.BLINK.value)

            else:
                # Reset gdy brak twarzy
                shared_face_x.value = -1
                shared_face_y.value = -1
                
    except KeyboardInterrupt:
        print("[Vision] Przerwano przez użytkownika")
    except Exception as e:
        print(f"[Vision] Błąd: {e}")
    finally:
        print("[Vision] Zamykam kamerę...")
        camera.close()

# --- START ---

if __name__ == "__main__":
    # Zmienne współdzielone
    face_x = Value('i', -1)
    face_y = Value('i', -1)
    emotion_id = Value('i', -1)

    p = Process(target=run_vision_pipeline, args=(face_x, face_y, emotion_id))
    p.start()

    print("Główny proces działa. Naciśnij Ctrl+C aby wyjść.")
    
    try:
        while True:
            # Możesz tu dodać odczyt współdzielonych zmiennych
            if face_x.value != -1:
                pass#print(f"Twarz w: ({face_x.value}, {face_y.value}), Emocja: {EMOTION_LABELS[emotion_id.value] if emotion_id.value != -1 else 'Brak'}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nZatrzymywanie procesu wizji...")
        p.terminate()
        p.join()
        print("Zakończono.")