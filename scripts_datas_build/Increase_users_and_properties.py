# scripts_datas_build/Increase_users_and_properties.py
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

def increase_users_and_properties():
    # Config
    faker_fr = Faker('fr_FR')
    faker_all = Faker()
    Faker.seed(42)
    random.seed(42)

    NUM_USERS = 300
    NUM_PROPERTIES = 1000
    PERCENT_FOREIGN = 0.3

    title_templates = [
        "{} {} au cœur de {}",
        "{} {} avec vue sur {}",
        "{} {} proche de {}",
        "{} {} dans un quartier branché de {}",
        "{} {} à {}",
        "{} {} près de {}",
        "{} {} à proximité de {}",
        "{} {} en plein coeur de {}",
        "{} {} pourvu d'un beau panorama sur {}"
    ]
    types = ['Studio', 'Appartement', 'Duplex', 'Loft', 'T2', 
            'Chalet', 'Maison', 'Gite', 'Villa', 'Yourte', 'Cabane',
            'Pavillon']
    adjectives = ['cozy','moderne','rustique','typique','traditionnelle',
                'rural','spacieux', 'familial', 'romantique', 'lumineux',
                'luxueux', 'charmant', 'magnifique', 'paisible', 'calme']

    # Load existing data
    users_file = 'datas/users.csv'
    properties_file = 'datas/properties.csv'

    if os.path.exists(users_file):
        existing_users = pd.read_csv(users_file)
        max_user_id = existing_users['user_id'].max()
    else:
        existing_users = pd.DataFrame()
        max_user_id = 0

    if os.path.exists(properties_file):
        existing_properties = pd.read_csv(properties_file)
        max_property_id = existing_properties['property_id'].max()
    else:
        existing_properties = pd.DataFrame()
        max_property_id = 0

    # Helper functions
    def generate_birthdate():
        today = datetime.today()
        age = random.randint(18, 70)
        birth_date = today - timedelta(days=365 * age + random.randint(0, 364))
        return birth_date.date()

    def generate_sex_and_name(is_foreign):
        sex = random.choice(['M', 'F'])
        if is_foreign:
            if sex == 'M':
                first_name = faker_all.first_name_male()
            else:
                first_name = faker_all.first_name_female()
            last_name = faker_all.last_name()
            name = f"{first_name} {last_name}"
            return sex, name
        else:
            if sex == 'M':
                first_name = faker_fr.first_name_male()
            else:
                first_name = faker_fr.first_name_female()
            last_name = faker_fr.last_name()
            name = f"{first_name} {last_name}"
            return sex, name

    def generate_phone_and_address(is_foreign):
        if is_foreign:
            return faker_all.phone_number(), faker_all.address().replace("\n", ", ")
        else:
            return faker_fr.phone_number(), faker_fr.address().replace("\n", ", ")

    # Generate users
    def generate_users(num_users, start_id):
        users = []
        for i in range(num_users):
            is_foreign = (i >= int((1 - PERCENT_FOREIGN) * num_users))
            sex, name = generate_sex_and_name(is_foreign)
            phone, address = generate_phone_and_address(is_foreign)
            email = f"{name.lower()}.{random.randint(1000,9999)}@example.com"
            signup_date = faker_fr.date_between(start_date='-5y', end_date='today')
            birth_date = generate_birthdate()
            users.append({
                'user_id': start_id + i + 1,
                'name': name,
                'email': email,
                'signup_date': signup_date,
                'birth_date': birth_date,
                'phone': phone,
                'address': address,
                'sex': sex
            })
        return pd.DataFrame(users)

    # Generate properties (France only, all with real user as owner)
    def generate_properties(num_props, start_id, user_pool):
        props = []
        for i in range(num_props):
            owner = user_pool.sample(1).iloc[0]
            prop_type = random.choice(types)
            city = faker_fr.city()
            num_bedrooms = random.randint(1, 6)  # ou autre logique de ton code
            surface_min = num_bedrooms * 10
            surface_max = num_bedrooms * 25
            surface_m2 = random.randint(surface_min, surface_max)
            props.append({
                'property_id': start_id + i + 1,
                'owner_id': owner['user_id'],
                'property_type': prop_type,
                'title': random.choice(title_templates).format(prop_type, random.choice(adjectives), city),
                'location': city,
                'price_per_night': random.randint(30, 500),
                'max_occupants': random.randint(num_bedrooms, 8),
                'surface_m2': surface_m2,
                'parking_spaces': random.randint(0, 2),
                'wifi_access': random.choice([True, False]),
                'num_bedrooms': num_bedrooms,
                'num_bathrooms': random.randint(1, 3),
            })
        return pd.DataFrame(props)

    # Run generation
    new_users = generate_users(NUM_USERS, max_user_id)
    all_users = pd.concat([existing_users, new_users], ignore_index=True)

    # Properties only for French users (first 70%)
    french_users = new_users.iloc[:int((1 - PERCENT_FOREIGN) * NUM_USERS)]
    new_props = generate_properties(NUM_PROPERTIES, max_property_id, french_users)
    all_props = pd.concat([existing_properties, new_props], ignore_index=True)

    # Save back to CSV
    all_users.to_csv('datas/users.csv', index=False)
    all_props.to_csv('datas/properties.csv', index=False)
    # Save to CSV
    # all_users.to_csv(users_file, index=False)
    # all_props.to_csv(properties_file, index=False)

    print(f"{NUM_USERS} utilisateurs ajoutés (dont {int(PERCENT_FOREIGN * NUM_USERS)} étrangers)")
    print(f"{NUM_PROPERTIES} logements ajoutés, tous en France 🇫🇷")

    return None