import pandas as pd

# Chargement des utilisateurs
df = pd.read_csv("datas/users.csv", parse_dates=["signup_date", "birth_date"])

# Fonction pour déterminer le sexe à partir du prénom
def infer_sex(name):
    first_name = name.split()[0].lower()
    # Liste indicative de prénoms masculins et féminins en France
    male_names = {"arnaud", "bob", "luc", "noah", "léo", "julien", "antoine", "matthieu", "victor", "nicolas",
                  "romain", "théo", "quentin", "hugo", "louis", "adrien", "maxime", "yanis"}
    # On suppose "F" par défaut si non trouvé
    return "M" if first_name in male_names else "F"

# Application de la fonction
df["sex"] = df["name"].apply(infer_sex)

# Vérification
print(df[["name", "sex"]].head())

# Sauvegarde du fichier final
df.to_csv("datas/users.csv", index=False)
