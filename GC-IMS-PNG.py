import streamlit as st
from PIL import Image
import io
import numpy as np
import cv2
from streamlit_cropper import st_cropper

# Titolo dell'app
st.title("Crop Manuale di Immagini GC-IMS")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine (.png)", type=["png"])

if uploaded_file:
    # Apertura dell'immagine con PIL
    image = Image.open(uploaded_file)

    # Mostra l'immagine caricata
    st.subheader("Immagine Originale")
    st.image(image, use_column_width=True)

    # Interfaccia di cropping manuale
    st.subheader("Seleziona l'area da ritagliare")
    cropped_image = st_cropper(image, box_color='red', aspect_ratio=None)

    # Mostra l'immagine ritagliata
    if cropped_image:
        st.subheader("Immagine Ritagliata")
        st.image(cropped_image, use_column_width=True)

        # Pulsante di download
        buf = io.BytesIO()
        cropped_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 Scarica Immagine Ritagliata",
            data=byte_im,
            file_name="ritaglio.png",
            mime="image/png"
        )
