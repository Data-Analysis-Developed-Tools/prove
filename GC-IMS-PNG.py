import cv2
import numpy as np
import pandas as pd
from PIL import Image
import io
import matplotlib.pyplot as plt

# Convertire in scala di grigi per analizzare l'intensità
image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Converti da RGB a Grayscale

# Normalizzare l'immagine per evidenziare le variazioni cromatiche
normalized_img = cv2.normalize(image_gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

# Applicare la colormap "jet" per evidenziare le intensità
colormap_img = cv2.applyColorMap(normalized_img, cv2.COLORMAP_JET)

# Applicare un threshold per segmentare le aree ad alta intensità
_, thresh = cv2.threshold(normalized_img, 150, 255, cv2.THRESH_BINARY)

# Trovare i contorni dei blob
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Lista per raccogliere i dati dei blob
data_new = []

# Processare ogni blob trovato
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_blob = colormap_img[y:y+h, x:x+w]

    # Trova il punto con massima intensità nel blob
    _, max_val, _, max_loc = cv2.minMaxLoc(normalized_img[y:y+h, x:x+w])

    # Convertire il blob in formato PNG in memoria
    cropped_pil = Image.fromarray(cropped_blob)
    buf = io.BytesIO()
    cropped_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    data_new.append([byte_im, x, x+w, y, y+h, x + max_loc[0], y + max_loc[1]])

# Creare un DataFrame pandas con i dati dei blob
df_final = pd.DataFrame(data_new, columns=["Immagine", "X Inizio", "X Fine", "Y Inizio", "Y Fine", "X Max Intensità", "Y Max Intensità"])

# Visualizzare i blob estratti con matplotlib
fig, axes = plt.subplots(1, len(data_new), figsize=(15, 5))

# Se c'è un solo blob, `axes` non è una lista, quindi lo forziamo in una lista
if len(data_new) == 1:
    axes = [axes]

for ax, (blob_img, _, _, _, _, _, _) in zip(axes, data_new):
    img = Image.open(io.BytesIO(blob_img))  # Convertire il blob in immagine
    ax.imshow(img)
    ax.axis("off")

plt.show()  # Mostrare i blob estratti

# Rimuovere le immagini dalla tabella per visualizzarla correttamente
df_final.drop(columns=["Immagine"], inplace=True)

# Visualizzare la tabella con i dettagli dei blob
import ace_tools as tools
tools.display_dataframe_to_user(name="Feature Estratte dai Blob", dataframe=df_final)
