import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtered Data')
    output.seek(0)
    return output.getvalue()

def main():
    st.title("Volcano Plot Application")

    # File upload section
    uploaded_file = st.file_uploader("Upload your input Excel file", type=["xlsx"])
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)

        # Generate data for the plot if the uploaded file is processed
        data['Log2FoldChange'] = np.log2(data['Values'] / data['Control'])
        data['p-value'] = np.random.rand(len(data))
        data['-Log10(p-value)'] = -np.log10(data['p-value'])

        # User input for thresholds
        threshold_fold_change = st.sidebar.slider("Log2 Fold Change Threshold", min_value=float(data['Log2FoldChange'].min()), max_value=float(data['Log2FoldChange'].max()), value=1.0)
        threshold_pvalue = st.sidebar.slider("-Log10(p-value) Threshold", min_value=float(data['-Log10(p-value)'].min()), max_value=float(data['-Log10(p-value)'].max()), value=1.5)

        # Filter data based on thresholds
        filtered_data = data[(data['Log2FoldChange'].abs() > threshold_fold_change) & (data['-Log10(p-value)'] > threshold_pvalue)]

        # Plotting
        fig = px.scatter(filtered_data, x='Log2FoldChange', y='-Log10(p-value)', hover_data=['Log2FoldChange', 'p-value'])
        fig.add_hline(y=threshold_pvalue, line_dash="dot", annotation_text="p-value threshold")
        fig.add_vline(x=0, line_dash="dot", annotation_text="Fold Change = 0")
        st.plotly_chart(fig, use_container_width=True)

        # Download button for the filtered data
        df_xlsx = to_excel(filtered_data)
        st.download_button(label="Download Excel file", data=df_xlsx, file_name="filtered_data.xlsx", mime="application/vnd.ms-excel")

if __name__ == "__main__":
    main()
