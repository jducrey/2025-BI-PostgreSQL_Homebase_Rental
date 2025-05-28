# main.py
from scripts.create_cozy_bnb_db import create_cozy_bnb_db
from scripts.init_tables import init_tables
from scripts.insert_data import insert_data
from scripts_datas_build.Increase_users_and_properties import increase_users_and_properties
from scripts_datas_build.Increase_bookings_and_reviews import increase_bookings_and_reviews
import pytest


if __name__ == "__main__":
    print("\n🔧 Création de la base...")
    create_cozy_bnb_db()

    print("\n📐 Initialisation des tables...")
    init_tables()

    print("\n📊 Génération des utilisateurs et propriétés...")
    # increase_users_and_properties()

    print("\n📅 Génération des réservations et des avis...")
    # increase_bookings_and_reviews()

    print("\n📥 Initialisation des tables...")
    insert_data()

    print("\n🧪 Tests de la qualité des données...")
    exit_code=pytest.main(["scripts_tests_data_quality/test_data_integrity.py",
                 "scripts_tests_data_quality/test_data_consistency.py",
                 "scripts_tests_data_quality/test_temporal_logic.py",
                 "scripts_tests_data_quality/test_relations.py",
                 "scripts_tests_data_quality/test_edge_cases.py"])
    if exit_code != 0:
        print("❌ Tests échoués, checkez les logs.")
        exit(exit_code)
    
    print("\n✅ Tout est prêt, chef !")