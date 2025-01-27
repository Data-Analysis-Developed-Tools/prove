import streamlit as st
import pandas as pd
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

        # Simulazione dei dati di pvalue e log2FoldChange per dimostrazione
        num_rows = len(data)
        simulated_log2FoldChange = np.random.normal(0, 1, num_rows)
        simulated_pvalues = np.random.uniform(0, 0.05, num_rows)

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
