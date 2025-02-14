import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def extract_metadata_and_data(file_bytes):
    """
    Estrae i metadati e i dati binari dal file .mea.
    - I metadati sono identificati come stringhe leggibili all'inizio del file.
    - I dati binari vengono separati per la generazione dell'immagine.
    """
    file_text = file_bytes.decode("utf-8", errors="ignore")  # Decodifica il file in UTF-8 ignorando errori
    lines = file_text.splitlines()

    metadata = {}
    binary_start = 0

    # Estrazione dei metadati
    for i, line in enumerate(lines):
        if "=" in line:  # Cerca le linee formattate come metadati (chiave = valore)
            key, value = map(str.strip, line.split("=", 1))
            metadata[key] = value
        else:
            binary_start = i
            break  # Quando incontriamo la prima riga non leggibile, passiamo ai dati binari

    # Estrazione dei dati binari effettivi
    binary_data = np.frombuffer(file_bytes[binary_start:], dtype=np.uint8)

    # Debug: Mostra una parte dei dati binari
    st.write(f"📊 Dimensione dati binari: {len(binary_data)} bytes")
    st.write(f"🔍 Prime 100 posizioni binarie: {binary_data[:100]}")

    # Controllo se la matrice è quadrata e se la conversione è riuscita
    if len(binary_data) < 100:
        st.error("❌ I dati binari sono troppo pochi per generare un'immagine.")
        return metadata, None  # Evita errori se non ci sono dati sufficienti
    else:
        size = int(np.sqrt(len(binary_data)))
        st.write(f"🖼️ La matrice avrà dimensione: {size}x{size}")

    # Converte i dati in formato uint8
    binary_data = np.array(binary_data, dtype=np.uint8)

    return metadata, binary_data

def generate_image_from_data(binary_data):
    """
    Converte i dati binari in una bitmap e li visualizza con colormap Inferno.
    """
    if binary_data is None:
        return None  # Evita errori se non ci sono dati validi

    # Determina la dimensione della matrice per visualizzare l'immagine
    size = int(np.sqrt(len(binary_data)))  # Calcolo della dimensione della matrice quadrata
    matrix_data = binary_data[:size**2].reshape((size, size))  # Conversione in matrice 2D

    # Creazione della figura con colormap inferno
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(matrix_data, cmap="inferno", aspect="auto")
    plt.colorbar(im, ax=ax, label="Intensità del Segnale")
    plt.title("Bitmap del File .MEA")

    return fig

# 🏠 **Interfaccia Streamlit**
st.title("Visualizzazione File .MEA")
st.write("Carica un file .MEA per visualizzarne i dati in un'immagine.")

# 📂 **Caricamento File**
uploaded_file = st.file_uploader("Carica il tuo file .MEA", type=["mea"])

if uploaded_file is not None:
    st.success("✅ File caricato con successo!")

    # 📌 **Lettura del file e separazione dei metadati dai dati binari**
    file_bytes = uploaded_file.read()
    metadata, binary_data = extract_metadata_and_data(file_bytes)

    # 📝 **Mostra i metadati**
    with st.expander("📄 Mostra Metadati"):
        st.json(metadata)

    # 🎨 **Generazione dell'immagine**
    if binary_data is not None:
        st.write("🔍 Generando immagine dalla bitmap...")
        image_fig = generate_image_from_data(binary_data)

        # 🖼 **Mostra l'immagine generata**
        if image_fig is not None:
            st.pyplot(image_fig)
    else:
        st.error("❌ Errore nella generazione dell'immagine. I dati binari non sono validi.")
