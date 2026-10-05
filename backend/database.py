import os
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL")


conexion = psycopg2.connect(
    DATABASE_URL
)