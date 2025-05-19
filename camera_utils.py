import cv2
import numpy as np
import streamlit as st
from datetime import datetime
from database import insert_emotion
import time

# di dalam while loop kamera
time.sleep(0.05)  # Delay 50ms antara frame


def detect_emotion_live(model, labels, conn):
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Tidak dapat mengakses kamera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi_gray, (48, 48))
            roi_normalized = roi_resized / 255.0
            roi_reshaped = roi_normalized.reshape(1, 48, 48, 1)

            prediction = model.predict(roi_reshaped)
            max_index = int(np.argmax(prediction))
            emotion = labels[max_index]

            # Gambar kotak dan label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Simpan ke database
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_emotion(conn, timestamp, emotion)

        stframe.image(frame, channels="BGR")

    cap.release()
