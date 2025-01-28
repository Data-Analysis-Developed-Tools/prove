import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Funzione per caricare i dati
def carica_dati(file):
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
        classi = dati.columns.get_level_values(1).unique()
        return dati, classi
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {str(e)}")
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
                pval_log2fc = p_val_log * media_diff if p_val_log is not None else None
                risultati.append([var, media_diff, p_val_log, pval_log2fc, media_log[var]])
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2FoldChange', '-log10(p-value)', '-log10(p-value) x Log2FoldChange', 'MediaLog'])
        return risultati_df
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None

# Applica una scala di colore personalizzata
def apply_custom_color_scale(df):
    norm = plt.Normalize(-df['-log10(p-value) x Log2FoldChange'].abs().max(), df['-log10(p-value) x Log2FoldChange'].abs().max())
    color_scale = lambda x: f'background-color: {plt.cm.RdBu_r(norm(x)) if not pd.isnull(x) else "none"}'
    return df.style.applymap(color_scale, subset=['-log10(p-value) x Log2FoldChange'])

# Crea il volcano plot con linee e annotazioni
def crea_volcano_plot(dati, classi, show_labels, size_by_media, color_by_media):
    if dati is not None:
        size = None
        color = None
        if size_by_media:
            size = np.power(10, dati['MediaLog'] - dati['MediaLog'].min()) / (np.power(10, dati['MediaLog'].max()) - np.power(10, dati['MediaLog'].min())) * 100
        if color_by_media:
            color = dati['MediaLog']
        fig = px.scatter(dati, x='Log2FoldChange', y='-log10(p-value)', text='Variabile' if show_labels else None,
                         hover_data=['Variabile'], size=size, color=color,
                         color_continuous_scale='RdYlBu_r', size_max=30)
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
            size_by_media = st.checkbox("Dimensiona punti per media valori assoluti inter-tesi", value=False)
            color_by_media = st.checkbox("Colora punti per media dei valori assoluti inter-tesi", value=False)
            dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, classi, show_labels, size_by_media, color_by_media)
                st.plotly_chart(fig)
                st.write("Dati visibili attualmente nel grafico:")
                html = apply_custom_color_scale(dati_preparati).render()
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.error("Nessun dato preparato per il grafico.")
        else:
            st.error("Dati non caricati correttamente.")
    else:
        st.warning("Si prega di caricare un file Excel.")

if __name__ == "__main__":
    main()
