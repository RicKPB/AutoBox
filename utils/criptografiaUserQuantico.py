from utils.userEncryption import valideKeyUser
from fernet import Fernet
import utils.userEncryption
import os

utils.userEncryption.generateKeyUser()

keyUser = utils.userEncryption.loadKeyUser()

if valideKeyUser(keyUser):
    f = Fernet(keyUser)
else:
    print('Invalid key format!!')

# quantUsers = input(int('Digite a quantidade de usuarios: '))

dateUser = dict()

while True:

    userLogin = input('Digite o usuario: ')
    userPassword = input('Digite a senha: ')

    os.system('cls')

    dateUser.setdefault(userLogin, userPassword)

    sair = input('Quer sair? [s]air: ').lower().startswith('s')
    if sair is True:
        utils.userEncryption.saveCredentialsUser(dateUser, 'Y:/AUTOBOX/CriptografiaUserPermission/permissionUserSys.enc', keyUser)
        userDataSys = utils.userEncryption.loadCredentialsUser('Y:/AUTOBOX/CriptografiaUserPermission/permissionUserSys.enc', keyUser)
        print('Sistema finalizado!')
        break

print(userDataSys)
