# Exemple : vérifier les chevauchements de réservations
import pandas as pd
from datetime import datetime

def test_no_overlapping_bookings():
    bookings = pd.read_csv('datas/bookings.csv')
    bookings['start_date'] = pd.to_datetime(bookings['start_date'])
    bookings['end_date'] = pd.to_datetime(bookings['end_date'])

    overlapping_found = False
    errors = []

    for property_id, group in bookings.groupby('property_id'):
        sorted_group = group.sort_values(by='start_date')
        for i in range(len(sorted_group) - 1):
            current_end = sorted_group.iloc[i]['end_date']
            next_start = sorted_group.iloc[i + 1]['start_date']
            if next_start < current_end:
                overlapping_found = True
                errors.append({
                    "property_id": property_id,
                    "booking_1": sorted_group.iloc[i]['booking_id'],
                    "booking_2": sorted_group.iloc[i + 1]['booking_id'],
                    "overlap_start": next_start,
                    "overlap_end": current_end
                })

    if overlapping_found:
        print(f"❌ {len(errors)} conflits détectés dans les réservations.")
        for e in errors[:10]:  # Limiter à 10 conflits affichés
            print(f" - Logement {e['property_id']} : bookings {e['booking_1']} et {e['booking_2']} se chevauchent ({e['overlap_start']} < {e['overlap_end']})")
        assert False, "Des chevauchements de réservations ont été détectés."
    else:
        print("✅ Test passé : Aucun chevauchement détecté entre les bookings.")
