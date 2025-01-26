import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Funzione per caricare i dati
def carica_dati(file):
    dati = pd.read_excel(file)
    return dati

# Funzione per preparare i dati per il volcano plot
def prepara_dati(dati, fold_change_threshold, p_value_threshold):
    # Calcolo del -log10(p-value)
    dati['-log10(p-value)'] = -np.log10(dati['p-value'])
    
    # Filtraggio in base ai valori soglia
    dati_filtrati = dati[(dati['Log2FoldChange'].abs() >= fold_change_threshold) &
                         (dati['-log10(p-value)'] >= -np.log10(p_value_threshold))]
    return dati_filtrati

# Funzione per creare il volcano plot
def crea_volcano_plot(dati):
    fig = px.scatter(dati, x='Log2FoldChange', y='-log10(p-value)', hover_data=[dati.index])
    return fig

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")

    # Caricamento del file e impostazione dei threshold tramite form
    with st.form(key='form1'):
        file = st.file_uploader("Carica il file Excel", type=['xlsx'])
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il -log2FoldChange', value=1.0)
        p_value_threshold = st.number_input('Inserisci il valore soglia per il p-value', value=0.05)
        submit_button = st.form_submit_button(label='Applica Filtri')
    
    if file and submit_button:
        dati = carica_dati(file)
        dati_filtrati = prepara_dati(dati, fold_change_threshold, p_value_threshold)
        fig = crea_volcano_plot(dati_filtrati)
        st.plotly_chart(fig)
        st.dataframe(dati_filtrati)  # Visualizzazione della tabella delle variabili filtrate

if __name__ == "__main__":
    main()
