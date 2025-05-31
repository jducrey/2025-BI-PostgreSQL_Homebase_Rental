from config.db_utils import connect_cozy_bnb_db


# booking_date < start_date
def test_booking_date_before_start_date():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM bookings
        WHERE booking_date >= start_date;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} réservation(s) ont une date de réservation après ou égale à la date de début !"


# start_date < end_date
def test_start_before_end_date():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM bookings
        WHERE start_date >= end_date;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} réservation(s) ont une date de début après ou égale à la date de fin !"


# review_date > end_date
def test_review_after_booking_end():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM reviews r
        JOIN bookings b ON r.booking_id = b.booking_id
        WHERE r.review_date <= b.end_date;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} review(s) écrite(s) avant ou pendant le séjour !"


# signup_date <= booking_date
def test_signup_before_booking():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        WHERE b.booking_date < u.signup_date;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} réservations ont été faites avant l'inscription de l'utilisateur !"
