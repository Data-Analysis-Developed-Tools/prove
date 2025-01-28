import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
import plotly.graph_objects as go

# Funzione per caricare i dati
def carica_dati(file):
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
        classi = dati.columns.get_level_values(1).unique()
        return dati, classi
    except ValueError:
        st.error("Il file caricato non ha due livelli di intestazione come richiesto.")
        return None, None

# Preparazione dei dati per il volcano plot
def prepara_dati(dati, classi, fold_change_threshold, p_value_threshold):
    if dati is not None:
        risultati = []
        for var in dati.index:
            valori = [dati.loc[var, dati.columns.get_level_values(1) == classe].dropna().values for classe in classi]
            if len(valori[0]) > 0 and len(valori[1]) > 0:
                media_diff = np.log2(np.mean(valori[0]) / np.mean(valori[1]))
                t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                if abs(media_diff) >= fold_change_threshold and p_val_log >= p_value_threshold:
                    risultati.append([var, media_diff, p_val_log])
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2FoldChange', '-log10(p-value)'])
        return risultati_df
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None

# Crea il volcano plot
def crea_volcano_plot(dati, classi, show_labels):
    if dati is not None:
        fig = px.scatter(dati, x='Log2FoldChange', y='-log10(p-value)', text='Variabile' if show_labels else None,
                         hover_data=['Variabile'])
        fig.update_layout(title='Volcano Plot', xaxis_title='Log2FoldChange', yaxis_title='-log10(p-value)')
        return fig
    else:
        return None

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    if file is not None:
        dati, classi = carica_dati(file)
        if dati is not None:
            fold_change_threshold = st.number_input('Inserisci il valore soglia per il Log2FoldChange', value=0.0)
            p_value_threshold = st.number_input('Inserisci il valore soglia per il -log10(p-value)', value=0.05)
            show_labels = st.checkbox("Mostra etichette delle variabili", value=True)
            dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, classi, show_labels)
                st.plotly_chart(fig, use_container_width=True)
                
                # Input for selected indices
                selected_indices = st.text_input("Enter indices of selected points", "")
                if selected_indices:
                    selected_indices = list(map(int, selected_indices.split(',')))
                    selected_data = dati_preparati.iloc[selected_indices]
                    st.write("Selected Data:")
                    st.dataframe(selected_data)
            else:
                st.error("Nessun dato preparato per il grafico.")
        else:
            st.error("Dati non caricati correttamente.")

if __name__ == "__main__":
    main()
