import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np

# Funzione per caricare i dati
def carica_dati(file):
    dati = pd.read_excel(file, header=[0, 1], index_col=0)
    return dati

# Preparazione dei dati per il volcano plot
def prepara_dati(dati):
    classi = dati.columns.get_level_values(1).unique()
    risultati = []
    for var in dati.index:
        valori = [dati.loc[var, dati.columns.get_level_values(1) == classe].dropna().values for classe in classi]
        if len(valori[0]) > 0 and len(valori[1]) > 0:
            media_diff = np.mean(valori[0]) - np.mean(valori[1])
            t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
            risultati.append([var, media_diff, -np.log10(p_val) if p_val > 0 else None])
    risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Differenza Media', '-log10(p-value)'])
    return risultati_df

# Crea il volcano plot
def crea_volcano_plot(dati):
    fig = px.scatter(dati, x='Differenza Media', y='-log10(p-value)', text='Variabile', hover_data=['Variabile'])
    fig.update_traces(textposition='top center')
    fig.update_layout(title='Volcano Plot', xaxis_title='Differenza Media', yaxis_title='-log10(p-value)')
    return fig

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])
    if file is not None:
        dati = carica_dati(file)
        dati_preparati = prepara_dati(dati)
        fig = crea_volcano_plot(dati_preparati)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
