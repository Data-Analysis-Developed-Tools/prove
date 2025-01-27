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
    # Simuliamo dei dati per il volcano plot
    data = pd.DataFrame({
        'log2FoldChange': np.random.normal(0, 1, 100),
        'pvalue': np.random.uniform(0, 0.05, 100)
    })
    data['-log10(pvalue)'] = -np.log10(data['pvalue'])

    # Aggiungiamo una colonna per le etichette
    data['label'] = ['gene' + str(i) for i in range(100)]

    # Opzione per mostrare/nascondere le etichette
    show_labels = st.checkbox("Mostra etichette")

    # Creazione del volcano plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(data['log2FoldChange'], data['-log10(pvalue)'], c='blue', edgecolors='w')

    if show_labels:
        for i in range(data.shape[0]):
            ax.text(data.iloc[i]['log2FoldChange'], data.iloc[i]['-log10(pvalue)'], data.iloc[i]['label'], fontsize=9)

    ax.set_xlabel('Log2 Fold Change')
    ax.set_ylabel('-Log10(p-value)')
    ax.set_title('Volcano Plot')
    st.pyplot(fig)

    # Link per scaricare il DataFrame come Excel
    if not data.empty:
        tmp_download_link = download_link(data, "dati_significativi.xlsx", "Scarica i dati come Excel")
        if tmp_download_link:
            st.markdown(tmp_download_link, unsafe_allow_html=True)
        else:
            st.error("Errore nella creazione del link di download.")
    else:
        st.error("Nessun dato disponibile per il download.")

if __name__ == "__main__":
    main()
