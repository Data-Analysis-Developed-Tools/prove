import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import base64
import os

def create_download_link(df, filename):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def main():
    uploaded_file = st.file_uploader("Carica il file Excel", type="xlsx")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        # Verifica che le colonne necessarie siano presenti nel DataFrame
        required_columns = ['pvalue', 'log2FoldChange']
        if not all(column in data.columns for column in required_columns):
            st.error(f"Errore: il file deve contenere le seguenti colonne: {', '.join(required_columns)}")
            return
        st.write("Dati caricati con successo!")

        # Preparazione dei dati per il nuovo file Excel
        output_df = pd.DataFrame({
            'Etichette': data.iloc[:, 0],  # Presumendo che la prima colonna contenga le etichette
            'log2FoldChange': data['log2FoldChange'],
            '-log10(pvalue)': -np.log10(data['pvalue']),
            'p-value': data['pvalue']
        })

        # Creazione del link di download per il nuovo file Excel
        file_name = os.path.splitext(uploaded_file.name)[0] + "_values_from_volcano_plot.xlsx"
        link = create_download_link(output_df, file_name)
        st.markdown(link, unsafe_allow_html=True)

    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
