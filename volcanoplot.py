import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
import base64
from io import BytesIO

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

# Funzione per creare e salvare il grafico
def crea_volcano_plot(dati, show_labels):
    if dati is not None:
        fig = px.scatter(dati, x='Log2 Fold Change', y='-log10(p-value)', text='Variabile' if show_labels else None, hover_data=['Variabile'])
        fig.update_traces(textposition='top center')
        fig.update_layout(title='Volcano Plot', xaxis_title='Log2 Fold Change', yaxis_title='-log10(p-value)')
        return fig
    else:
        return None

# Funzione per convertire un grafico Plotly in immagine JPG
def convert_fig_to_image(fig):
    img_bytes = fig.to_image(format="jpg")
    return img_bytes

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")

    # Widget per il caricamento dei file
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    # Form per inserire il p-value e il fold change desiderati
    with st.form(key='my_form'):
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il -log2FoldChange', value=2.0)
        p_value = st.number_input('Inserisci il valore soglia per il p-value', value=0.05, format='%f')
        p_value_threshold = -np.log10(p_value) if p_value > 0 else None  # Convertiamo il p-value in -log10(p-value)
        submit_button = st.form_submit_button(label='Applica Filtri')

    # Opzione per mostrare o nascondere le etichette delle variabili nel grafico
    show_labels = st.checkbox("Mostra etichette delle variabili", value=True)

def download_link(object_to_download, download_filename, download_link_text):
    """
    Genera un link HTML per scaricare un oggetto Python (come DataFrame) come un file.

    Args:
    object_to_download (DataFrame, str, file): L'oggetto da scaricare.
    download_filename (str): il nome del file sotto il quale il file sarà salvato dall'utente.
    download_link_text (str): il testo del link di download mostrato.

    Returns:
    str: una stringa HTML con un link di download.
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)  # Converti il DataFrame in CSV
    b64 = base64.b64encode(object_to_download.encode()).decode()  # Codifica in base64
    return f'<a href="data:file/csv;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
    
    
    if file is not None and submit_button:
        dati = carica_dati(file)
        if dati is not None:
            dati_preparati = prepara_dati(dati, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, show_labels)
                if fig is not None:
                    st.plotly_chart(fig)
                    # Pulsante per scaricare il grafico come immagine JPG
                    img_bytes = convert_fig_to_image(fig)
                    st.download_button(label="Scarica il grafico come JPG", data=img_bytes, file_name="volcano_plot.jpg", mime="image/jpeg")
                    # Link per scaricare il DataFrame come Excel
                    tmp_download_link = download_link(dati_preparati, "dati_significativi.xlsx", "Scarica i dati come Excel")
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
