import utils.userEncryption
import tkinter as tk
from model.inputBox import InputBox
import os
import json
from tkinter import messagebox
import fernet


def load_credentials():
    file_path = os.path.join(os.path.dirname(__file__), 'credentials.enc')
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    credentials = {}
    for line in decrypted_data.splitlines():
        username, password = line.split(':')
        credentials[username] = password
    return credentials

class LoginScreen:
    def __init__(self, root):

        self.root = root
        self.root.title("Tela de Login")
        self.root.geometry("300x150")
        self.root.configure(bg='#f0f0f0')

        # Título da tela de login
        self.label_title = tk.Label(self.root, text="Login", font=('Arial', 18), bg='#f0f0f0')
        self.label_title.pack(pady=10)

        # Frame para campos de login
        self.frame_login = tk.Frame(self.root, bg='#f0f0f0')
        self.frame_login.pack(pady=10)

        self.label_username = tk.Label(self.frame_login, text='Usuário:', bg='#f0f0f0')
        self.label_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.entry_username = tk.Entry(self.frame_login)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = tk.Label(self.frame_login, text='Senha:', bg='#f0f0f0')
        self.label_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.entry_password = tk.Entry(self.frame_login, show='*')
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.button_login = tk.Button(self.root, text="Login", command=self.login)
        self.button_login.pack(pady=10)

        self.root.bind("<Return>", lambda event: self.login())

    @staticmethod
    def validate_credentials(username, password):
        try:
            # Ler e descriptografar o arquivo de credenciais
            encrypted_file_path = os.path.join(os.path.dirname(__file__), 'Y:/AUTOBOX/CriptografiaUserPermission/permissionUserSys.enc')
            with open(encrypted_file_path, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = utils.userEncryption.decryptDataUser(encrypted_data)
            credentials = json.loads(decrypted_data)

            return credentials.get(username) == password
        except Exception as e:
            print("Erro na validação das credenciais:", e)
            return False

    @staticmethod
    def show_warning(message):
        messagebox.showwarning("Aviso", message)
