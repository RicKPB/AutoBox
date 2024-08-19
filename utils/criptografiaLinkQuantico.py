from utils.dataEncryption import validate_key
from fernet import Fernet
import utils.dataEncryption

utils.dataEncryption.generate_key()

key = utils.dataEncryption.load_key()

if validate_key(key):
    f = Fernet(key)
else:
    print("Invalid key format.")

date = input(str("Digite a informacao: "))

date_link = dict()

date_link.setdefault('link', date)

utils.dataEncryption.save_credentials(date_link, "Y:/AUTOBOX/CriptografiaLinkQuantico/linkSistema.enc", key)

load_dateSys = utils.dataEncryption.load_credentials("Y:/AUTOBOX/CriptografiaLinkQuantico/linkSistema.enc", key)
print(load_dateSys)

if validate_key(key):
    f = Fernet(key)
else:
    print("Invalid key format.")
