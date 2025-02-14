import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

# Titolo dell'app
st.title("Strumento Interattivo per il Ritaglio di Immagini GC-IMS")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine (.png)", type=["png"])

if uploaded_file:
    # Apertura immagine con PIL e conversione in RGB
    image = Image.open(uploaded_file).convert("RGB")  # Assicura compatibilità con Streamlit

    # Mostrare l'immagine caricata
    st.image(image, caption="Immagine Caricata", use_column_width=True)

    # Converti l'immagine in NumPy array per compatibilità con st_canvas
    img_np = np.array(image)

    # Creazione della canvas interattiva per il ritaglio
    st.subheader("Seleziona un'area da ritagliare con il mouse")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Colore semi-trasparente per la selezione
        stroke_width=3,
        stroke_color="#FF0000",  # Rosso per il contorno
        background_image=image,  # Immagine convertita in RGB
        height=image.height,
        width=image.width,
        drawing_mode="rect",
        key="canvas"
    )

    # Se l'utente ha disegnato un rettangolo, ritaglia l'area selezionata
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            obj = objects[0]  # Prende il primo rettangolo disegnato
            left, top, width, height = map(int, [obj["left"], obj["top"], obj["width"], obj["height"]])

            # Ritagliare l'immagine
            cropped_image = img_np[top:top+height, left:left+width]

            # Convertire l'immagine ritagliata in PIL
            cropped_pil = Image.fromarray(cropped_image)

            # Mostrare l'immagine ritagliata
            st.image(cropped_pil, caption="Immagine Ritagliata", use_column_width=True)

            # Creare un pulsante di download per l'immagine ritagliata
            buf = io.BytesIO()
            cropped_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Scarica Immagine Ritagliata",
                data=byte_im,
                file_name="ritaglio.png",
                mime="image/png"
            )
