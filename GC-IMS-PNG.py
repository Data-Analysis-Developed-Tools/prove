import streamlit as st
import cv2
import numpy as np
import tempfile
from PIL import Image
import io

# Titolo dell'app
st.title("Tool Interattivo per Ritaglio Immagine GC-IMS")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine (.png)", type=["png"])

if uploaded_file:
    # Leggere l'immagine
    image = Image.open(uploaded_file)
    img_np = np.array(image)

    # Mostrare l'immagine caricata
    st.image(image, caption="Immagine Caricata", use_column_width=True)

    # Selezione del ritaglio interattivo
    st.subheader("Seleziona un'area da ritagliare")
    from streamlit_drawable_canvas import st_canvas

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  
        stroke_width=3,
        stroke_color="#FF0000",
        background_image=image,
        height=img_np.shape[0],
        width=img_np.shape[1],
        drawing_mode="rect",
        key="canvas"
    )

    # Quando l'utente ha disegnato un rettangolo
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            obj = objects[0]  # Considera il primo rettangolo disegnato
            left, top, width, height = map(int, [obj["left"], obj["top"], obj["width"], obj["height"]])

            # Ritagliare l'immagine
            cropped_image = img_np[top:top+height, left:left+width]

            # Convertire l'immagine ritagliata in PIL
            cropped_pil = Image.fromarray(cropped_image)

            # Mostrare l'immagine ritagliata
            st.image(cropped_pil, caption="Immagine Ritagliata", use_column_width=True)

            # Creare un pulsante di download
            buf = io.BytesIO()
            cropped_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Scarica Immagine Ritagliata",
                data=byte_im,
                file_name="ritaglio.png",
                mime="image/png"
            )
