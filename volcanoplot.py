import pandas as pd
import streamlit as st

def carica_dati(file):
    try:
        dati = pd.read_excel(file, header=[0, 1], index_col=0)
        classi = dati.columns.get_level_values(1).unique()
        return dati, classi
    except ValueError as e:
        st.error(f"Errore nel caricamento del file: {str(e)}")
        return None, None
    except Exception as e:
        st.error(f"Errore non gestito: {str(e)}")
        return None, None

def main():
    st.title("Volcano Plot Interattivo")
    file = st.file_uploader("Carica il file Excel", type=['xlsx'])

    if file is not None:
        dati, classi = carica_dati(file)
        if dati is not None:
            # Il resto del codice per elaborare i dati
            st.write("Dati caricati correttamente!")
        else:
            st.error("Impossibile procedere senza dati validi.")
    else:
        st.warning("Si prega di caricare un file Excel.")

if __name__ == "__main__":
    main()
