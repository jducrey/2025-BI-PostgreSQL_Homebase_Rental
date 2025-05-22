import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv("datas/properties.csv")

# Fixer la graine pour la reproductibilité
np.random.seed(42)

# Définir les valeurs possibles et leurs probabilités
values = [0, 1, 2, 3]
probabilities = [0.38, 0.48, 0.1, 0.04]

# Générer aléatoirement les places de parking
df['parking_spaces'] = np.random.choice(values, size=len(df), p=probabilities)

# Sauvegarder dans le même fichier ou un nouveau
df.to_csv("datas/properties.csv", index=False)
