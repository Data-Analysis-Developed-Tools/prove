import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = to_excel(object_to_download)  # Convert DataFrame to Excel
    b64 = base64.b64encode(object_to_download).decode()
    return f'<a href="data:file/xlsx;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def main():
    st.title('Volcano Plot App')
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        
        # Check if data has necessary columns to generate 'p-value' and 'Log2FoldChange'
        if 'Sample' in data.columns and 'Control' in data.columns:
            # Simulate 'Log2FoldChange' and 'p-value' for demonstration purposes
            data['Log2FoldChange'] = np.log2(data['Sample'] / data['Control'])
            data['p-value'] = np.random.uniform(0, 1, data.shape[0])
            data['-Log10(p-value)'] = -np.log10(data['p-value'])
        
        st.write("Here's the first few rows of your data:", data.head())

        # Filtering data based on user input for demonstration
        threshold_pvalue = st.slider('P-value Cutoff', 0.0, 1.0, 0.05)
        threshold_fold_change = st.slider('Log2 Fold Change Cutoff', 0.0, 10.0, 1.0)
        filtered_data = data[(data['p-value'] <= threshold_pvalue) & (abs(data['Log2FoldChange']) >= threshold_fold_change)]

        # Plotting the volcano plot
        fig, ax = plt.subplots()
        ax.scatter(filtered_data['Log2FoldChange'], filtered_data['-Log10(p-value)'])
        ax.axhline(y=-np.log10(threshold_pvalue), color='r', linestyle='--')
        ax.axvline(x=threshold_fold_change, color='b', linestyle='--')
        ax.set_xlabel('Log2 Fold Change')
        ax.set_ylabel('-Log10 P-value')
        st.pyplot(fig)

        # Download link for filtered data
        df_xlsx = to_excel(filtered_data)  # Convert DataFrame to Excel
        st.markdown(download_link(df_xlsx, 'filtered_data.xlsx', 'Download filtered data as Excel'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
