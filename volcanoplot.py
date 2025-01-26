import pandas as pd
import streamlit as st
from io import BytesIO
import numpy as np  # Aggiunto per il calcolo di log

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")

    # Caricamento dei dati e selezione dei threshold tramite form
    with st.form(key='my_form'):
        file = st.file_uploader("Carica il file Excel", type=['xlsx'])
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il -log2FoldChange', value=2.0)
        p_value_threshold = st.number_input('Inserisci il valore soglia per il p-value', value=0.05)
        submit_button = st.form_submit_button(label='Applica Filtri')

    # Verifica se il file è stato caricato e il pulsante premuto
    if file is not None and submit_button:
        dati = pd.read_excel(file)  # Assumendo una lettura diretta del file Excel

        # Calcolo del -log10(p-value) per filtrare
        dati['-log10(p-value)'] = -np.log10(dati['p-value'])

        # Filtraggio dei dati secondo le soglie specificate
        dati_preparati = dati[(dati['Log2FoldChange'].abs() >= fold_change_threshold) &
                              (dati['-log10(p-value)'] >= -np.log10(p_value_threshold))]

        # Mostra la tabella dei dati filtrati
        st.write("Variabili che superano i valori soglia inseriti:", dati_preparati)

        # Conversione DataFrame in Excel e creazione di un pulsante di download automatico
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dati_preparati.to_excel(writer, index=False)
            writer.save()
        output.seek(0)

        st.download_button(
            label="Scarica i dati filtrati come Excel",
            data=output,
            file_name='dati_filtrati.xlsx',
            mime='application/vnd.ms-excel'
        )

if __name__ == "__main__":
    main()
