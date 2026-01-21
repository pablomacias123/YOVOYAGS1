from flask import Flask, jsonify, request
from flask_cors import CORS
import Backend.Functions as callMethod
import Backend.GlobalInfo.Helpers as HelperFunctions

app = Flask(__name__)
CORS(app)

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = callMethod.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500  # Mensaje de error más claro

# Ruta para obtener un usuario por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = callMethod.get_user_by_id(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500  # Mensaje de error más claro

# Ruta para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        nombre = data.get('nombre')
        email = data.get('email')
        contraseña = data.get('contraseña')
        rol = data.get('rol')
        user_id = callMethod.add_user(nombre, email, contraseña, rol)
        return jsonify({"message": "User created", "id": user_id}), 201
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500  # Mensaje de error más claro

# Ruta para actualizar un usuario
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        nombre = data.get('nombre')
        email = data.get('email')
        rol = data.get('rol')
        affected_rows = callMethod.update_user(user_id, nombre, email, rol)
        if affected_rows > 0:
            return jsonify({"message": "User updated"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500  # Mensaje de error más claro

# Ruta para eliminar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        affected_rows = callMethod.delete_user(user_id)
        if affected_rows > 0:
            return jsonify({"message": "User deleted"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500  # Mensaje de error más claro







@app.route('/unidades', methods=['GET'])
def get_unidades():
    try:
        unidades = callMethod.get_all_unidades()
        return jsonify(unidades), 200
    except Exception as e:
        HelperFunctions.PrintException()
        return jsonify({'error': 'Error interno del servidor.'}), 500

@app.route('/unidades', methods=['POST'])
def create_unidad():
    try:
        data = request.json
        nombre = data.get('nombre')
        numero_economico = data.get('numero_economico')
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        ruta_id = data.get('ruta_id')
        unidad_id = callMethod.add_unidad(
            nombre, numero_economico, latitud, longitud, ruta_id
        )
        return jsonify({"message": "Unidad creada", "id": unidad_id}), 201
    except Exception as e:
        HelperFunctions.PrintException()
        return jsonify({'error': 'Error interno del servidor.'}), 500

# ==========================
#  RUTAS
# ==========================

@app.route('/rutas', methods=['GET'])
def get_rutas():
    try:
        rutas = callMethod.get_all_rutas()
        return jsonify(rutas), 200
    except Exception as e:
        HelperFunctions.PrintException()
        return jsonify({'error': 'Error interno del servidor.'}), 500

@app.route('/rutas', methods=['POST'])
def create_ruta():
    try:
        data = request.json
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        ruta_id = callMethod.add_ruta(nombre, descripcion)
        return jsonify({"message": "Ruta creada", "id": ruta_id}), 201
    except Exception as e:
        HelperFunctions.PrintException()
        return jsonify({'error': 'Error interno del servidor.'}), 500

# ==========================
#  PARADAS
# ==========================

@app.route('/paradas', methods=['GET'])
def get_paradas():
    try:
        paradas = callMethod.get_all_paradas()
        return jsonify(paradas), 200
    except Exception as e:
        HelperFunctions.PrintException()
        return jsonify({'error': 'Error interno del servidor.'}), 500

@app.route('/paradas', methods=['POST'])
def create_parada():
    try:
        data = request.json
        nombre = data.get('nombre')
        latitud = data.get('latitud')
        longitud = data.get('longitud')
        parada_id = callMethod.add_parada(
            nombre, latitud, longitud
        )
        return jsonify({"message": "Parada creada", "id": parada_id}), 201
    except Exception as e:
        HelperFunctions.PrintException()
        return jsonify({'error': 'Error interno del servidor.'}), 500










# Ejecutar la API
if __name__ == '__main__':
    app.run(debug=True)



# API para el registro de usuarios
@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()
        strFirstName = data.get('strFirstName')
        strLastName = data.get('strLastName')
        strEmail = data.get('strEmail')
        strPassword = data.get('strPassword')
        strPhone = data.get('strPhone')
        strAddress = data.get('strAddress')
        strPostalCode = data.get('strPostalCode')
        strTitularNombre = data.get('strTitularNombre')
        strCardNumber = data.get('strCardNumber')
        strExpirationDate = data.get('strExpirationDate')
        strSecurityCode = data.get('strSecurityCode')

        # Llama a la función en Functions.py para insertar el usuario
        documento_actualizado = callMethod.insert_usuario_log({
            "strFirstName": strFirstName,
            "strLastName": strLastName,
            "strEmail": strEmail,
            "strPassword": strPassword,
            "strPhone": strPhone,
            "strAddress": strAddress,
            "strPostalCode": strPostalCode,
            "strTitularNombre": strTitularNombre,
            "strCardNumber": strCardNumber,
            "strExpirationDate": strExpirationDate,
            "strSecurityCode": strSecurityCode,
            "role":"admin"
        })

        return jsonify(documento_actualizado), 201  # Retorna el resultado en formato JSON y el código de estado 201

    except Exception as e:
        HelperFunctions.PrintException()
        print(str(e))
        return jsonify({'error': 'Error interno del servidor.'}), 500  # Mensaje de error más claro
