import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psql_var import userName, mdp

# Connexion à la base 'postgres' (par défaut) pour créer une autre base
conn = psycopg2.connect(
    dbname="postgres",
    user=userName,
    password=mdp,
    host="localhost",
    port="5432"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # obligatoire pour CREATE DATABASE
cur = conn.cursor()

# Nom de la base à créer
db_name = "cozybnb_db"

# Création de la base
try:
    cur.execute(f"CREATE DATABASE {db_name};")
    print(f"Base de données '{db_name}' créée avec succès.")
except psycopg2.errors.DuplicateDatabase:
    print(f"La base '{db_name}' existe déjà.")
finally:
    cur.close()
    conn.close()
