import streamlit as st
from PIL import Image
import numpy as np

uploaded_file = st.file_uploader("Upload gambar wajah", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('L')  # Konversi ke grayscale
    st.image(image, caption='Gambar yang Diupload', width=300)

    # Resize dan konversi ke array numpy
    img = image.resize((48, 48))  # Resize gambar sesuai ukuran yang diperlukan
    img_array = np.array(img) / 255.0  # Normalisasi

    img_array = img_array.reshape(1, 48, 48, 1)  # Tambahkan dimensi untuk kompatibilitas model

    # Lakukan prediksi atau proses lainnya
