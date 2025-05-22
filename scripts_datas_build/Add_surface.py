import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv("datas/properties.csv")

# Fixer la graine pour la reproductibilité
np.random.seed(42)

# Paramètres pour la simulation
base_m2_per_person = np.random.uniform(12, 18, size=len(df))  # entre 12 et 18 m² par personne
price_factor = df['price_per_night'] / 10  # prix influe, mais pas de manière linéaire
random_noise = np.random.normal(loc=0, scale=5, size=len(df))  # bruit gaussien ±5 m²

# Calcul de la superficie
df['surface_m2'] = (
    df['max_occupants'] * base_m2_per_person +
    price_factor +
    random_noise
).round().astype(int)

# S'assurer que la surface est au moins 10 m² (ex : petit studio)
df['surface_m2'] = df['surface_m2'].clip(lower=10)

# Sauvegarder dans le même fichier ou un nouveau
df.to_csv("datas/properties.csv", index=False)
