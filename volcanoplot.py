def prepara_dati(dati, fold_change_threshold, p_value_threshold):
    if dati is not None:
        classi = dati['Class'].unique()  # Accedi correttamente alla colonna 'Class'
        risultati = []
        for var in dati.columns[2:]:  # Ignora le colonne 'name' e 'Class'
            valori = [dati.loc[dati['Class'] == classe, var].dropna().values for classe in classi]
            if len(valori[0]) > 0 and len(valori[1]) > 0:
                media_diff = np.log2(np.mean(valori[1]) / np.mean(valori[0])) if np.mean(valori[0]) > 0 else None
                t_stat, p_val = ttest_ind(valori[0], valori[1], equal_var=False)
                p_val_log = -np.log10(p_val) if p_val > 0 else None
                if abs(media_diff) >= fold_change_threshold and p_val_log >= p_value_threshold:
                    risultati.append([dati.iloc[var]['name'], media_diff, p_val_log])
        risultati_df = pd.DataFrame(risultati, columns=['Variabile', 'Log2 Fold Change', '-log10(p-value)'])
        return risultati_df
    else:
        st.error("Il dataframe non è stato caricato correttamente.")
        return None
