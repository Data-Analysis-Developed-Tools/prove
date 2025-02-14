import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def process_mea_file(file):
    """Legge il file .mea e lo converte in una matrice di dati numerici."""
    raw_data = np.frombuffer(file.read(), dtype=np.uint8)  # Legge il file come dati binari
    size = int(np.sqrt(len(raw_data)))  # Calcola la dimensione per una matrice quadrata approssimata
    matrix_data = raw_data[:size**2].reshape((size, size))  # Converte in matrice 2D
    return matrix_data

# Interfaccia Streamlit
st.title("Visualizzazione File .MEA")
st.write("Carica un file .mea e visualizza la sua rappresentazione con colorazione virtuale.")

# Pulsante per il caricamento del file
uploaded_file = st.file_uploader("Carica il tuo file .MEA", type=["mea"])

if uploaded_file is not None:
    st.success("File caricato con successo! Generando immagine...")

    # Processa il file e ottiene i dati
    data_matrix = process_mea_file(uploaded_file)

    # Genera la visualizzazione con colorazione inferno
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(data_matrix, cmap="inferno", aspect="auto")
    plt.colorbar(im, ax=ax, label="Intensità del Segnale")
    plt.title("Mappa di Colorazione Virtuale")

    # Mostra l'immagine in Streamlit
    st.pyplot(fig)
