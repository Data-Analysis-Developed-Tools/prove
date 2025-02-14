import cv2
import numpy as np
import pandas as pd
from PIL import Image
import os
import streamlit as st

# Caricare l'immagine
image_path = "/mnt/data/image.png"
image = cv2.imread(image_path)

# Convertire l'immagine in scala di grigi per analizzare l'intensità
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Normalizzare l'immagine per evidenziare le variazioni cromatiche
normalized_img = cv2.normalize(image_gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

# Applicare la colormap "jet" per evidenziare le intensità
colormap_img = cv2.applyColorMap(normalized_img, cv2.COLORMAP_JET)

# Applicare un threshold per segmentare le regioni di maggiore intensità
_, thresh = cv2.threshold(normalized_img, 150, 255, cv2.THRESH_BINARY)

# Trovare i contorni delle macchie sulla mappa di calore
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Lista per la tabella dei risultati
data = []

# Cartella per le immagini ritagliate
output_folder = "/mnt/data/cropped_blobs_colormap/"
os.makedirs(output_folder, exist_ok=True)

# Processare ogni contorno rilevato
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)  # Ottieni il bounding box
    cropped_blob = colormap_img[y:y+h, x:x+w]  # Ritaglia l'area del blob

    # Trova il punto di massima intensità sulla scala cromatica
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(normalized_img[y:y+h, x:x+w])

    # Salva l'immagine ritagliata
    cropped_path = os.path.join(output_folder, f"blob_{i}.png")
    Image.fromarray(cropped_blob).save(cropped_path)

    # Aggiungere i dati alla tabella
    data.append([cropped_path, x, x+w, y, y+h, x + max_loc[0], y + max_loc[1]])

# Creare un DataFrame pandas con i risultati
df_colormap = pd.DataFrame(data, columns=["Immagine", "X Inizio", "X Fine", "Y Inizio", "Y Fine", "X Max Intensità", "Y Max Intensità"])

# Visualizzare la tabella aggiornata su Streamlit
st.subheader("Blob Identificati con Scala Cromatica")
st.dataframe(df_colormap)
