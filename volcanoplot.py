import pandas as pd
import streamlit as st
from io import BytesIO

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

        # Qui va il codice per preparare i dati usando i threshold inseriti
        # ... codice per preparare i dati ...
        
        # Assumiamo che 'dati_preparati' sia il DataFrame filtrato da visualizzare
        dati_preparati = dati  # Questa linea è solo illustrativa

        # Mostra i dati preparati
        st.write(dati_preparati)

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
