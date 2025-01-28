import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
import base64
from io import BytesIO
import plotly.graph_objects as go  # Import per le funzioni aggiuntive di Plotly

# Funzione per caricare i dati
def carica_dati(file):
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
    except ValueError:
        st.error("Il file caricato non ha due livelli di intestazione come richiesto.")
        return None
    return dati

# Preparazione dei dati per il volcano plot
def prepara_dati(dati, fold_change_threshold, p_value_threshold):
    if dati is not None and isinstance(dati.columns, pd.MultiIndex):
        classi = dati.columns.get_level_values(1).unique()
        risultati = []
        for var in dati.index:
            valori = [dati.loc[var, dati.columns.get_level_values(1) == classe].dropna().values for classe in classi]
            if len(valori[0]) > 0 and len(valori[1]) > 0:
                media_diff = np.log2(np.mean(valori[0]) / np.mean(valori[1]))
                t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                if abs(media_diff) >= fold_change_threshold and p_val_log >= p_value_threshold:
                    risultati.append([var, media_diff, p_val_log])
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2 Fold Change', '-log10(p-value)'])
        return risultati_df, classi
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None, None

# Funzione per creare e salvare il grafico
def crea_volcano_plot(dati, show_labels, classi):
    if dati is not None:
        fig = px.scatter(
            dati,
            x='Log2 Fold Change',
            y='-log10(p-value)',
            text='Variabile' if show_labels else None,
            hover_data=['Variabile']
        )
        # Aggiungi una linea verticale al valore 0 dell'asse x
        fig.add_shape(
            type='line',
            x0=0, y0=0,
            x1=0, y1=dati['-log10(p-value)'].max(),
            line=dict(color='Orange', width=3)
        )
        # Aggiungi etichette per le classi
        fig.add_annotation(
            x=dati['Log2 Fold Change'].min(), y=dati['-log10(p-value)'].max(),
            text=f"Sovra-espressione in {classi[1]}",
            showarrow=False,
            xanchor='left',
            yanchor='top'
        )
        fig.add_annotation(
            x=dati['Log2 Fold Change'].max(), y=dati['-log10(p-value)'].max(),
            text=f"Sovra-espressione in {classi[0]}",
            showarrow=False,
            xanchor='right',
            yanchor='top'
        )
        # Aggiorna layout del grafico
        fig.update_layout(
            title='Volcano Plot',
            xaxis_title='Log2 Fold Change',
            yaxis_title='-log10(p-value)'
        )
        return fig
    else:
        return None

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")

    # Widget per il caricamento dei file
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    # Form per inserire il p-value e il fold change desiderati
    with st.form(key='my_form'):
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il Log2FoldChange', value=2.0)
        p_value = st.number_input('Inserisci il valore soglia per il p-value', value=0.05, format='%f')
        p_value_threshold = -np.log10(p_value) if p_value > 0 else None
        submit_button = st.form_submit_button(label='Applica Filtri')

    # Opzione per mostrare o nascondere le etichette delle variabili nel grafico
    show_labels = st.checkbox("Mostra etichette delle variabili", value=True)

    if file is not None and submit_button:
        dati, classi = carica_dati(file)
        if dati is not None:
            dati_preparati, classi = prepara_dati(dati, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, show_labels, classi)
                if fig is not None:
                    st.plotly_chart(fig)
    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
