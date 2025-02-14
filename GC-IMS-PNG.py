import cv2
import numpy as np
import pandas as pd
from PIL import Image
import os
import streamlit as st

# Percorso dell'immagine
image_path = "/mnt/data/image.png"

# Verificare che il file esista
if not os.path.exists(image_path):
    st.error(f"Errore: il file {image_path} non esiste!")
    st.stop()

# Tentare di caricare l'immagine con OpenCV
image = cv2.imread(image_path)

# Se OpenCV fallisce, provare con PIL
if image is None:
    try:
        image_pil = Image.open(image_path)
        image = np.array(image_pil)  # Convertire PIL in array NumPy
    except Exception as e:
        st.error(f"Errore durante il caricamento dell'immagine: {e}")
        st.stop()

# Convertire l'immagine in scala di grigi
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Normalizzare l'immagine
normalized_img = cv2.normalize(image_gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

# Applicare la colormap "jet"
colormap_img = cv2.applyColorMap(normalized_img, cv2.COLORMAP_JET)

# Threshold per segmentare le aree ad alta intensità
_, thresh = cv2.threshold(normalized_img, 150, 255, cv2.THRESH_BINARY)

# Trovare i contorni
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Lista dei dati dei blob
data = []
output_folder = "/mnt/data/cropped_blobs_colormap/"
os.makedirs(output_folder, exist_ok=True)

# Processare ogni blob
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_blob = colormap_img[y:y+h, x:x+w]

    # Punto con massima intensità
    _, max_val, _, max_loc = cv2.minMaxLoc(normalized_img[y:y+h, x:x+w])

    # Salva il blob
    cropped_path = os.path.join(output_folder, f"blob_{i}.png")
    Image.fromarray(cropped_blob).save(cropped_path)

    data.append([cropped_path, x, x+w, y, y+h, x + max_loc[0], y + max_loc[1]])

# Creare la tabella
df_colormap = pd.DataFrame(data, columns=["Immagine", "X Inizio", "X Fine", "Y Inizio", "Y Fine", "X Max Intensità", "Y Max Intensità"])

# Visualizzare i dati su Streamlit
st.subheader("Blob Identificati con Scala Cromatica")
st.dataframe(df_colormap)
