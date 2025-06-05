# scripts/insert_data.py
import csv
from config.db_utils import connect_cozy_bnb_db

def insert_from_csv(cursor, table_name, file_path, columns):
    with open(file_path, mode='r', encoding='utf-8') as f:
        next(f)  # skip header
        reader = csv.reader(f)
        for row in reader:
            row = [None if val == '\\N' else val for val in row]
            placeholders = ', '.join(['%s'] * len(row))
            sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(sql, row)

def insert_data():
    try:
        conn = connect_cozy_bnb_db()
        cur = conn.cursor()
        print("Connexion réussie.")

        insert_from_csv(cur, 'users', 'datas/users.csv', ['user_id', 'name', 'email', 'signup_date', 'birth_date', 'phone', 'address', 'sex'])
        insert_from_csv(cur, 'properties', 'datas/properties.csv', ['property_id', 'owner_id', 'property_type', 'title', 'location', 'price_per_night', 'max_occupants', 'surface_m2', 'parking_spaces', 'wifi_access', 'num_bedrooms', 'num_bathrooms'])
        insert_from_csv(cur, 'bookings', 'datas/bookings.csv', ['booking_id', 'user_id', 'property_id', 'start_date', 'end_date', 'total_price', 'booking_date', 'canceled', 'cancellation_date'])
        insert_from_csv(cur, 'reviews', 'datas/reviews.csv', ['review_id', 'booking_id', 'rating', 'comment', 'review_date'])

        conn.commit()
        cur.close()
        conn.close()
        print("Données insérées et connexion fermée.")

    except Exception as e:
        print(f"Erreur : {e}")

    return None