import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def extract_gcims_data(file_bytes):
    """
    Estrae i metadati e i dati binari da un file .MEA relativo a GC-IMS.
    - I metadati contengono informazioni sperimentali.
    - I dati binari rappresentano la matrice 2D (Tempo di Ritenzione x Tempo di Deriva).
    """
    file_text = file_bytes.decode("utf-8", errors="ignore")  # Decodifica il file come testo ignorando errori
    lines = file_text.splitlines()

    metadata = {}
    binary_start = 0

    # 🔍 **Separazione metadati e dati binari**
    for i, line in enumerate(lines):
        if "=" in line:  # Cerca le linee con formato "chiave = valore"
            key, value = map(str.strip, line.split("=", 1))
            metadata[key] = value
        else:
            binary_start = i
            break  # Quando i metadati finiscono, inizia la parte binaria

    # 📌 **Estrazione dati binari**
    binary_data = np.frombuffer(file_bytes[binary_start:], dtype=np.float32)  # I dati GC-IMS sono tipicamente float32

    # 🔎 **Verifica della lunghezza dei dati**
    st.write(f"📊 Dimensione dati binari: {len(binary_data)} valori numerici")

    # 📏 **Definizione delle dimensioni della matrice GC-IMS**
    # La matrice è tipicamente di 200x200, 256x256 o 512x512 in base alla risoluzione dello strumento
    size = int(np.sqrt(len(binary_data)))  
    if size * size != len(binary_data):
        st.warning("⚠️ I dati binari non formano una matrice quadrata perfetta, potrebbero essere troncati.")
    
    matrix_data = binary_data[:size**2].reshape((size, size))  # Converte in matrice 2D

    return metadata, matrix_data

def generate_image_from_gcims(matrix_data):
    """
    Genera una heatmap dai dati GC-IMS con colormap Inferno.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(matrix_data, cmap="inferno", aspect="auto", origin="lower")  # "lower" allinea gli assi RT-DT
    plt.colorbar(im, ax=ax, label="Intensità del Segnale")
    plt.xlabel("Tempo di Ritenzione (RT)")
    plt.ylabel("Tempo di Deriva (DT)")
    plt.title("Mappa GC-IMS")

    return fig

# 🏠 **Interfaccia Streamlit**
st.title("Visualizzazione GC-IMS da File .MEA")
st.write("Carica un file .MEA per visualizzare la mappa 2D GC-IMS.")

# 📂 **Caricamento File**
uploaded_file = st.file_uploader("Carica il tuo file .MEA", type=["mea"])

if uploaded_file is not None:
    st.success("✅ File caricato con successo!")

    # 📌 **Lettura del file e separazione dei metadati dai dati binari**
    file_bytes = uploaded_file.read()
    metadata, matrix_data = extract_gcims_data(file_bytes)

    # 📝 **Mostra i metadati**
    with st.expander("📄 Mostra Metadati"):
        st.json(metadata)

    # 🎨 **Generazione dell'immagine GC-IMS**
    if matrix_data is not None:
        st.write("🔍 Generando immagine GC-IMS...")
        image_fig = generate_image_from_gcims(matrix_data)

        # 🖼 **Mostra l'immagine generata**
        st.pyplot(image_fig)
    else:
        st.error("❌ Errore nella generazione dell'immagine. I dati binari non sono validi.")
