import cv2
import numpy as np
import time
import csv
from datetime import datetime
import tensorflow as tf

# ======================
# LOAD TFLITE MODEL
# ======================
interpreter = tf.lite.Interpreter(model_path="emotion_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ⚠ MUST match training folder order
labels = ["anger", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

# ======================
# FACE DETECTOR
# ======================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ======================
# LOG FILE
# ======================
log_file = open("emotion_log.csv", "a", newline="")
logger = csv.writer(log_file)

if log_file.tell() == 0:
    logger.writerow(["timestamp", "emotion"])

# ======================
# CAMERA
# ======================
cap = cv2.VideoCapture(0)

capture_interval = 2
last_capture_time = 0
last_emotion = ""

print("✅ Real-time emotion detection started (Press Q to quit)")

# ======================
# LOOP
# ======================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(60, 60)
    )

    current_time = time.time()

    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        if current_time - last_capture_time >= capture_interval:

            face = gray[y:y+h, x:x+w]

            if face.size == 0:
                continue

            face = cv2.resize(face, (48, 48))
            face = face.astype(np.float32) / 255.0
            face = face.reshape(1, 48, 48, 1)

            interpreter.set_tensor(input_details[0]['index'], face)
            interpreter.invoke()

            prediction = interpreter.get_tensor(output_details[0]['index'])[0]
            last_emotion = labels[np.argmax(prediction)]

            logger.writerow([datetime.now().isoformat(), last_emotion])
            print(datetime.now(), "→", last_emotion)

            last_capture_time = current_time

        if last_emotion:
            cv2.putText(
                frame,
                last_emotion,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ======================
# CLEANUP
# ======================
cap.release()
log_file.close()
cv2.destroyAllWindows()
