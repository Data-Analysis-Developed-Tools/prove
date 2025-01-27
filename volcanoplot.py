import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Simuliamo dei dati per il volcano plot
data = pd.DataFrame({
    'log2FoldChange': np.random.normal(0, 1, 100),
    'pvalue': np.random.uniform(0, 0.05, 100)
})
data['-log10(pvalue)'] = -np.log10(data['pvalue'])

# Aggiungiamo una colonna per le etichette
data['label'] = ['gene' + str(i) for i in range(100)]

# Opzione per mostrare/nascondere le etichette
show_labels = st.checkbox("Mostra etichette")

# Creazione del volcano plot
fig, ax = plt.subplots()
sns.scatterplot(x='log2FoldChange', y='-log10(pvalue)', data=data, ax=ax)

if show_labels:
    for i in range(data.shape[0]):
        ax.text(data.iloc[i]['log2FoldChange'], data.iloc[i]['-log10(pvalue)'], data.iloc[i]['label'], fontsize=9)

st.pyplot(fig)
