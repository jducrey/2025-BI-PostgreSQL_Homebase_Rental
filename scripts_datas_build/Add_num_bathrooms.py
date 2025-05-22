import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv("datas/properties.csv")

# Graine pour reproductibilité
np.random.seed(42)

# Fonction pour générer un nombre de salles de bains réaliste
def generate_bathrooms(occupants):
    if occupants <= 3:
        return 1
    elif occupants <= 6:
        return np.random.choice([1, 2], p=[0.3, 0.7])
    else:
        return np.random.choice([2, 3], p=[0.4, 0.6])

# Appliquer la fonction
df["num_bathrooms"] = df["max_occupants"].apply(generate_bathrooms)

# Sauvegarde du fichier modifié
df.to_csv("datas/properties.csv", index=False)
