import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
import base64
from io import BytesIO

def carica_dati(file, mostra_etichette_caricamento):
    if mostra_etichette_caricamento:
        st.info("Caricamento e lettura del file Excel...")
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
    except ValueError:
        st.error("Il file caricato non ha due livelli di intestazione come richiesto.")
        return None
    if mostra_etichette_caricamento:
        st.success("File caricato con successo!")
    return dati

def prepara_dati(dati, fold_change_threshold, p_value_threshold, mostra_etichette_caricamento):
    if dati is not None and isinstance(dati.columns, pd.MultiIndex):
        if mostra_etichette_caricamento:
            st.info("Elaborazione dei dati per il volcano plot...")
        classi = dati.columns.get_level_values(1).unique()
        risultati = []
        for var in dati.index:
            valori = [dati.loc[var, (dati.columns.get_level_values(1) == classe)].dropna().values for classe in classi]
            if len(valori[0]) > 0 and len(valori[1]) > 0:
                media_diff = np.log2(np.mean(valori[0]) / np.mean(valori[1]))
                t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                if abs(media_diff) >= fold_change_threshold and p_val_log >= p_value_threshold:
                    risultati.append([var, media_diff, p_val_log])
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2 Fold Change', '-log10(p-value)'])
        if mostra_etichette_caricamento:
            st.success("Dati elaborati con successo!")
        return risultati_df
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None

def main():
    st.title("Volcano Plot Interattivo")
    mostra_etichette_caricamento = st.checkbox("Mostra etichette di caricamento", value=True)

    file = st.file_uploader("Carica il file Excel", type=['xlsx'])
    with st.form(key='my_form'):
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il -log2FoldChange', value=2.0)
        p_value = st.number_input('Inserisci il valore soglia per il p-value', value=0.05, format='%f')
        p_value_threshold = -np.log10(p_value) if p_value > 0 else None
        submit_button = st.form_submit_button(label='Applica Filtri')

    show_labels = st.checkbox("Mostra etichette delle variabili nel grafico", value=True)

    if file is not None and submit_button:
        dati = carica_dati(file, mostra_etichette_caricamento)
        if dati is not None:
            dati_preparati = prepara_dati(dati, fold_change_threshold, p_value_threshold, mostra_etichette_caricamento)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, show_labels)
                if fig is not None:
                    st.plotly_chart(fig)
                    img_bytes = convert_fig_to_image(fig)
                    st.download_button(label="Scarica il grafico come JPG", data=img_bytes, file_name="volcano_plot.jpg", mime="image/jpeg")
                    tmp_download_link = download_link(dati_preparati, "dati_significativi.xlsx", "Scarica i dati come Excel")
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
