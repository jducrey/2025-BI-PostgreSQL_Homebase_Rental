# scripts/init_tables.py
from config.db_utils import connect_cozy_bnb_db

def init_tables():
    try:
        conn = connect_cozy_bnb_db()
        cur = conn.cursor()
        print("Connexion réussie.")

        cur.execute("""
            -- Table des utilisateurs
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                signup_date DATE,
                birth_date DATE,
                phone TEXT,
                address TEXT,
                sex TEXT CHECK (sex IN ('M', 'F'))
            );

            -- Table des propriétés
            CREATE TABLE IF NOT EXISTS properties (
                property_id INTEGER PRIMARY KEY,
                owner_id INTEGER REFERENCES users(user_id),
                property_type TEXT,
                title TEXT,
                location TEXT,
                price_per_night NUMERIC,
                max_occupants INTEGER,
                surface_m2 NUMERIC,
                parking_spaces INTEGER CHECK (parking_spaces BETWEEN 0 AND 3),
                wifi_access BOOLEAN,
                num_bedrooms INTEGER,
                num_bathrooms INTEGER
            );

            -- Table des réservations
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                property_id INTEGER REFERENCES properties(property_id),
                start_date DATE,
                end_date DATE,
                total_price NUMERIC,
                booking_date DATE
            );

            -- Table des avis
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INTEGER PRIMARY KEY,
                booking_id INTEGER REFERENCES bookings(booking_id),
                rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                comment TEXT,
                review_date DATE
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Tables créées et connexion fermée.")

    except Exception as e:
        print(f"Erreur : {e}")
        
    return None