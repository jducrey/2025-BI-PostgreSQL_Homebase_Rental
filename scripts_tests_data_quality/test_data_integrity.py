from config.db_utils import connect_cozy_bnb_db


# Aucun doublon d’ID dans les tables
def test_no_duplicate_ids():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    for table, id_col in [('users', 'user_id'), ('properties', 'property_id'),
                          ('bookings', 'booking_id'), ('reviews', 'review_id')]:
        cur.execute(f"""
            SELECT COUNT(*) - COUNT(DISTINCT {id_col}) FROM {table};
        """)
        dup = cur.fetchone()[0]
        assert dup == 0, f"{dup} doublon(s) d’ID dans la table {table} !"
    cur.close()
    conn.close()


# Aucun doublons d'email, pour les utilisateurs
def test_unique_emails():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM (
            SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1
        ) AS duplicates;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} email(s) en double dans les utilisateurs !"


# Tous les logements ont un propriétaire valide
def test_all_properties_have_owners():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM properties p
        LEFT JOIN users u ON p.owner_id = u.user_id
        WHERE u.user_id IS NULL;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} logements sans propriétaire valide !"


# Chaque review est associée à une réservation existante
def test_reviews_linked_to_existing_booking():
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
    assert count == 0, f"{count} review(s) sans réservation valide !"


# Aucun logement n'est loué gratuitement
def test_price_per_night_positive():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM properties WHERE price_per_night <= 0;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} logements ont un prix invalide (≤ 0 €) !"


# Aucune valeur manquantes dans les colonnes critiques
def test_null_values_critical_columns():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT COUNT(*) FROM users WHERE user_id IS NULL OR name IS NULL OR signup_date IS NULL
    UNION
    SELECT COUNT(*) FROM properties WHERE property_id IS NULL OR owner_id IS NULL OR price_per_night IS NULL
    UNION
    SELECT COUNT(*) FROM bookings WHERE booking_id IS NULL OR user_id IS NULL OR property_id IS NULL OR start_date IS NULL OR end_date IS NULL OR booking_date IS NULL;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} valeurs NULL détectées dans des colonnes critiques"


# Vérifie que si canceled = TRUE alors cancellation_date est bien NON NULL.
def test_cancellation_date_not_null_when_canceled():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM bookings
        WHERE canceled = TRUE
          AND cancellation_date IS NULL;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} booking(s) annulé(s) sans cancellation_date !"


# Vérifie que si canceled = FALSE alors cancellation_date est bien NULL.
def test_cancellation_date_null_when_not_canceled():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM bookings
        WHERE canceled = FALSE
          AND cancellation_date IS NOT NULL;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} booking(s) non annulé(s) avec une cancellation_date !"

