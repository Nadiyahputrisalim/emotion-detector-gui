import streamlit as st
from PIL import Image
import numpy as np
import cv2
import tensorflow as tf
from datetime import datetime
from config import MODEL_PATH, DATABASE_PATH, IMAGE_SIZE
from database import connect_db, create_table, insert_emotion
from camera_utils import detect_emotion_live
from config import MODEL_PATH, DATABASE_PATH, IMAGE_SIZE, LABELS
from camera_utils import detect_emotion_live
from keras.models import load_model
from database import connect_db, create_table

model = load_model(MODEL_PATH)
conn = connect_db(DATABASE_PATH)
create_table(conn)

option = st.radio("Pilih metode input", ['📸 Kamera Langsung', '📁 Upload Gambar'])

if option == '📸 Kamera Langsung':
    detect_emotion_live(model, LABELS, conn)


# Load model
model = tf.keras.models.load_model(MODEL_PATH)
labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Koneksi database
conn = connect_db(DATABASE_PATH)
create_table(conn)

st.title("😃 Deteksi Ekspresi Wajah")

option = st.radio("Pilih metode input", ['📸 Kamera Langsung', '📁 Upload Gambar'])

if option == '📁 Upload Gambar':
    uploaded_file = st.file_uploader("Upload gambar wajah", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert('L')
        st.image(image, caption='Gambar yang Diupload', width=300)

        img = np.array(image.resize(IMAGE_SIZE)) / 255.0
        img_array = img.reshape(1, 48, 48, 1)

        predictions = model.predict(img_array)
        label = labels[np.argmax(predictions)]
        st.success(f"Ekspresi terdeteksi: **{label}**")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_emotion(conn, timestamp, label)

elif option == '📸 Kamera Langsung':
    detect_emotion_live(model, labels, conn)
