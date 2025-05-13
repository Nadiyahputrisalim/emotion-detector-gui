import streamlit as st
from keras.models import load_model
import numpy as np
from PIL import Image, ImageOps
import cv2

# Load model
model = load_model("models/model_emosi.h5")


# Label emosi sesuai dataset
labels = ['Marah', 'Jijik', 'Takut', 'Senang', 'Sedih', 'Kaget', 'Netral']

st.set_page_config(page_title="Deteksi Emosi Wajah", layout="centered")
st.title("😊 Deteksi Emosi dari Wajah")

uploaded_file = st.file_uploader("📤 Upload gambar wajah", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('L')  # Grayscale
    st.image(image, caption='Gambar yang Diupload', width=300)
    img = image.resize((48, 48))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1, 48, 48, 1)

    prediction = model.predict(img_array)
    label_index = np.argmax(prediction)
    emosi = labels[label_index]

    st.markdown(f"### 😃 Emosi Terdeteksi: **{emosi}**")
    st.write("📊 Probabilitas Semua Emosi:")
    for i in range(7):
        st.write(f"- {labels[i]}: `{prediction[0][i]:.2f}`")
import preprocess

# Menggunakan fungsi untuk preprocessing gambar
image = preprocess.preprocess_image("path_to_image.jpg")

# Menggunakan fungsi untuk memuat dataset
data = preprocess.load_data("data.csv")

import database

# Koneksi ke database
conn = database.connect_db("emotion_database.db")

# Mengambil data emosi
emotions_data = database.fetch_emotions(conn)

import config

# Menggunakan nilai konfigurasi
model_path = config.MODEL_PATH
image_size = config.IMAGE_SIZE
