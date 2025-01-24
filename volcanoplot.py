import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    return df

def preprocess_data(df):
    # Estraiamo le categorie e i nomi delle variabili
    categories = df.iloc[0, 2:].tolist()  # Assumendo che le categorie siano dalle terza colonna in poi
    variable_names = df.iloc[1, 2:].tolist()  # Nomi delle variabili dalla terza colonna in poi
    
    # Aggiorniamo il dataframe escludendo le prime due righe e impostiamo i nuovi nomi delle colonne
    df = df.iloc[2:]  # Rimuove le righe con categorie e nomi variabili
    
    # Assegna nuovi nomi di colonna assicurandosi di includere tutte le colonne
    new_column_names = ['Desc1', 'Desc2'] + variable_names  # Assumendo che le prime due colonne siano descrittive
    if len(new_column_names) != len(df.columns):
        raise ValueError(f"Expected {len(df.columns)} column names, but got {len(new_column_names)}")
    
    df.columns = new_column_names
    
    return df, categories, variable_names


def create_volcano_plot(df, variable_names, categories):
    # Supponiamo di avere due condizioni per il confronto: condizione A e condizione B
    # Qui potresti dover adattare il codice per adattarsi alle tue specifiche categorie
    
    # Calcoliamo log2(Fold Change) e -log10(p-value)
    df['log2FC'] = df[variable_names[0]] / df[variable_names[1]]  # Questo è un esempio, potrebbe necessitare di adattamento
    df['-log10p'] = -np.log10(df[variable_names[2]])  # Supponiamo che p-values siano nella terza colonna variabile

    fig = px.scatter(df, x='log2FC', y='-log10p',
                     hover_data=['Desc1', 'Desc2'],
                     title="Volcano Plot",
                     labels={"log2FC": "Log2 Fold Change", "-log10p": "-Log10 p-value"})
    return fig

# Widget per il caricamento del file
uploaded_file = st.file_uploader("Carica un file Excel o CSV", type=['csv', 'xlsx'])
if uploaded_file is not None:
    df = load_data(uploaded_file)
    df, categories, variable_names = preprocess_data(df)

    # Creiamo il volcano plot
    fig = create_volcano_plot(df, variable_names, categories)
    st.plotly_chart(fig)
