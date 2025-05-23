import pandas as pd
import random
from datetime import datetime, timedelta

# Chargement des données utilisateurs et logements
users = pd.read_csv('datas/users.csv')
properties = pd.read_csv('datas/properties.csv')  # doit contenir 'property_id' et 'price_per_night'

# Ajout dans les fichiers existants
bookings_csv = pd.read_csv('datas/bookings.csv')
reviews_csv = pd.read_csv('datas/reviews.csv')

# Combien de bookings/reviews tu veux générer ?
NUM_BOOKINGS = 10000
NUM_REVIEWS = 8000

# Déterminer le max des IDs actuels
max_booking_id = bookings_csv['booking_id'].max() if not bookings_csv.empty else 0
max_review_id = reviews_csv['review_id'].max() if not reviews_csv.empty else 0

# Fonctions utilitaires
def random_date(start, end):
    """Retourne une date aléatoire entre deux dates"""
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_booking_dates():
    """Génère une paire (start_date, end_date) entre 2023 et 2025"""
    start_date = random_date(datetime(2023, 1, 1), datetime(2025, 12, 1))
    nights = random.randint(1, 14)
    end_date = start_date + timedelta(days=nights)
    return start_date, end_date, nights

def generate_booking_date_before(start_date):
    """Génère une date de réservation avant le start_date"""
    delta_days = random.randint(1, 90)
    return start_date - timedelta(days=delta_days)

def generate_review_date(end_date):
    """Génère une date de review entre 1 jour et 1 mois après le end_date"""
    delta_days = random.randint(1, 30)
    return end_date + timedelta(days=delta_days)

def generate_review_text(rating):
    if rating >= 4:
        return random.choice([
            "Séjour incroyable, merci !", 
            "Tout était parfait ", 
            "Très bonne expérience", 
            "Rien à redire",
            "Super expérience !",
            "Très bon séjour",
            "Propriétaire sympa et logement clean",
            "Je recommande !",
            "Super séjour, hôte très sympa !",
            "Excellente expérience, je recommande.",
            "Le logement était parfait",
            "Top top top ! Rien à redire."
        ])
    elif rating == 3:
        return random.choice([
            "C'était moyen", 
            "Un peu décevant", 
            "Pas mal mais peut mieux faire",
            "Correct sans plus",
            "Peut mieux faire",
            "C'était ok",
            "Juste correct mais sans plus.",
            "Quelques soucis, mais globalement ok.",
            "Moyennement satisfait."
        ])
    else:
        return random.choice([
            "Expérience bof", 
            "Beaucoup de problèmes", 
            "Très déçu",
            "Expérience décevante",
            "Propreté douteuse",
            "Je ne recommande pas",
            "Propriétaire peu accueillant !",
            "Très déçu, pas conforme à l'annonce.",
            "Problèmes d'hygiène, je ne recommande pas.",
            "Expérience frustrante, à éviter."
        ])

# Génération des bookings
bookings = []
for i in range(NUM_BOOKINGS):
    booking_id = max_booking_id + i + 1
    user_id = random.choice(users['user_id'].values)
    property_row = properties.sample().iloc[0]
    property_id = property_row['property_id']
    price_per_night = property_row['price_per_night']
    
    start_date, end_date, nights = generate_booking_dates()
    total_price = round(price_per_night * nights, 2)
    booking_date = generate_booking_date_before(start_date)
    
    bookings.append([booking_id, user_id, property_id, start_date.date(), end_date.date(), total_price, booking_date.date()])

bookings_df = pd.DataFrame(bookings, columns=[
    'booking_id', 'user_id', 'property_id', 'start_date', 'end_date', 'total_price', 'booking_date'
])

# Tirer aléatoirement des bookings uniques pour lesquels on va générer une review
bookings_with_reviews = random.sample(bookings, NUM_REVIEWS)

# Génération des reviews
reviews = []
for i,booking in enumerate(bookings_with_reviews):
    review_id = max_review_id + i + 1
    booking_id = booking[0]
    rating = random.randint(1, 5)
    comment = generate_review_text(rating)
    review_date = generate_review_date(datetime.strptime(str(booking[4]), "%Y-%m-%d")).date()
    
    reviews.append([review_id, booking_id, rating, comment, review_date])

reviews_df = pd.DataFrame(reviews, columns=[
    'review_id', 'booking_id', 'rating', 'comment', 'review_date'
])

bookings_combined = pd.concat([bookings_csv, bookings_df], ignore_index=True)
reviews_combined = pd.concat([reviews_csv, reviews_df], ignore_index=True)

# Sauvegarde
bookings_combined.to_csv('datas/bookings.csv', index=False)
reviews_combined.to_csv('datas/reviews.csv', index=False)

print("Données enrichies et ajoutées dans bookings.csv et reviews.csv")