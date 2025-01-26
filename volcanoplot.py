import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np

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
        return risultati_df
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None

# Crea il volcano plot
def crea_volcano_plot(dati):
    if dati is not None:
        fig = px.scatter(dati, x='Log2 Fold Change', y='-log10(p-value)', text='Variabile', hover_data=['Variabile'])
        fig.update_traces(textposition='top center')
        fig.update_layout(title='Volcano Plot', xaxis_title='Log2 Fold Change', yaxis_title='-log10(p-value)')
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
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il -log2FoldChange', value=2.0)
        p_value_threshold = st.number_input('Inserisci il valore soglia per il -log10(p-value)', value=-np.log10(0.05))
        submit_button = st.form_submit_button(label='Applica Filtri')

    if file is not None and submit_button:
        dati = carica_dati(file)
        if dati is not None:
            dati_preparati = prepara_dati(dati, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati)
                if fig is not None:
                    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
