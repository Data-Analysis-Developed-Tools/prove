import pandas as pd
import streamlit as st
import plotly.express as px

def load_data(uploaded_file):
    # Supponendo che il file sia in formato .xlsx; se non sei sicuro, puoi aggiungere controlli basati sull'estensione del file.
    df = pd.read_excel(uploaded_file, engine='openpyxl', header=None)
    return df


def preprocess_data(df):
    # Assumiamo che le prime due righe contengano le intestazioni necessarie
    # Prima riga: nomi delle classi per le osservazioni, combinate con la seconda riga
    headers = df.iloc[0:2].apply(lambda x: x.map(str)).agg('_'.join)
    df.columns = headers
    df = df.drop(index=[0, 1])

    # Gestisci le colonne descrittive
    variable_descriptions = df[['m/z_RT [min]', 'RT [min]_RT [min]']].copy()
    df.drop(['m/z_RT [min]', 'RT [min]_RT [min]'], axis=1, inplace=True)

    # Converti tutti i dati rimanenti in float
    df = df.apply(pd.to_numeric, errors='coerce')

    return df, variable_descriptions

def create_volcano_plot(df, variable_descriptions):
    # Implementa la logica per il volcano plot, esempio:
    fig = px.scatter(df, x='logFC', y='-log10(p-value)', hover_data=variable_descriptions.columns.tolist())
    return fig

# Streamlit UI
st.title('Visualizzazione Volcano Plot')
uploaded_file = st.file_uploader("Carica un file CSV o Excel", type=['csv', 'xlsx'])
if uploaded_file:
    df = load_data(uploaded_file)
    df, variable_descriptions = preprocess_data(df)
    fig = create_volcano_plot(df, variable_descriptions)
    st.plotly_chart(fig)
