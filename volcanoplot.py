import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def load_data(uploaded_file):
    # Carica il file, salta le prime due righe per le intestazioni
    df = pd.read_excel(uploaded_file, header=[0, 1])
    df.columns = [f"{i}_{j}" if j else f"{i}" for i, j in df.columns]
    return df

def preprocess_data(df):
    # Estrae le descrizioni variabili e nomi delle classi
    # Le descrizioni delle variabili si trovano nelle prime due colonne
    variable_descriptions = df[['m/z_', 'RT [min]_']].copy()
    df.drop(['m/z_', 'RT [min]_'], axis=1, inplace=True)

    # Trasforma il dataframe per avere classi come colonne e osservazioni come righe
    df = df.melt(id_vars=['m/z_', 'RT [min]_'], var_name='Class', value_name='Intensity')
    
    return df, variable_descriptions

def create_volcano_plot(df):
    # Calcola log2 Fold Change e -log10 p-value (esempi)
    df['log2FC'] = np.log2(df['Intensity'] / df['Intensity'].mean())  # Cambia con calcoli reali
    df['-log10p'] = -np.log10(0.05)  # Cambia con calcoli reali

    fig = px.scatter(df, x='log2FC', y='-log10p', color='Class',
                     hover_data=['m/z_', 'RT [min]_'])
    return fig

# Interfaccia utente Streamlit
st.title('Visualizzazione Volcano Plot')
uploaded_file = st.file_uploader("Carica un file CSV o Excel", type=['csv', 'xlsx'])
if uploaded_file is not None:
    df = load_data(uploaded_file)
    df, variable_descriptions = preprocess_data(df)
    fig = create_volcano_plot(df)
    st.plotly_chart(fig)
