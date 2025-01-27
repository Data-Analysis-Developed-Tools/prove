import streamlit as st
import pandas as pd
import plotly.express as px
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

        if submit_button:
            num_rows = len(data)
            simulated_log2FoldChange = np.random.normal(0, 1, num_rows)
            simulated_pvalues = np.random.uniform(0, 0.05, num_rows)

            # Creazione del volcano plot con Plotly
            data['Log2FoldChange'] = simulated_log2FoldChange
            data['-Log10(p-value)'] = -np.log10(simulated_pvalues)
            fig = px.scatter(data, x='Log2FoldChange', y='-Log10(p-value)', 
                             hover_data=[data.columns[0], 'p-value', 'Log2FoldChange'],
                             size_max=10)
            fig.update_traces(marker=dict(size=6))  # Ridurre la dimensione dei marker
            fig.add_vline(x=0, line_width=2, line_dash="dash", line_color="red")  # Linea verticale
            fig.update_layout(showlegend=False, hovermode='closest')
            st.plotly_chart(fig, use_container_width=True)

            # Creazione del link di download per il nuovo file Excel
            output_df = data[['Etichette', 'Log2FoldChange', '-Log10(p-value)', 'p-value']]
            file_name = os.path.splitext(uploaded_file.name)[0] + "_values_from_volcano_plot.xlsx"
            link = create_download_link(output_df, file_name)
            st.markdown(link, unsafe_allow_html=True)

    else:
        st.info("Carica un file per procedere.")

if __name__ == "__main__":
    main()
