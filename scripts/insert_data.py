import psycopg2
import csv
from psql_var import userName, mdp

def insert_from_csv(cursor, table_name, file_path, columns):
    with open(file_path, mode='r', encoding='utf-8') as f:
        next(f)  # skip header
        reader = csv.reader(f)
        for row in reader:
            placeholders = ', '.join(['%s'] * len(row))
            sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(sql, row)

try:
    conn = psycopg2.connect(
        dbname="cozybnb_db",
        user=userName,
        password=mdp,
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    print("Connexion réussie.")

    insert_from_csv(cur, 'users', 'datas/users.csv', ['user_id', 'name', 'email', 'signup_date', 'birth_date', 'phone', 'address', 'sex'])
    insert_from_csv(cur, 'properties', 'datas/properties.csv', ['property_id', 'owner_id', 'title', 'location', 'price_per_night', 'max_occupants', 'surface_m2', 'parking_spaces', 'wifi_access', 'num_bedrooms', 'num_bathrooms'])
    insert_from_csv(cur, 'bookings', 'datas/bookings.csv', ['booking_id', 'user_id', 'property_id', 'start_date', 'end_date', 'total_price', 'booking_date'])
    insert_from_csv(cur, 'reviews', 'datas/reviews.csv', ['review_id', 'booking_id', 'rating', 'comment', 'review_date'])

    conn.commit()
    cur.close()
    conn.close()
    print("Données insérées et connexion fermée.")

except Exception as e:
    print(f"Erreur : {e}")
