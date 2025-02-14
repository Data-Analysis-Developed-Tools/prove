import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from gc-ims-tools import MeaMeasurement  # Importa il pacchetto per leggere i .MEA

def load_mea_file(file):
    """
    Carica il file .MEA utilizzando gc-ims-tools e restituisce la matrice GC-IMS.
    """
    with open(file, "rb") as f:
        mea = MeaMeasurement(f)  # Carica il file .MEA correttamente

    # Ottiene la matrice di intensità (RT x DT)
    intensity_matrix = mea.intensity
    rt_values = mea.rt_values  # Tempo di ritenzione (asse Y)
    dt_values = mea.dt_values  # Tempo di deriva (asse X)

    return intensity_matrix, rt_values, dt_values

def plot_gcims_image(intensity_matrix, rt_values, dt_values, gamma):
    """
    Genera l'immagine GC-IMS con colormap Inferno e regolazione del contrasto.
    """
    # Normalizzazione dei dati per il miglior contrasto
    matrix = intensity_matrix - np.min(intensity_matrix)
    matrix /= np.max(matrix)  # Porta i valori tra 0 e 1
    matrix = matrix ** gamma  # Correzione gamma per regolare il contrasto

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(matrix, cmap="inferno", aspect="auto", origin="lower",
                   extent=[dt_values[0], dt_values[-1], rt_values[0], rt_values[-1]])
    plt.colorbar(im, ax=ax, label="Intensità del Segnale")
    plt.ylabel("Tempo di Ritenzione (RT) [s]")  
    plt.xlabel("Tempo di Deriva (DT) [ms]")      
    plt.title("Mappa GC-IMS (RT vs DT) - Regolabile")

    return fig

# 🏠 **Interfaccia Streamlit**
st.title("Visualizzazione GC-IMS da File .MEA")
st.write("Carica un file .MEA per visualizzare la mappa 2D GC-IMS.")

# 📂 **Caricamento File**
uploaded_file = st.file_uploader("Carica il tuo file .MEA", type=["mea"])

if uploaded_file is not None:
    st.success("✅ File caricato con successo!")

    # 📌 **Lettura del file con gc-ims-tools**
    try:
        intensity_matrix, rt_values, dt_values = load_mea_file(uploaded_file)

        # 🎚 **Cursore per regolazione contrasto (Gamma Correction)**
        gamma_value = st.slider(
            "Regola il contrasto dell'immagine (gamma)", 
            min_value=0.1, max_value=3.0, value=1.0, step=0.1, format="%.1f"
        )

        # 🎨 **Generazione dell'immagine GC-IMS**
        st.write("🔍 Generando immagine GC-IMS con regolazione contrasto...")
        image_fig = plot_gcims_image(intensity_matrix, rt_values, dt_values, gamma_value)

        # 🖼 **Mostra l'immagine generata**
        st.pyplot(image_fig)

    except Exception as e:
        st.error(f"❌ Errore durante la lettura del file .MEA: {e}")
