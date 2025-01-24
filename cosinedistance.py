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
        df = pd.read_excel(uploaded_file)
    
    # Puoi ora utilizzare il DataFrame 'df' per le tue operazioni
    st.write(df)


# Spiegazione del codice:
# - `pandas` è usato per gestire i dati in formato tabellare (dataframe).
# - `numpy` è utilizzato per operazioni numeriche.
# - `scipy.spatial.distance.cosine` calcola la distanza di coseno tra vettori.

# Caricamento del file Excel o CSV (assicurarsi di caricare il file su Colab)
# Supponiamo che il file sia chiamato "data.xlsx" e che si trovi nella cartella principale di Colab.
# Puoi caricare il file da Google Drive o tramite l'interfaccia di upload.
from google.colab import files
uploaded = files.upload()

# Una volta caricato, leggiamo il file in un DataFrame di pandas.
# Sostituire "data.xlsx" con il nome del file caricato.
file_name = list(uploaded.keys())[0]
df = pd.read_excel(file_name)

# Esploriamo i primi dati per verificare che il caricamento sia avvenuto correttamente.
print("Anteprima dei dati:")
print(df.head())

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

print("\nMatrice delle distanze di coseno reciproche:")
print(cosine_distance_df)

# Calcolo della distanza di coseno rispetto alla prima osservazione (riga 2 nel file, indice 0 nel data)
first_observation = data[0]  # Vettore della prima osservazione
distances_to_first = [cosine(first_observation, data[i]) for i in range(len(data))]

# Creiamo un DataFrame per visualizzare queste distanze
distances_to_first_df = pd.DataFrame({
    "Osservazione": observation_labels,
    "Distanza rispetto alla prima": distances_to_first
})

print("\nDistanze di coseno rispetto alla prima osservazione:")
print(distances_to_first_df)

# Esportiamo i risultati in un file Excel per un report completo
output_file = "cosine_distances_report.xlsx"

with pd.ExcelWriter(output_file) as writer:
    cosine_distance_df.to_excel(writer, sheet_name="Matrice_distanze", index=True)
    distances_to_first_df.to_excel(writer, sheet_name="Distanze_prima", index=False)

print(f"\nReport salvato nel file: {output_file}")

# Forniamo un link per scaricare il file generato
from google.colab import files
files.download(output_file)
