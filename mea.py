import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def extract_gcims_data(file_bytes):
    """
    Estrae i metadati e i dati binari da un file .MEA relativo a GC-IMS.
    - I metadati contengono informazioni sperimentali.
    - I dati binari rappresentano la matrice 2D reale, senza imporre forme arbitrarie.
    """
    file_text = file_bytes.decode("utf-8", errors="ignore")  
    lines = file_text.splitlines()

    metadata = {}
    binary_start = None

    # 🔍 **Separazione metadati e dati binari**
    for i, line in enumerate(lines):
        if "=" in line:  # Cerca le linee con formato "chiave = valore"
            key, value = map(str.strip, line.split("=", 1))
            metadata[key] = value
        elif binary_start is None and not line.strip():  
            binary_start = i + 1  # Trova la prima riga vuota (separatore dati)
            break  

    if binary_start is None:
        st.error("❌ Errore: impossibile identificare l'inizio dei dati binari.")
        return metadata, None

    # 📌 **Estrazione dati binari senza ipotesi di formato**
    raw_data = file_bytes[binary_start:].strip()
    
    # **Provo diversi formati numerici**
    try:
        binary_data = np.frombuffer(raw_data, dtype=np.float32)
    except ValueError:
        try:
            binary_data = np.frombuffer(raw_data, dtype=np.int16)
        except ValueError:
            st.error("❌ Errore: impossibile leggere i dati binari in float32 o int16.")
            return metadata, None

    # 🔎 **Analisi della distribuzione dei dati**
    data_min, data_max, data_mean = np.min(binary_data), np.max(binary_data), np.mean(binary_data)
    st.write(f"📊 Dati GC-IMS: Min={data_min}, Max={data_max}, Media={data_mean}")

    # 📏 **Determinazione dinamica della forma della matrice**
    possible_shapes = [(x, len(binary_data) // x) for x in range(10, 1000) if len(binary_data) % x == 0]

    if not possible_shapes:
        st.error("❌ Impossibile trovare una forma valida per la matrice GC-IMS.")
        return metadata, None

    # Sceglie la forma più vicina a una matrice "rettangolare"
    best_shape = min(possible_shapes, key=lambda s: abs(s[0] - s[1]))

    # Reshape senza forzare dimensioni arbitrarie
    matrix_data = binary_data.reshape(best_shape)

    return metadata, matrix_data

def generate_image_from_gcims(matrix_data):
    """
    Genera una heatmap dai dati GC-IMS con colormap Inferno.
    Non impone una forma, ma usa la matrice reale.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(matrix_data, cmap="inferno", aspect="auto", origin="lower")  
    plt.colorbar(im, ax=ax, label="Intensità del Segnale")
    plt.ylabel("Tempo di Ritenzione (RT)")  
    plt.xlabel("Tempo di Deriva (DT)")      
    plt.title("Mappa GC-IMS (RT vs DT)")

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
