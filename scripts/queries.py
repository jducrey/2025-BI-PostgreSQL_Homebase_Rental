import psycopg2
from config.db_utils import connect_cozy_bnb_db

def queries_for_first_KPIs():

    def execute_query(query, description):
        try:
            conn = connect_cozy_bnb_db()
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
            "Top 5 des logements les plus réservés"
        ),
        (
            """
            SELECT p.title, SUM(b.total_price) AS total_revenue
            FROM properties p
            JOIN bookings b ON p.property_id = b.property_id
            WHERE b.canceled = FALSE
            GROUP BY p.title
            ORDER BY total_revenue DESC
            LIMIT 5;
            """,
            "Top 5 des logements ayant généré les plus gros revenus"
        ),
        (
            """
            SELECT p.title, AVG(r.rating) AS avg_rating
            FROM properties p
            JOIN bookings b ON p.property_id = b.property_id
            JOIN reviews r ON b.booking_id = r.booking_id
            GROUP BY p.title
            ORDER BY avg_rating DESC
            LIMIT 5;
            """,
            "Top 5 des logements les mieux notés"
        ),
        (
            """
            SELECT p.title, AVG(r.rating) AS avg_rating
            FROM properties p
            JOIN bookings b ON p.property_id = b.property_id
            JOIN reviews r ON b.booking_id = r.booking_id
            GROUP BY p.title
            ORDER BY avg_rating ASC
            LIMIT 5;
            """,
            "Top 5 des logements les moins bien notés"
        ),
        (
            """
            SELECT DATE_TRUNC('month', start_date) AS month, COUNT(*) AS bookings_count
            FROM bookings
            WHERE start_date >= CURRENT_DATE - INTERVAL '1 year'
            GROUP BY month
            ORDER BY month;
            """,
            "Nombre total de réservations par mois sur l'année écoulée"
        ),
        (
            """
            SELECT DATE_TRUNC('month', start_date) AS month, COUNT(*) AS bookings_count
            FROM bookings
            WHERE start_date >= CURRENT_DATE - INTERVAL '1 year'
            AND canceled = FALSE
            GROUP BY month
            ORDER BY month;
            """,
            "Nombre de réservations non annulées par mois sur l'année écoulée"
        ),
        (
            """
            SELECT p.location AS city, COUNT(b.booking_id) AS total_bookings
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            GROUP BY p.location
            ORDER BY total_bookings DESC
            LIMIT 10;
            """,
            "Top 10 des villes avec le plus de réservations"
        ),
        (
            """
            SELECT p.location AS city, COUNT(b.booking_id) AS total_bookings
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            WHERE b.canceled = FALSE
            GROUP BY p.location
            ORDER BY total_bookings DESC
            LIMIT 10;
            """,
            "Top 10 des villes avec le plus de réservations non annulées"
        ),
        (
            """
            SELECT p.location AS city, COUNT(b.booking_id) AS total_bookings
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            WHERE b.canceled = TRUE
            GROUP BY p.location
            ORDER BY total_bookings DESC
            LIMIT 10;
            """,
            "Top 10 des villes avec le plus de réservations annulées"
        ),
        (
            """
            SELECT u.name AS owner_name, SUM(b.total_price) AS total_revenue
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            JOIN users u ON p.owner_id = u.user_id
            GROUP BY u.name
            ORDER BY total_revenue DESC
            LIMIT 10;
            """,
            "Top 10 des plus gros revenus totaux générés par propriétaire"
        ),
        (
            """
            SELECT u.name AS owner_name, SUM(b.total_price) AS total_revenue
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            JOIN users u ON p.owner_id = u.user_id
            WHERE b.canceled = FALSE
            GROUP BY u.name
            ORDER BY total_revenue DESC
            LIMIT 10;
            """,
            "Top 10 des plus gros revenus totaux générés par propriétaire sans annulation"
        ),
        (
            """
            SELECT p.location AS city, SUM(b.total_price) AS total_revenue
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            GROUP BY p.location
            ORDER BY total_revenue DESC
            LIMIT 10;
            """,
            "Top 10 des plus gros revenus totaux générés par ville"
        ),
        (
            """
            SELECT p.location AS city, SUM(b.total_price) AS total_revenue
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            WHERE b.canceled = FALSE
            GROUP BY p.location
            ORDER BY total_revenue DESC
            LIMIT 10;
            """,
            "Top 10 des plus gros revenus totaux générés par ville sans annulation"
        ),
        (
            """
            SELECT
                ROUND(COUNT(r.review_id)::decimal / COUNT(b.booking_id) * 100, 2) AS review_rate_percent
            FROM bookings b
            LEFT JOIN reviews r ON b.booking_id = r.booking_id
            WHERE b.canceled = FALSE;
            """,
            "Taux d'avis déposés après réservation non annulées"
        ),
        (
            """
            WITH booking_durations AS (
                SELECT
                    property_id,
                    SUM((end_date - start_date)) AS booked_days
                FROM bookings
                GROUP BY property_id
            ),
            total_period AS (
                SELECT
                    MIN(start_date) AS period_start,
                    MAX(end_date) AS period_end
                FROM bookings
            ),
            total_days AS (
                SELECT (period_end - period_start) AS total_days
                FROM total_period
            )
            SELECT
                p.property_id,
                p.title,
                bd.booked_days,
                td.total_days,
                ROUND((bd.booked_days::decimal / td.total_days) * 100, 2) AS occupancy_rate_percent
            FROM booking_durations bd
            JOIN properties p ON bd.property_id = p.property_id
            CROSS JOIN total_days td
            ORDER BY occupancy_rate_percent DESC
            LIMIT 10;
            """,
            "Top 10 des meilleurs taux d'occupations des logements sur toute la période couverte"
        ),
        (
            """
            WITH booking_durations AS (
                SELECT
                    property_id,
                    SUM((end_date - start_date)) AS booked_days
                FROM bookings
                WHERE canceled = FALSE
                GROUP BY property_id
            ),
            total_period AS (
                SELECT
                    MIN(start_date) AS period_start,
                    MAX(end_date) AS period_end
                FROM bookings
            ),
            total_days AS (
                SELECT (period_end - period_start) AS total_days
                FROM total_period
            )
            SELECT
                p.property_id,
                p.title,
                bd.booked_days,
                td.total_days,
                ROUND((bd.booked_days::decimal / td.total_days) * 100, 2) AS occupancy_rate_percent
            FROM booking_durations bd
            JOIN properties p ON bd.property_id = p.property_id
            CROSS JOIN total_days td
            ORDER BY occupancy_rate_percent DESC
            LIMIT 10;
            """,
            "Top 10 des meilleurs taux d'occupations des logements sans annulations sur toute la période couverte"
        ),
        (
            """
            SELECT 
                ROUND(AVG(end_date - start_date), 2) AS avg_nights_per_booking
            FROM bookings;
            """,
            "Nombre moyen de nuits par réservation"
        ),
        (
            """
            SELECT 
                ROUND(AVG(end_date - start_date), 2) AS avg_nights_per_booking
            FROM bookings
            WHERE canceled = FALSE;
            """,
            "Nombre moyen de nuits par réservation sans annulations"
        ),
        (
            """
            WITH first_booking AS (
                SELECT 
                    b.user_id,
                    MIN(b.booking_date) AS first_booking_date
                FROM bookings b
                GROUP BY b.user_id
            )
            SELECT 
                ROUND(AVG(fb.first_booking_date - u.signup_date), 2) AS avg_days_signup_to_first_booking
            FROM first_booking fb
            JOIN users u ON fb.user_id = u.user_id;
            """,
            "Délai moyen entre l'inscription et la première réservation"
        ),
        (
            """
            WITH first_booking AS (
                SELECT 
                    b.user_id,
                    MIN(b.booking_date) AS first_booking_date
                FROM bookings b
                WHERE b.canceled = TRUE
                GROUP BY b.user_id
            )
            SELECT 
                ROUND(AVG(fb.first_booking_date - u.signup_date), 2) AS avg_days_signup_to_first_booking
            FROM first_booking fb
            JOIN users u ON fb.user_id = u.user_id;
            """,
            "Délai moyen entre l'inscription et la première réservation, pour les annulations"
        ),
        (
            """
            WITH bookings_with_season AS (
                SELECT 
                    EXTRACT(YEAR FROM start_date) AS year,
                    CASE 
                        WHEN EXTRACT(MONTH FROM start_date) IN (12, 1, 2) THEN 'Hiver'
                        WHEN EXTRACT(MONTH FROM start_date) IN (3, 4, 5) THEN 'Printemps'
                        WHEN EXTRACT(MONTH FROM start_date) IN (6, 7, 8) THEN 'Été'
                        WHEN EXTRACT(MONTH FROM start_date) IN (9, 10, 11) THEN 'Automne'
                    END AS season
                FROM bookings
            )
            SELECT 
                year,
                season,
                COUNT(*) AS total_bookings
            FROM bookings_with_season
            GROUP BY year, season
            ORDER BY year,
                CASE 
                    WHEN season = 'Hiver' THEN 1
                    WHEN season = 'Printemps' THEN 2
                    WHEN season = 'Été' THEN 3
                    WHEN season = 'Automne' THEN 4
                END;
            """,
            "Nombre global de réservation par saison"
        ),
        (
            """
            WITH bookings_with_season AS (
                SELECT 
                    EXTRACT(YEAR FROM start_date) AS year,
                    CASE 
                        WHEN EXTRACT(MONTH FROM start_date) IN (12, 1, 2) THEN 'Hiver'
                        WHEN EXTRACT(MONTH FROM start_date) IN (3, 4, 5) THEN 'Printemps'
                        WHEN EXTRACT(MONTH FROM start_date) IN (6, 7, 8) THEN 'Été'
                        WHEN EXTRACT(MONTH FROM start_date) IN (9, 10, 11) THEN 'Automne'
                    END AS season
                FROM bookings
                WHERE canceled = TRUE
            )
            SELECT 
                year,
                season,
                COUNT(*) AS total_bookings
            FROM bookings_with_season
            GROUP BY year, season
            ORDER BY year,
                CASE 
                    WHEN season = 'Hiver' THEN 1
                    WHEN season = 'Printemps' THEN 2
                    WHEN season = 'Été' THEN 3
                    WHEN season = 'Automne' THEN 4
                END;
            """,
            "Nombre global de réservation annulées par saison"
        ),
        (
            """ 
            SELECT
                ROUND(100.0 * COUNT(*) FILTER (WHERE canceled = TRUE) / COUNT(*), 2) AS cancellation_rate_percent
            FROM bookings;
            """,
            "Taux global d'annulation de réservation"
        ),
        (
            """ 
            SELECT
                p.location AS city,
                COUNT(*) FILTER (WHERE b.canceled = TRUE) AS canceled_bookings,
                COUNT(*) AS total_bookings,
                ROUND(100.0 * COUNT(*) FILTER (WHERE b.canceled = TRUE) / COUNT(*), 2) AS cancellation_rate_percent
            FROM bookings b
            JOIN properties p ON b.property_id = p.property_id
            GROUP BY p.location
            HAVING COUNT(*) > 0  -- Pour éviter la div/0
            ORDER BY cancellation_rate_percent DESC
            LIMIT 10;
            """,
            "Top 10 des villes avec le plus gros taux d'annulation des réservations"
        )
    ]

    for query, description in queries:
        execute_query(query, description)
            
    return None
