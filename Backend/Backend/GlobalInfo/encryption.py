from cryptography.fernet import Fernet

# Función para generar una nueva clave
def generate_key():
    return Fernet.generate_key()

# Guardar la clave en un archivo
def save_key(key, filename="clave.key"):
    with open(filename, "wb") as file:
        file.write(key)

# Cargar la clave desde un archivo
def load_key(filename="clave.key"):
    with open(filename, "rb") as file:
        return file.read()

# Cifrar los datos
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Descifrar los datos
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# === PRUEBA ===
if __name__ == "__main__":
    # Paso 1: Generar y guardar la clave
    key = generate_key()
    save_key(key)

    # Paso 2: Cargar la clave
    key = load_key()

    # Paso 3: Cifrar un dato sensible (tarjeta de crédito)
    dato_cifrado = encrypt_data("4111111111111111", key)
    print("Cifrado:", dato_cifrado)

    # Paso 4: Descifrar el dato
    dato_original = decrypt_data(dato_cifrado, key)
    print("Original:", dato_original)
