from google.colab import files
import pandas as pd
import io
import gc_ims
import matplotlib.pyplot as plt
import numpy as np

# Installazione della libreria gc-ims-tools se non presente
!pip install gc-ims-tools

# Passaggio 1: Caricamento del file da PC
uploaded = files.upload()

# Ottenere il nome del file caricato
time_series_filename = list(uploaded.keys())[0]
print(f"File caricato: {time_series_filename}")

# Passaggio 2: Lettura del file .mea con gc-ims-tools
try:
    time_series = gc_ims.load_time_series(time_series_filename)
    print("File .mea caricato con successo!")
except Exception as e:
    print(f"Errore nel caricamento del file: {e}")

# Passaggio 3: Visualizzazione dei dati
print("Anteprima dei dati:")
print(time_series.head())

# Passaggio 4: Analisi basilare
print("\nStatistiche descrittive:")
print(time_series.describe())

# Passaggio 5: Visualizzazione dei dati con Matplotlib
plt.figure(figsize=(10, 5))
plt.plot(time_series.index, time_series.iloc[:, 0], label='Segnale GC-IMS')
plt.xlabel("Tempo")
plt.ylabel("Intensità")
plt.title("Segnale GC-IMS nel tempo")
plt.legend()
plt.show()

# Passaggio 6: Esempio di preprocessing (normalizzazione dei dati)
time_series_normalized = (time_series - time_series.min()) / (time_series.max() - time_series.min())
print("Dati normalizzati:")
print(time_series_normalized.head())

# Passaggio 7: Salvataggio dei dati preprocessati per utilizzo futuro
time_series_normalized.to_csv("time_series_normalized.csv")
print("Dati preprocessati salvati in 'time_series_normalized.csv'")
