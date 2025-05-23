import streamlit as st
from config import MODEL_PATH, DATABASE_PATH, LABELS
from database import connect_db, create_table
from camera_utils import detect_emotion_live
from tensorflow.keras.models import load_model
import os

# Set konfigurasi halaman
st.set_page_config(page_title="Emotion Detection App", layout="centered")
st.title("📷 Deteksi Ekspresi Wajah Real-Time")

# Cek dan load model hanya sekali
if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model tidak ditemukan di: {MODEL_PATH}")
    st.stop()

@st.cache_resource
def load_emotion_model():
    return load_model(MODEL_PATH)

model = load_emotion_model()

# Setup database
conn = connect_db(DATABASE_PATH)
create_table(conn)

# Pilih metode input (pastikan key unik)
input_method = st.radio(
    "Pilih metode input:",
    ["📸 Kamera Langsung", "📁 Upload Gambar"],
    key="input_method_radio"
)

# Jika kamera dipilih
if input_method == "📸 Kamera Langsung":
    if 'run_camera' not in st.session_state:
        st.session_state.run_camera = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Kamera", key="start_cam_btn"):
            st.session_state.run_camera = True
    with col2:
        if st.button("Stop Kamera", key="stop_cam_btn"):
            st.session_state.run_camera = False

    if st.session_state.run_camera:
        st.success("✅ Kamera aktif. Deteksi emosi berjalan.")
        detect_emotion_live(model, LABELS, conn)
    else:
        st.warning("⛔ Kamera tidak aktif.")

# Jika upload gambar dipilih
elif input_method == "📁 Upload Gambar":
    uploaded_file = st.file_uploader("Upload gambar wajah", type=["jpg", "jpeg", "png"], key="uploader_key")
    if uploaded_file is not None:
        from PIL import Image
        import numpy as np
        import cv2

        image = Image.open(uploaded_file).convert("L")  # konversi ke grayscale
        image = image.resize((48, 48))
        image_array = np.array(image) / 255.0
        image_array = image_array.reshape(1, 48, 48, 1)

        prediction = model.predict(image_array)
        label_index = np.argmax(prediction)
        label = LABELS[label_index]
        confidence = prediction[0][label_index]

        st.image(uploaded_file, caption=f"Prediksi: {label} ({confidence:.2%})", use_column_width=True)
