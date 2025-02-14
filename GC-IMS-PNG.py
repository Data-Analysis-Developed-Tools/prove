import cv2
import numpy as np
import pandas as pd
from PIL import Image
import os
import streamlit as st

# Caricamento dell'immagine ritagliata dal precedente crop
st.subheader("Seleziona l'immagine ritagliata per estrarre le feature")
uploaded_cropped_file = st.file_uploader("Carica l'immagine ritagliata (.png)", type=["png"])

if uploaded_cropped_file:
    # Salvataggio temporaneo dell'immagine caricata
    cropped_image_path = "/mnt/data/cropped_image.png"
    with open(cropped_image_path, "wb") as f:
        f.write(uploaded_cropped_file.getbuffer())

    # Caricare l'immagine ritagliata
    image = cv2.imread(cropped_image_path)

    # Verificare che l'immagine sia stata caricata correttamente
    if image is None:
        st.error(f"Errore: impossibile caricare l'immagine ritagliata.")
        st.stop()

    # Convertire in scala di grigi per analizzare l'intensità
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalizzare l'immagine per evidenziare le variazioni cromatiche
    normalized_img = cv2.normalize(image_gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # Applicare la colormap "jet"
    colormap_img = cv2.applyColorMap(normalized_img, cv2.COLORMAP_JET)

    # Threshold per segmentare le aree ad alta intensità
    _, thresh = cv2.threshold(normalized_img, 150, 255, cv2.THRESH_BINARY)

    # Trovare i contorni
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Lista dei dati dei nuovi blob
    data_new = []
    output_folder = "/mnt/data/cropped_blobs_from_crop/"
    os.makedirs(output_folder, exist_ok=True)

    # Processare ogni blob
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        cropped_blob = colormap_img[y:y+h, x:x+w]

        # Trova il punto di massima intensità
        _, max_val, _, max_loc = cv2.minMaxLoc(normalized_img[y:y+h, x:x+w])

        # Salva il nuovo blob
        cropped_path = os.path.join(output_folder, f"final_blob_{i}.png")
        Image.fromarray(cropped_blob).save(cropped_path)

        data_new.append([cropped_path, x, x+w, y, y+h, x + max_loc[0], y + max_loc[1]])

    # Creare il nuovo DataFrame
    df_final = pd.DataFrame(data_new, columns=["Immagine", "X Inizio", "X Fine", "Y Inizio", "Y Fine", "X Max Intensità", "Y Max Intensità"])

    # Visualizzare i dati su Streamlit
    st.subheader("Feature Estratte dal Crop")
    st.dataframe(df_final)
