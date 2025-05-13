import cv2
import numpy as np
import pandas as pd

def preprocess_image(image_path):
    # Membaca gambar
    img = cv2.imread(image_path)
    
    # Mengubah ukuran gambar jika diperlukan
    img = cv2.resize(img, (48, 48))
    
    # Mengubah gambar ke grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Normalisasi gambar (nilai pixel antara 0 dan 1)
    img = img / 255.0
    
    return np.expand_dims(img, axis=-1)  # Menambah dimensi untuk kompatibilitas model

def load_data(csv_path):
    # Misalnya, memuat data CSV dengan informasi gambar dan label
    df = pd.read_csv(csv_path)
    return df
