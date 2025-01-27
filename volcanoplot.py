import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO
import base64

def main():
    uploaded_file = st.file_uploader("Carica il file Excel", type="xlsx")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.write("Dati caricati con successo!")

        with st.form(key='my_form'):
            threshold_pvalue = st.number_input('Inserisci il valore soglia per p-value', min_value=0.0, max_value=1.0, value=0.05)
            threshold_fold_change = st.number_input('Inserisci il valore soglia per fold change', value=1.0)
            submit_button = st.form_submit_button(label='Genera Volcano Plot e scarica i dati')

        if submit_button:
            # Simulazione dei dati per il volcano plot
            data['log2FoldChange'] = np.random.normal(0, 1, len(data))
            data['pvalue'] = np.random.uniform(0.001, 1, len(data))
            data['-log10(pvalue)'] = -np.log10(data['pvalue'])

            # Filtra i dati in base alle soglie impostate
            filtered_data = data[(data['pvalue'] <= threshold_pvalue) & (abs(data['log2FoldChange']) >= threshold_fold_change)]

            # Creazione del volcano plot
            fig = px.scatter(
                data_frame=filtered_data,
                x='log2FoldChange',
                y='-log10(pvalue)',
                hover_data=[data.columns[0], 'pvalue', 'log2FoldChange'],
                title="Volcano Plot",
                labels={
                    "-log10(pvalue)": "-log10(p-value)",
                    "log2FoldChange": "Log2 Fold Change"
                }
            )
            fig.add_vline(x=0, line_dash="dash", line_color="red")
            fig.update_traces(marker=dict(size=5))  # Ridurre la dimensione dei marker a metà
            st.plotly_chart(fig, use_container_width=True)

            # Funzione per generare il download link per Excel
            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, index=False, sheet_name='Filtered Data')
                writer.save()
                processed_data = output.getvalue()
                return processed_data

            df_xlsx = to_excel(filtered_data)
            st.download_button(label='📥 Download Current Data as Excel',
                               data=df_xlsx,
                               file_name='filtered_data.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
