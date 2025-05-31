from config.db_utils import connect_cozy_bnb_db


# Vérifie que chaque review est relié à une réservation, qui existe bien
def test_no_orphan_reviews():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM reviews r
        LEFT JOIN bookings b ON r.booking_id = b.booking_id
        WHERE b.booking_id IS NULL;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} reviews ne sont liées à aucune réservation !"


# Vérifie qu'il n'y a pas deux reviews différents liées à la même réservation
def test_reviews_unique_per_booking():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM (
            SELECT booking_id FROM reviews GROUP BY booking_id HAVING COUNT(*) > 1
        ) AS duplicates;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} réservations ont plusieurs reviews associées !"


# Chaque réservation a au maximum une review
def test_max_one_review_per_booking():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM (
            SELECT booking_id, COUNT(*) AS nb_reviews
            FROM reviews
            GROUP BY booking_id
            HAVING COUNT(*) > 1
        ) AS excessive_reviews;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} réservation(s) ont plus d'une review !"
