# config/db_utils.py
import psycopg2
from config.psql_var import userName, mdp

def connect_cozy_bnb_db():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="cozybnb_db",
        user=userName,
        password=mdp
    )