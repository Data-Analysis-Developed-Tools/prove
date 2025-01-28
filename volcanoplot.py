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

# Crea il volcano plot con linee e annotazioni
def crea_volcano_plot(dati, classi, show_labels, size_by_media, color_by_media, point_size_scale, point_size_variance):
    if dati is not None:
        # Applichiamo l'esponenziale di 10 per amplificare le differenze nelle dimensioni
        size = (np.power(10, dati['MediaLog'] - dati['MediaLog'].min()) / (np.power(10, dati['MediaLog'].max()) - np.power(10, dati['MediaLog'].min())) * point_size_scale) * point_size_variance if size_by_media else None
        color = dati['MediaLog'] if color_by_media else None
        fig = px.scatter(dati, x='Log2FoldChange', y='-log10(p-value)', text='Variabile' if show_labels else None,
                         hover_data=['Variabile'], size=size, color=color,
                         color_continuous_scale='RdYlBu_r',
                         size_max=50)
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, dati['-log10(p-value)'].max()], mode='lines', line=dict(color='orange', width=2)))
        fig.add_annotation(x=-2, y=dati['-log10(p-value)'].max()*1.05, text=f"Over-expression in {classi[1]}", showarrow=False, font=dict(color="red", size=16))
        fig.add_annotation(x=2, y=dati['-log10(p-value)'].max()*1.05, text=f"Over-expression in {classi[0]}", showarrow=False, font=dict(color="green", size=16))
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
            if size_by_media:
                point_size_scale = st.slider("Scala dimensione punti", min_value=1, max_value=100, value=30)
                point_size_variance = st.slider("Varianza dimensionale dei punti", min_value=1, max_value=200, value=50)
            else:
                point_size_scale = 30
                point_size_variance = 50
            dati_preparati = prepara_dati(dati, classi, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, classi, show_labels, size_by_media, color_by_media, point_size_scale, point_size_variance)
                st.plotly_chart(fig)
                # Visualizza i dati sotto il grafico in forma di tabella interattiva
                st.write("Dati visibili attualmente nel grafico:")
                st.dataframe(dati_preparati.style.applymap(lambda x: f'background-color: {"#FF0000" if x > 0 else "#0000FF" if x < 0 else "#FFFFFF"}', subset=['-log10(p-value) x Log2FoldChange']))
            else:
                st.error("Nessun dato preparato per il grafico.")
        else:
            st.error("Dati non caricati correttamente.")
    else:
        st.warning("Si prega di caricare un file Excel.")

if __name__ == "__main__":
    main()
