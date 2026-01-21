from Backend.GlobalInfo.keys import get_db_connection

# Obtener todos los usuarios
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

# Obtener un usuario por ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Crear un nuevo usuario
def add_user(name, email, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, email, password, role))
    conn.commit()  # Guardamos los cambios
    user_id = cursor.lastrowid  # Obtenemos el ID del usuario creado
    conn.close()
    return user_id

# Actualizar un usuario
def update_user(user_id, name, email, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "UPDATE usuarios SET nombre = %s, email = %s, rol = %s WHERE id = %s"
    cursor.execute(sql, (name, email, role, user_id))
    conn.commit()
    conn.close()
    return cursor.rowcount  # Retorna la cantidad de filas afectadas

# Eliminar un usuario
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM usuarios WHERE id = %s"
    cursor.execute(sql, (user_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount  # Retorna la cantidad de filas eliminadas





# ==========================
#  UNIDADES
# ==========================

def get_all_unidades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM unidades")
    unidades = cursor.fetchall()
    conn.close()
    return unidades

def add_unidad(nombre, numero_economico, latitud, longitud, ruta_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO unidades (nombre, numero_economico, latitud, longitud, ruta_id) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (nombre, numero_economico, latitud, longitud, ruta_id))
    conn.commit()
    unidad_id = cursor.lastrowid
    conn.close()
    return unidad_id

# ==========================
#  RUTAS
# ==========================

def get_all_rutas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rutas")
    rutas = cursor.fetchall()
    conn.close()
    return rutas

def add_ruta(nombre, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO rutas (nombre, descripcion) VALUES (%s, %s)"
    cursor.execute(sql, (nombre, descripcion))
    conn.commit()
    ruta_id = cursor.lastrowid
    conn.close()
    return ruta_id

# ==========================
#  PARADAS
# ==========================

def get_all_paradas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paradas")
    paradas = cursor.fetchall()
    conn.close()
    return paradas

def add_parada(nombre, latitud, longitud):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO paradas (nombre, latitud, longitud) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, latitud, longitud))
    conn.commit()
    parada_id = cursor.lastrowid
    conn.close()
    return parada_id
