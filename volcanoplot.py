import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

def download_link(object_to_download, download_filename, download_link_text):
    """
    Genera un link HTML per scaricare un oggetto pandas DataFrame come Excel.
    """
    if isinstance(object_to_download, pd.DataFrame):
        output = BytesIO()
        object_to_download.to_excel(output, index=False)
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
    return None

def main():
    # Importa il file sorgente .xlsx
    uploaded_file = st.file_uploader("Carica il file Excel", type="xlsx")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.write("Dati caricati con successo!")

        # Configurazione dei parametri tramite form
        with st.form(key='my_form'):
            threshold_pvalue = st.number_input('Inserisci il valore soglia per p-value', min_value=0.0, max_value=1.0, value=0.05)
            threshold_fold_change = st.number_input('Inserisci il valore soglia per fold change', value=1.0)
            submit_button = st.form_submit_button(label='Genera Volcano Plot')

        if submit_button:
            # Filtra i dati in base alle soglie impostate
            filtered_data = data[(data['pvalue'] <= threshold_pvalue) & (abs(data['log2FoldChange']) >= threshold_fold_change)]

            # Creazione del volcano plot
            fig, ax = plt.subplots()
            ax.scatter(filtered_data['log2FoldChange'], -np.log10(filtered_data['pvalue']), c='blue', edgecolors='w')
            ax.set_xlabel('Log2 Fold Change')
            ax.set_ylabel('-Log10(p-value)')
            ax.set_title('Volcano Plot')
            st.pyplot(fig)

            # Link per scaricare il DataFrame come Excel
            if not filtered_data.empty:
                tmp_download_link = download_link(filtered_data, "dati_significativi.xlsx", "Scarica i dati come Excel")
                if tmp_download_link:
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                else:
                    st.error("Errore nella creazione del link di download.")
            else:
                st.error("Nessun dato significativo per il download.")
    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
