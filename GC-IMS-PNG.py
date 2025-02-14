import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

# Titolo dell'app
st.title("Tool Interattivo per Ritaglio Immagine GC-IMS")

# Caricamento immagine
uploaded_file = st.file_uploader("Carica un'immagine (.png)", type=["png"])

if uploaded_file:
    # Apertura dell'immagine con PIL e conversione in RGB
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Immagine Caricata", use_column_width=True)

    # Converti l'immagine in un oggetto BytesIO per generare un URL
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Creazione dell'URL per l'immagine di sfondo
    img_url = st.image(image).image_to_url(img_bytes)

    # Creazione della canvas interattiva
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Colore di riempimento con opacità
        stroke_width=3,
        stroke_color="#FF0000",
        background_image_url=img_url,  # Usa l'URL generato invece di passare direttamente l'immagine
        height=image.height,
        width=image.width,
        drawing_mode="rect",
        key="canvas"
    )

    # Quando l'utente ha disegnato un rettangolo
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            obj = objects[0]  # Considera il primo rettangolo disegnato
            left = int(obj["left"])
            top = int(obj["top"])
            width = int(obj["width"])
            height = int(obj["height"])

            # Ritaglio dell'immagine
            cropped_image = image.crop((left, top, left + width, top + height))

            # Mostra l'immagine ritagliata
            st.image(cropped_image, caption="Immagine Ritagliata", use_column_width=True)

            # Creazione del pulsante di download
            buf = io.BytesIO()
            cropped_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="📥 Scarica Immagine Ritagliata",
                data=byte_im,
                file_name="ritaglio.png",
                mime="image/png"
            )
