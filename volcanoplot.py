import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO
import base64
import os

def create_download_link(df, filename):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def main():
    uploaded_file = st.file_uploader("Carica il file Excel", type="xlsx")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.write("Dati caricati con successo!")

        # Setpoint e visualizzazione tramite form
        with st.form(key='my_form'):
            threshold_pvalue = st.number_input('Inserisci il valore soglia per p-value', min_value=0.0, max_value=1.0, value=0.05)
            threshold_fold_change = st.number_input('Inserisci il valore soglia per fold change', value=1.0)
            show_labels = st.checkbox("Mostra etichette")
            submit_button = st.form_submit_button(label='Genera Volcano Plot')

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

# Funzione per generare un link di download per il file DataFrame
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_excel(BytesIO(), index=False)
    b64 = base64.b64encode(object_to_download).decode()
    return f'<a href="data:file/xls;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")

            # Preparazione dei dati per il nuovo file Excel
            output_df = pd.DataFrame({
                'Etichette': data.iloc[:, 0],  # Presumendo che la prima colonna contenga le etichette
                'log2FoldChange': simulated_log2FoldChange,
                '-log10(pvalue)': -np.log10(simulated_pvalues),
                'p-value': simulated_pvalues
            })

            # Creazione del link di download per il nuovo file Excel
            file_name = os.path.splitext(uploaded_file.name)[0] + "_values_from_volcano_plot.xlsx"
            link = create_download_link(output_df, file_name)
            st.markdown(link, unsafe_allow_html=True)

    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
