from config.db_utils import connect_cozy_bnb_db


# Vérifie qu’aucun utilisateur ne réserve son propre logement
def test_no_self_booking():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM bookings b
        JOIN properties p ON b.property_id = p.property_id
        WHERE b.user_id = p.owner_id;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} réservation(s) par leurs propres propriétaires !"


# Tous les utilisateurs ont au moins 18 ans
def test_users_are_adults():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM users
        WHERE birth_date > CURRENT_DATE - INTERVAL '18 years';
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} utilisateur(s) ont moins de 18 ans !"


# Vérifie que chaque chambre peut faire au moins 9m^2
def test_surface_vs_bedrooms():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM properties
        WHERE surface_m2 < num_bedrooms * 9;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} propriétés ont une surface incohérente avec le nombre de chambres !"


# Vérifie que le nombre de chambres, n'est pas supérieur au nombre max d'occupants du logement
def test_max_occupants_vs_bedrooms():
    conn = connect_cozy_bnb_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM properties
        WHERE max_occupants < num_bedrooms;
    """)
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count == 0, f"{count} propriétés n'ont pas assez d'occupants pour le nombre de chambres !"
