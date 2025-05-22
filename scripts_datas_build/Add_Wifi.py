import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv("datas/properties.csv")

# Fixer la graine pour la reproductibilité
np.random.seed(42)

# Définir les valeurs possibles et leurs probabilités
values = [False, True]
probabilities = [0.2, 0.8]

# Générer aléatoirement les places de parking
df['wifi_access'] = np.random.choice(values, size=len(df), p=probabilities)

# Sauvegarder dans le même fichier ou un nouveau
df.to_csv("datas/properties.csv", index=False)