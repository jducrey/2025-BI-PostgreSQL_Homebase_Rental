import pandas as pd
import numpy as np
from datetime import timedelta

# Charger les fichiers
bookings = pd.read_csv("bookings.csv", parse_dates=["end_date"])
reviews = pd.read_csv("review.csv")

# Fusionner sur 'booking_id' pour récupérer la date de fin
merged = reviews.merge(bookings[["booking_id", "end_date"]], on="booking_id", how="left")

# Générer une date de review aléatoire entre 1 et 30 jours après end_date
merged["review_date"] = merged["end_date"] + pd.to_timedelta(np.random.randint(1, 31, size=len(merged)), unit="D")

# Enregistrer le nouveau review.csv avec les dates générées
merged.drop(columns=["end_date"]).to_csv("review.csv", index=False)

print("review.csv mis à jour avec les nouvelles dates de review.")