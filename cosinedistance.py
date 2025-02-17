# Importiamo le librerie necessarie
import pandas as pd
import numpy as np
import streamlit as st
from scipy.spatial.distance import cosine

# Creazione di un widget per il caricamento dei file
uploaded_file = st.file_uploader("Carica un file CSV o Excel", type=["csv", "xlsx"])
if uploaded_file is not None:
    # Verifica il tipo di file per caricare correttamente
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Visualizzazione del DataFrame caricato
    st.write("Anteprima dei dati:", df)

    # Separazione delle descrizioni delle osservazioni e delle variabili numeriche
    # Supponiamo che le descrizioni siano nella colonna "A" e i dati numerici nelle colonne dalla "B" in poi.
    # Convertiamo tutto in un formato numerico per calcoli corretti.
    observation_labels = df.iloc[:, 0]  # Colonna A: descrizioni delle osservazioni
    data = df.iloc[:, 1:].values  # Colonne numeriche (dalla B in poi)

    # Normalizzazione dei dati
    # La distanza di coseno si basa su vettori, quindi è importante verificare che i dati siano già numerici.
    # Se ci sono valori NaN o non numerici, li sostituiremo con 0 (o un valore più appropriato).
    data = np.nan_to_num(data)

    # Funzione per calcolare la matrice delle distanze di coseno
    def calculate_cosine_distances(data):
        """
        Calcola la matrice delle distanze di coseno reciproche.
        """
        n = data.shape[0]  # Numero di osservazioni
        distance_matrix = np.zeros((n, n))  # Matrice quadrata vuota

        for i in range(n):
            for j in range(n):
                if i != j:  # Non calcoliamo la distanza di un vettore con se stesso
                    distance_matrix[i, j] = cosine(data[i], data[j])
                else:
                    distance_matrix[i, j] = 0.0  # La distanza di un vettore con se stesso è zero
        return distance_matrix

    # Calcoliamo la matrice delle distanze di coseno
    cosine_distance_matrix = calculate_cosine_distances(data)

    # Creiamo un DataFrame per visualizzare la matrice delle distanze
    cosine_distance_df = pd.DataFrame(
        cosine_distance_matrix,
        index=observation_labels,
        columns=observation_labels
    )

    # Visualizzazione della matrice delle distanze
    st.write("Matrice delle distanze di coseno reciproche:", cosine_distance_df)

    # Calcolo della distanza di coseno rispetto alla prima osservazione (riga 2 nel file, indice 0 nel data)
    first_observation = data[0]  # Vettore della prima osservazione
    distances_to_first = [cosine(first_observation, data[i]) for i in range(len(data))]

    # Creiamo un DataFrame per visualizzare queste distanze
    distances_to_first_df = pd.DataFrame({
        "Osservazione": observation_labels,
        "Distanza rispetto alla prima": distances_to_first
    })

    st.write("Distanze di coseno rispetto alla prima osservazione:", distances_to_first_df)

    # Esportiamo i risultati in un file Excel per un report completo
    output_file = "cosine_distances_report.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        cosine_distance_df.to_excel(writer, sheet_name="Matrice_distanze", index=True)
        distances_to_first_df.to_excel(writer, sheet_name="Distanze_prima", index=False)

    # Forniamo un link per scaricare il file generato
    with open(output_file, "rb") as file:
        st.download_button(label="Scarica il report delle distanze", data=file, file_name=output_file)
