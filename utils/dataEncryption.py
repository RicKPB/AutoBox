from cryptography.fernet import Fernet
import json
import base64


# Gera uma chave no modo binario wb, write/binary.
def generate_key():
    key = Fernet.generate_key()
    with open("Y:/AUTOBOX/CriptografiaLinkQuantico/keySecretLinkSystem.key", "wb") as key_file:
        key_file.write(key)


# Carrega a chave em modo rb read/binary, aonde permite fazer a abertura/leitura do arquivo binario.
def load_key():
    with open("Y:/AUTOBOX/CriptografiaLinkQuantico/keySecretLinkSystem.key", "rb") as key_file:
        key = key_file.read()
    return key


# Funcao aonde permite que criptografe dados usando a chave secreta
# Recebe o parametro data (dados para criptografar e a key (chave secreta)
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


# Funcao aonde descriptografa os dados criptografados usando a chave secreta.
# Recebe os parametros da funcao anterior (dados criptografados) e a key (chave secreta)
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()


# Funcao para salvar os dados passados para o arq criptografados
# Recebe information (informacao para criptografar) - dicionario deve ser feito
# Recebe filename (nome do arquivo aonde sera realizado o save)
# Recebe key (chave secreta)
# Abre o arquivo em modo binario (wb), escreve os dados e fecha o arquivo
def save_credentials(information, filename, key):
    encrypted_data = encrypt_data(json.dumps(information), key)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


# Funcao para carregar os dados criptografados de um arquivo
# Recebe filename (nome do arquivo aonde estao os dados)
# Recebe a key (chave secreta)
# Funcao abre o arquivo no modo binario (rb) le os dados e descriptografa os dados
def load_credentials(filename, key):
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    return json.loads(decrypted_data)


def validate_key(key):
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
