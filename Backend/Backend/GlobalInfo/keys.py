import os
import mysql.connector

# Configuración de la conexión a MySQL
DB_CONFIG = {
    "host": "localhost",  # Cambia según tu configuración
    "user": "root",       # Usuario de la base de datos
    "password": "",       # Contraseña de la base de datos
    "database": "yovoy"  # Nombre de tu base de datos
}

# Función para obtener conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
