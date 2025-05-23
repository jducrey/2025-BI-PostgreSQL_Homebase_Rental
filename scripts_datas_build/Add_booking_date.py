import pandas as pd
from datetime import datetime, timedelta
import random

# Charger les données
df = pd.read_csv("bookings.csv")

# Fonction pour générer une date aléatoire entre 1 jour et 3 mois avant la start_date
def generate_random_booking_date(start_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    min_days = 1
    max_days = 90  # environ 3 mois
    delta_days = random.randint(min_days, max_days)
    booking_date = start_date - timedelta(days=delta_days)
    return booking_date.strftime("%Y-%m-%d")

# Appliquer la fonction à chaque ligne
df["booking_date"] = df["start_date"].apply(generate_random_booking_date)

# Sauvegarder le fichier modifié
df.to_csv("bookings.csv", index=False)

print("booking_date créée et sauvegardée dans bookings.csv")
