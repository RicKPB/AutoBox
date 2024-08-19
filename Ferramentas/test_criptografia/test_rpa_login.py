from cryptography.fernet import Fernet
import json
import tkinter as tk
from tkinter import messagebox
from functools import partial

def load_key():
    return open("Y:/AUTOBOX/CriptografiaUserPermission/KeySecretUserSystem.key", "rb").read()


def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()


def load_credentials(filename, key):
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = decrypt_data(encrypted_data, key)
    return json.loads(decrypted_data)


def login(credentials, username, password):
    if username in credentials and credentials[username] == password:
        return True
    else:
        return False


def run_rpa():
    messagebox.showinfo("RPA", "RPA Executada com Sucesso!")


def authenticate(credentials, entry_username, entry_password, root):
    username = entry_username.get()
    password = entry_password.get()
    if login(credentials, username, password):
        messagebox.showinfo("Login", "Login bem-sucedido!")
        root.destroy()
        run_rpa()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")


def login_screen(credentials):
    root = tk.Tk()
    root.title("Login RPA")

    tk.Label(root, text="Usuário").grid(row=0, column=0)
    tk.Label(root, text="Senha").grid(row=1, column=0)

    entry_username = tk.Entry(root)
    entry_password = tk.Entry(root, show="*")

    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    authenticate_partial = partial(authenticate, credentials, entry_username, entry_password, root)

    tk.Button(root, text="Login", command=authenticate_partial).grid(row=2, column=1)

    root.mainloop()


if __name__ == "__main__":
    key = load_key()
    loaded_credentials = load_credentials("Y:/AUTOBOX/CriptografiaUserPermission/permissionUserSys.enc", key)
    login_screen(loaded_credentials)
