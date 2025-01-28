import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def color_scale(value):
    """Restituisce il colore in formato HEX in base al valore."""
    norm = plt.Normalize(-abs(value).max(), abs(value).max())
    colormap = plt.cm.RdBu
    if pd.isna(value):
        return f"background-color: #f1f1f1"  # Grigio per NaN
    else:
        # Calcola il colore corrispondente al valore normalizzato
        rgb = colormap(norm(value), bytes=True)[:3]
        color = '#{:02x}{:02x}{:02x}'.format(*rgb)
        return f"background-color: {color}"

def apply_color_scale(df):
    return df.style.applymap(color_scale, subset=['-log10(p-value) x Log2FoldChange']).render()

# Altre funzioni rimangono invariate

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
                # Visualizza i dati sotto il grafico in forma di tabella
                st.write("Dati visibili attualmente nel grafico:")
                html = apply_color_scale(dati_preparati)
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.error("Nessun dato preparato per il grafico.")
        else:
            st.error("Dati non caricati correttamente.")
    else:
        st.warning("Si prega di caricare un file Excel.")

if __name__ == "__main__":
    main()
