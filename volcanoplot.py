import io
import pandas as pd
import base64
import streamlit as st

def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        if object_to_download.empty:
            return "Nessun dato da scaricare"
        else:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                object_to_download.to_excel(writer, index=False)
            data = output.getvalue()
    else:
        data = object_to_download

    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/xls;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def main():
    # Il resto del codice Streamlit

    # Dopo aver creato il DataFrame `dati_preparati`
    if not dati_preparati.empty:
        tmp_download_link = download_link(dati_preparati, "dati_significativi.xlsx", "Scarica i dati come Excel")
        st.markdown(tmp_download_link, unsafe_allow_html=True)
    else:
        st.write("Nessun dato significativo da scaricare.")

if __name__ == "__main__":
    main()
