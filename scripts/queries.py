import psycopg2
from psql_var import userName, mdp

def connect():
    return psycopg2.connect(
        dbname="cozybnb_db",
        user=userName,
        password=mdp,
        host="localhost",
        port="5432"
    )

def execute_query(query, description):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()

        print(f"\n{description}")
        print("-" * len(description))
        for row in results:
            print(row)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")

if __name__ == "__main__":
    queries = [
        (
            """
            SELECT p.title, COUNT(b.booking_id) AS total_bookings
            FROM properties p
            JOIN bookings b ON p.property_id = b.property_id
            GROUP BY p.title
            ORDER BY total_bookings DESC
            LIMIT 5;
            """,
            "Top 5 des propriétés les plus réservées"
        ),
        (
            """
            SELECT p.title, SUM(b.total_price) AS total_revenue
            FROM properties p
            JOIN bookings b ON p.property_id = b.property_id
            GROUP BY p.title
            ORDER BY total_revenue DESC;
            """,
            "Revenu total généré par chaque propriété"
        ),
        (
            """
            SELECT p.title, AVG(r.rating) AS avg_rating
            FROM properties p
            JOIN bookings b ON p.property_id = b.property_id
            JOIN reviews r ON b.booking_id = r.booking_id
            GROUP BY p.title
            ORDER BY avg_rating DESC;
            """,
            "Note moyenne par propriété"
        ),
        (
            """
            SELECT DATE_TRUNC('month', start_date) AS month, COUNT(*) AS bookings_count
            FROM bookings
            WHERE start_date >= CURRENT_DATE - INTERVAL '1 year'
            GROUP BY month
            ORDER BY month;
            """,
            "Nombre de réservations par mois sur l'année écoulée"
        )
    ]

    for query, description in queries:
        execute_query(query, description)
