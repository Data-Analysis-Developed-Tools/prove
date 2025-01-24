import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def load_data(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    return df

def preprocess_data(df):
    # Estrapola nomi delle classi e nomi descrittivi delle osservazioni
    class_names = df.iloc[0, 2:].tolist()  # Nomi delle classi dalle terze colonne in poi
    descriptive_names = df.iloc[1, 2:].tolist()  # Nomi descrittivi
    
    # Rimuove le prime due righe che contengono i metadati
    df = df.iloc[2:]
    
    # Imposta i nomi delle colonne, assicurandosi che il numero dei nomi corrisponda al numero di colonne
    if len(df.columns) != 2 + len(descriptive_names):
        raise ValueError(f"Expected {len(df.columns)} column names, but got {2 + len(descriptive_names)}")
    
    df.columns = ['Variable Description 1', 'Variable Description 2'] + descriptive_names
    return df, class_names


def create_volcano_plot(df, class_names):
    # Simulazione di dati per volcano plot
    df['log2FC'] = np.log2(df['Variable Description 2'] / df['Variable Description 1'])  # Sostituire con calcolo reale
    df['-log10p'] = -np.log10(0.05)  # Sostituire con dati reali di p-value
    
    # Crea il grafico interattivo
    fig = px.scatter(df, x='log2FC', y='-log10p',
                     hover_data=['Variable Description 1', 'Variable Description 2'],
                     title="Volcano Plot")
    return fig

# Streamlit UI
st.title('Volcano Plot Visualizer')
uploaded_file = st.file_uploader("Carica un file CSV o Excel", type=['csv', 'xlsx'])
if uploaded_file is not None:
    df = load_data(uploaded_file)
    df, class_names = preprocess_data(df)
    fig = create_volcano_plot(df, class_names)
    st.plotly_chart(fig)
