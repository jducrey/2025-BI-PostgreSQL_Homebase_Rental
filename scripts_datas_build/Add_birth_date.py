import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Charger le fichier
df = pd.read_csv("datas/users.csv")

# Fixer la graine pour reproductibilité
np.random.seed(42)

# Générer les dates de naissance aléatoires entre 18 et 70 ans
def generate_birth_date():
    today = pd.Timestamp.today()
    min_age = 18
    max_age = 70
    # Générer un âge aléatoire
    age = np.random.randint(min_age, max_age + 1)
    # Ajouter un décalage aléatoire sur l'année pour la diversité
    days_offset = np.random.randint(0, 365)
    birth_date = today - pd.DateOffset(years=age) - pd.Timedelta(days=days_offset)
    return birth_date.date()

# Appliquer à chaque utilisateur
df["birth_date"] = [generate_birth_date() for _ in range(len(df))]

# Sauvegarder le fichier mis à jour
df.to_csv("datas/users.csv", index=False)
