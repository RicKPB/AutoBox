from cryptography.fernet import Fernet
import json
import base64


# Gera uma chave no modo binario wb, write/binary.
def generateKeyUser():
    key = Fernet.generate_key()
    with open("Y:/AUTOBOX/CriptografiaUserPermission/KeySecretUserSystem.key", "wb") as key_file:
        key_file.write(key)


def loadKeyUser():
    with open("Y:/AUTOBOX/CriptografiaUserPermission/KeySecretUserSystem.key", "rb") as key_file:
        key = key_file.read()
    return key


def encryptDataUser(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decryptDataUser(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()


def saveCredentialsUser(information, filename, key):
    encrypted_data = encryptDataUser(json.dumps(information), key)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


# Funcao para carregar os dados criptografados de um arquivo
# Recebe filename (nome do arquivo aonde estao os dados)
# Recebe a key (chave secreta)
# Funcao abre o arquivo no modo binario (rb) le os dados e descriptografa os dados
def loadCredentialsUser(filename, key):
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = decryptDataUser(encrypted_data, key)
    return json.loads(decrypted_data)


def valideKeyUser(key):
    try:
        print(f"Key length: {len(key)}")
        print(f"Key content: {key}")
        if isinstance(key, str):
            key = key.encode()

        if len(key) != 44:
            raise ValueError("Invalid key length. Must be 44 characters.")

        decoded_key = base64.urlsafe_b64decode(key)
        return len(decoded_key) == 32
    except Exception as e:
        print(f"Key validation failed: {e}")
        return False
