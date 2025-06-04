# 🏠 Cozybnb – Data Pipeline & BI sur données locatives

![Pytest](https://img.shields.io/badge/tests-passing-brightgreen?style=flat&logo=pytest)

Projet personnel de **Data Engineering & Analysis**, basé sur une plateforme fictive de locations de logements.  
🎯 Objectif : démontrer la capacité à construire **un pipeline de données réaliste**, à en garantir **la qualité métier**, et à produire des **insights actionnables** comme en entreprise.

---

## 🔍 Objectifs du projet

- Générer des **données synthétiques réalistes** sur 4 tables : `users`, `properties`, `bookings`, `reviews`
- Construire une **base PostgreSQL propre** (modèle relationnel, contraintes)
- Garantir la **qualité des données** via des tests automatisés (intégrité, cohérence métier, logique temporelle)
- Réaliser une **analyse SQL poussée** (KPI, segmentations, tendances)
- Proposer une **visualisation Power BI** directement exploitable

---

## 🧱 Architecture & pipeline

```bash
📦 PostgreSQL_Homebase-Rental_Project/
│
├── config/
|   ├── __init__.py
|   ├── db_utils.py
|   └── psql_var.py         # Fichier à remplir avec vos mdp psql.
|
├── dashboard/
|   └── CozyBnB_Dashboard.pbix
|
├── datas/                  # Fichiers CSV générés
│   ├── bookings.csv
|   ├── properties.csv
|   ├── reviews.csv
|   └── users.csv
|
├── queries/
│   ├── Average_mark_by_property.sql
│   ├── Bookings_quantity_on_last_year.sql
│   ├── Top5_most_booked_properties.sql
│   └── Total_revenue_by_property.sql
│
├── scripts/
│   ├── __init__.py
│   ├── create_cozy_bnb_db.py
│   ├── init_tables.py
│   ├── insert_data.py
│   └── queries.py
│
├── scripts_datas_build/
│   ├── Add_birth_date.py
│   ├── Add_booking_date.py
│   ├── Add_gender.py
│   ├── Add_num_bathrooms.py
│   ├── Add_num_bedrooms.py
│   ├── Add_parking.py
│   ├── Add_review_date.py
│   ├── Add_surface.py
│   ├── Add_user_coords.py
│   ├── Add_Wifi.py
│   ├── Increase_bookings_and_reviews.py    # Script of bookings and reviews datas generations
│   └── Increase_users_and_properties.py    # Script of users and properties datas generations
│
├── scripts_tests_data_quality/
│   ├── __init__.py
│   ├── test_data_consistency.py
│   ├── test_data_integrity.py
│   ├── test_edge_cases.py
│   ├── test_relations.py
│   └── test_temporal_logic.py
│
├── main.py                # Pipeline complet automatisé
├── README.md
└── requirements.txt
```

---

## 🧪 Qualité des données & validation

✅ Données validées par des tests Pytest :

- **Intégrité des IDs & clés étrangères**
- **Chronologie cohérente** (`signup_date < booking_date`, etc.)
- **Règles métiers réalistes** (ex : pas d’auto-réservation)
- **Distributions logiques** (répartition France/étranger, types de logements, etc.)

---

## ⚙️ Stack technique

- **Python** : génération & tests (`pandas`, `faker`, `pytest`)
- **PostgreSQL** : modélisation relationnelle, KPI
- **Git & GitHub** : versioning et collaboration
- **Power BI** : tableau de bord visuel final
- **VS Code** : IDE principal

---

## 📊 Exemples d'insights extraits

- 🌍 Taux d’occupation par région
- 🛏️ Revenus par type de logement
- 📆 Détection de la saisonnalité
- 👤 Segmentation des utilisateurs

---

## 🚀 Pour lancer le projet en local

1. Cloner le dépôt :
```bash
git clone https://github.com/jducrey/cozybnb.git
cd cozybnb
```

2. Lancer le pipeline principal :
```bash
python main.py
```

3. Explorer le dashboard Power BI dans
```bash
dashboards/cozybnb_powerbi.pbix
```

---

## Branches terminées (supprimées)

- `data-quality-test` : contenait le développement des tests de cohérence métier (réservations non-chevauchantes, âge légal, cohérence temporelle, etc.). Mergée dans `main` le 2025-05-31

- `add_README.md` : contenait le développement du fichier de documentation README.md, permettant de présenter le but du projet (Objectif métier, Objectif Technique, Architecture, ...). Mergée dans `main` le 2025-06-04 via [Pull Request #13](lien-vers-la-pr-si-dispo).

- `Add_queries_for_KPIs` : contenait le développement du script queries.py, permettant le calcul d'une partie des KPIs nécessaires, pour l'analyse des données d'une vraie plateforme de locations de logements. Mergée dans `main` le 2025-06-04 via [Pull Request #15](lien-vers-la-pr-si-dispo).

--- 

## 🤝 À propos
Projet solo mené par Julien Ducrey dans le cadre de sa montée en compétences continue sur la Data Engineering & Analytics.

🎯 Objectif : **remplacer les données synthétiques par des données réelles sans modifier l’infrastructure**, et produire des insights directement exploitables.

    Tu veux voir comment je peux transformer tes données en insights ? Jette un œil au repo 👇
    🔗 Mon portfolio GitHub