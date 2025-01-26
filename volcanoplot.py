import pandas as pd
import streamlit as st
import io

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

        # Convertire DataFrame in Excel e creare un pulsante di download
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
            dati_preparati.to_excel(writer, sheet_name='Sheet1')
            writer.save()
        towrite.seek(0)  # riposizionamento al principio del file dopo il salvataggio
        b64 = base64.b64encode(towrite.read()).decode()  # codifica in base64
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="dati_filtrati.xlsx">Scarica i dati filtrati</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
