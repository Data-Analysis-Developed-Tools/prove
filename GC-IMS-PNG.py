import streamlit as st
from PIL import Image
import io
import numpy as np
import cv2
from streamlit_cropper import st_cropper

# Titolo dell'app
st.title("Segmentazione delle Macchie in Immagini GC-IMS")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine (.png)", type=["png"])

if uploaded_file:
    # Apertura dell'immagine con PIL
    image = Image.open(uploaded_file)
    
    # Interfaccia di cropping manuale
    st.subheader("Seleziona l'area da ritagliare")
    cropped_image = st_cropper(image, box_color='red', aspect_ratio=None)

    if cropped_image:
        st.subheader("Immagine Ritagliata")
        st.image(cropped_image, use_container_width=True)
        
        # Convertire l'immagine ritagliata in un array numpy per l'elaborazione
        img_np = np.array(cropped_image.convert("RGB"))
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # Cursore per la soglia cromatica
        threshold_value = st.slider("Soglia per la segmentazione", 0, 255, 150)
        
        # Applicare un threshold
        _, thresh = cv2.threshold(img_gray, threshold_value, 255, cv2.THRESH_BINARY)
        
        # Trovare i contorni
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Visualizzare l'immagine segmentata
        st.subheader("Immagine Segmentata")
        st.image(thresh, use_column_width=True, caption="Macchie Segmentate")
        
        # Processare ogni blob trovato
        blob_data = []
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            cropped_blob = img_np[y:y+h, x:x+w]
            
            # Trova il punto con massima intensità nel blob
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img_gray[y:y+h, x:x+w])
            x_max, y_max = x + max_loc[0], y + max_loc[1]
            
            # Convertire in formato scaricabile
            blob_pil = Image.fromarray(cropped_blob)
            buf = io.BytesIO()
            blob_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            # Salvare i dettagli del blob
            blob_data.append((byte_im, x, x+w, y, y+h, x_max, y_max))
            
        # Mostrare i blob ritagliati
        st.subheader("Blob Identificati")
        for i, (blob_img, x_start, x_end, y_start, y_end, x_max, y_max) in enumerate(blob_data):
            st.image(blob_img, caption=f"Blob {i+1}: X[{x_start}:{x_end}], Y[{y_start}:{y_end}], Max Intensità ({x_max}, {y_max})", use_container_width=True)
            
            # Pulsante di download per ogni blob
            st.download_button(
                label=f"📥 Scarica Blob {i+1}",
                data=blob_img,
                file_name=f"blob_{i+1}.png",
                mime="image/png"
            )
