import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv("datas/properties.csv")

# Fixer la graine pour reproductibilité
np.random.seed(42)

# Générer un nombre de chambres entre 1 et max_occupants pour chaque ligne
df["num_bedrooms"] = df["max_occupants"].apply(lambda x: np.random.randint(1, x + 1))

# Sauvegarder dans le fichier
df.to_csv("datas/properties.csv", index=False)
