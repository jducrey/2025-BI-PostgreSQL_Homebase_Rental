import pandas as pd
from faker import Faker

# Chargement de la table des utilisateurs
df = pd.read_csv("datas/users.csv", parse_dates=["signup_date", "birth_date"])

# Initialisation de Faker en français
fake = Faker("fr_FR")

# Génération des numéros de téléphone et adresses
df["phone"] = [fake.phone_number().replace(" ", "").replace("0", "+33", 1) for _ in range(len(df))]
df["address"] = [fake.address().replace("\n", ", ") for _ in range(len(df))]

# Affichage du résultat
print(df.head())

# Sauvegarde du fichier enrichi
df.to_csv("datas/users.csv", index=False)
