import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import plotly.express as px
from scipy.stats import ttest_ind
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

# Calcola la media per ogni variabile e il suo logaritmo in base 10
def calcola_media_log(dati):
    media = dati.mean(axis=1)
    return np.log10(media + 1)  # Aggiungi 1 per evitare logaritmo di zero

# Preparazione dei dati per il volcano plot
def prepara_dati(dati, classi, fold_change_threshold, p_value_threshold):
    if dati is not None:
        media_log = calcola_media_log(dati.iloc[:, 1:])
        risultati = []
        for var in dati.index:
            valori = [dati.loc[var, dati.columns.get_level_values(1) == classe].dropna().values for classe in classi]
            if len(valori[0]) > 0 and len(valori[1]) > 0:
                media_diff = np.log2(np.mean(valori[0]) / np.mean(valori[1]))
                t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                log10_pval_log2fc = p_val_log * media_diff
                risultati.append([var, media_diff, p_val_log, log10_pval_log2fc])
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2FoldChange', '-log10(p-value)', '-log10(p-value x Log2FoldChange)'])
        return risultati_df
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None

# Crea il volcano plot con linee e annotazioni
def crea_volcano_plot(dati, classi, show_labels):
    if dati is not None:
        fig = px.scatter(dati, x='Log2FoldChange', y='-log10(p-value)', text='Variabile' if show_labels else None,
                         hover_data=['Variabile'])
        fig.update_layout(title='Volcano Plot', xaxis_title='Log2FoldChange', yaxis_title='-log10(p-value)')
        return fig
    else:
        return None

# Colora le celle della tabella
def colora_celle(val):
    norm = mcolors.TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
    rgba = mcolors.to_hex(mcolors.to_rgba(mcolors.TABLEAU_COLORS['tab:blue'], norm(val)))
    return f'background-color: {rgba}'

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    # Form per inserire i threshold
    with st.form(key='my_form'):
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il Log2FoldChange', value=0.0)
        p_value_threshold = st.number_input('Inserisci il valore soglia per il -log10(p-value)', value=0.05)
        submit_button = st.form_submit_button(label='Applica Filtri')

    if file is not None and submit_button:
        dati, classi = carica_dati(file)
        if dati is not None:
            dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, classi, True)
                if fig is not None:
                    st.plotly_chart(fig)
                    # Mostra la tabella con colorazione
                    st.dataframe(dati_preparati.style.applymap(colora_celle, subset=['-log10(p-value x Log2FoldChange)']))
                else:
                    st.error("Il grafico non contiene dati da visualizzare.")
            else:
                st.error("Nessun dato preparato per il grafico.")
        else:
            st.error("Dati non caricati correttamente.")

if __name__ == "__main__":
    main()
