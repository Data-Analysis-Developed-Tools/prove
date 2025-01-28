import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
import plotly.graph_objects as go
from matplotlib import colors
import matplotlib.pyplot as plt

# Definizione delle altre funzioni come carica_dati ecc. (omesso per brevità)

# Aggiunta della funzione di colorazione condizionale
def apply_color(val):
    color = 'white'  # default for zero
    if val < 0:
        color = 'blue'
    elif val > 0:
        color = 'red'
    return f'background-color: {color}'

# Modifica di prepara_dati e crea_volcano_plot (omesso per brevità)

def main():
    st.title("Volcano Plot Interattivo")
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    if file is not None:
        dati, classi = carica_dati(file)
        if dati is not None:
            fold_change_threshold = st.number_input('Inserisci il valore soglia per il Log2FoldChange', value=0.0)
            p_value_threshold = st.number_input('Inserisci il valore soglia per il -log10(p-value)', value=0.05)
            show_labels = st.checkbox("Mostra etichette delle variabili", value=True)
            size_by_media = st.checkbox("Dimensiona punti per media valori assoluti inter-tesi", value=False)
            color_by_media = st.checkbox("Colora punti per media dei valori assoluti inter-tesi", value=False)
            dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, classi, show_labels, size_by_media, color_by_media)
                st.plotly_chart(fig)
                # Visualizza i dati sotto il grafico in forma di tabella con colorazione condizionata
                st.write("Dati visibili attualmente nel grafico:")
                st.dataframe(dati_preparati.style.applymap(apply_color, subset=['-log10(p-value) x Log2FoldChange']))
            else:
                st.error("Nessun dato preparato per il grafico.")
        else:
            st.error("Dati non caricati correttamente.")

if __name__ == "__main__":
    main()
