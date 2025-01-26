import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
import numpy as np
from io import BytesIO

# Funzione per caricare i dati
def carica_dati(file):
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
    except ValueError:
        st.error("Il file caricato non ha due livelli di intestazione come richiesto.")
        return None
    return dati

# Preparazione dei dati per il volcano plot
def prepara_dati(dati, fold_change_threshold, p_value_threshold):
    if dati is not None and isinstance(dati.columns, pd.MultiIndex):
        classi = dati.columns.get_level_values(1).unique()
        risultati = []
        for var in dati.index:
            valori = [dati.loc[var, dati.columns.get_level_values(1) == classe].dropna().values for classe in classi]
            if len(valori[0]) > 0 and len(valori[1]) > 0:
                media_diff = np.log2(np.mean(valori[0]) / np.mean(valori[1]))
                t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                if abs(media_diff) >= fold_change_threshold and p_val <= p_value_threshold:
                    risultati.append([var, media_diff, p_val_log, p_val])
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2 Fold Change', '-log10(p-value)', 'p-value'])
        return risultati_df
    else:
        st.error("Il dataframe non contiene un indice multi-livello come atteso.")
        return None

# Funzione per creare il volcano plot
def crea_volcano_plot(dati, show_labels):
    if dati is not None:
        fig = px.scatter(dati, x='Log2 Fold Change', y='-log10(p-value)', text='Variabile' if show_labels else None, hover_data=['Variabile'])
        fig.update_traces(textposition='top center')
        fig.update_layout(title='Volcano Plot', xaxis_title='Log2 Fold Change', yaxis_title='-log10(p-value)')
        return fig
    else:
        return None

# Funzione per scaricare i dati come Excel
def get_table_download_link(df):
    """Generates a download link allowing the data in a given panda dataframe to be downloaded as an excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
        writer.save()
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="filtered_data.xlsx">Download Excel file</a>'
    return href

# Streamlit App
def main():
    st.title("Volcano Plot Interattivo")

    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    with st.form(key='my_form'):
        fold_change_threshold = st.number_input('Inserisci il valore soglia per il -log2Fold Change', value=2.0)
        p_value_threshold = st.number_input('Inserisci il valore soglia per il p-value', value=0.05, format='%f')
        submit_button = st.form_submit_button(label='Applica Filtri')

    show_labels = st.checkbox("Mostra etichette delle variabili", value=True)

    if file is not None and submit_button:
        dati = carica_dati(file)
        if dati is not None:
            dati_preparati = prepara_dati(dati, fold_change_threshold, p_value_threshold)
            if dati_preparati is not None:
                fig = crea_volcano_plot(dati_preparati, show_labels)
                if fig is not None:
                    st.plotly_chart(fig)
                    st.markdown(get_table_download_link(dati_preparati), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
