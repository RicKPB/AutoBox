import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


class InputBox:
    def __init__(self, root):
        self.root = root
        self.root.title("Inserir Valor")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')

        # CRIAÇÃO DO FRAME DA LOGO
        self.logo_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.logo_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # CARREGAMENTO DA LOGO DA AUTOBOX
        logo_path_AutoBox = os.path.join(os.path.dirname(__file__), 'Y:/AUTOBOX/Materiais', 'Logo-AutoBoxRpa.png')
        self.logo_image_AutoBox = Image.open(logo_path_AutoBox).convert("RGBA")
        self.logo_image_AutoBox = self.logo_image_AutoBox.resize((105, 105), Image.LANCZOS)
        logo_data = self.logo_image_AutoBox.getdata()
        new_logo_data_AutoBox = [(255, 255, 255, 0) if item[:3] == (255, 255, 255) else item for item in logo_data]
        self.logo_image_AutoBox.putdata(new_logo_data_AutoBox)
        self.logo_photo_AutoBox = ImageTk.PhotoImage(self.logo_image_AutoBox)

        # CARREGAMENTO DA LOGO DA QUANTICO DIGITAL
        logo_path_QuanticoDigital = os.path.join(os.path.dirname(__file__), 'Y:/AUTOBOX/Materiais', 'Logo_Quantico.png')
        self.logo_image_QuanticoDigital = Image.open(logo_path_QuanticoDigital).convert("RGBA")
        self.logo_image_QuanticoDigital = self.logo_image_QuanticoDigital.resize((200, 75), Image.LANCZOS)
        logo_data_new = self.logo_image_QuanticoDigital.getdata()
        new_logo_data_NewLogo = [(255, 255, 255, 0) if item[:3] == (255, 255, 255) else item for item in logo_data_new]
        self.logo_image_QuanticoDigital.putdata(new_logo_data_NewLogo)
        self.logo_photo_NewLogo = ImageTk.PhotoImage(self.logo_image_QuanticoDigital)

        # POSIÇÃO DAS LOGOS NA TELA DE CADASTRO
        self.logo_label_AutoBox = tk.Label(self.logo_frame, image=self.logo_photo_AutoBox, bg='#f0f0f0')
        self.logo_label_AutoBox.pack(side='left')

        self.logo_label_NewLogo = tk.Label(self.logo_frame, image=self.logo_photo_NewLogo, bg='#f0f0f0')
        self.logo_label_NewLogo.pack(side='right')

        # CONFIGURAÇÃO DAS IMAGENS NA FORMA RESPONSIVA
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.file_selected = False
        self.file_path_selected = None
        self.value_company = None
        self.value_content = None
        self.value_shelf = None
        self.value_name_json = None

        # OPÇÃO PARA SELEÇÃO DO ARQUIVO EXCEL (PLANILHA FEITA PELO COLABORADOR)
        self.frame_file = tk.Frame(root, bg='#f0f0f0')
        self.frame_file.grid(row=1, column=0, columnspan=2, pady=10)
        self.label_file = tk.Label(self.frame_file, text='Selecione o arquivo Excel (.xlsx):', bg='#f0f0f0')
        self.label_file.pack(side=tk.LEFT, padx=5)
        self.button_browse = tk.Button(self.frame_file, text="Selecionar Arquivo", command=self.browse_file)
        self.button_browse.pack(side=tk.LEFT, padx=5)

        # CAIXA DE TEXTO PARA A ESCRITA DA EMPRESA DA GUARDA
        self.frame_company = tk.Frame(root, bg='#f0f0f0')
        self.frame_company.grid(row=2, column=0, columnspan=2, pady=10)
        self.label_company = tk.Label(self.frame_company, text='Digite a Empresa: ', bg='#f0f0f0')
        self.label_company.pack(side=tk.LEFT, padx=5)
        self.entry_company = tk.Entry(self.frame_company, width=40)
        self.entry_company.pack(side=tk.RIGHT, padx=5)

        # CAIXA DE TEXTO PARA A ESCRITA DO CONTEUDO DA EMPRESA
        self.frame_content = tk.Frame(root, bg='#f0f0f0')
        self.frame_content.grid(row=3, column=0, columnspan=2, pady=10)
        self.label_content = tk.Label(self.frame_content, text='Digite o Conteúdo: ', bg='#f0f0f0')
        self.label_content.pack(side=tk.LEFT, padx=5)
        self.entry_content = tk.Entry(self.frame_content, width=40)
        self.entry_content.pack(side=tk.RIGHT, padx=5)

        # CAIXA DE TEXTO PARA A ESCRITA DA PRATELEIRA
        self.frame_shelf = tk.Frame(root, bg='#f0f0f0')
        self.frame_shelf.grid(row=4, column=0, columnspan=2, pady=10)
        self.label_shelf = tk.Label(self.frame_shelf, text='Digite a Prateleira: ', bg='#f0f0f0')
        self.label_shelf.pack(side=tk.LEFT, padx=5)
        self.entry_shelf = tk.Entry(self.frame_shelf, width=40)
        self.entry_shelf.pack(side=tk.RIGHT, padx=5)

        # CAIXA DE TEXTO PARA A ESCRITA DO ARQUIVO JSON (EMPRESA - CONTEUDO - PRATELEIRA)
        self.frame_name_json = tk.Frame(root, bg='#f0f0f0')
        self.frame_name_json.grid(row=5, column=0, columnspan=2, pady=10)
        self.label_name_json = tk.Label(self.frame_name_json, text='Digite nome planilha: ', bg='#f0f0f0')
        self.label_name_json.pack(side=tk.LEFT, padx=5)
        self.entry_name_json = tk.Entry(self.frame_name_json, width=40)
        self.entry_name_json.pack(side=tk.RIGHT, padx=5)

        # BOTÃO DE CONFIRMAÇÃO
        self.submit_button = tk.Button(root, text="CONFIRMAR", command=self.submit)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.entry_company.focus_set()
        self.root.bind("<Return>", lambda event: self.submit())

    # FUNÇÃO PARA CONFIRMAÇÃO DE ARQUIVO EXCEL
    def browse_file(self):
        self.file_path_selected = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if self.file_path_selected:
            self.file_selected = True

    # FUNÇÃO PARA A PASSAGEM DOS VALORES DO CADASTRO
    def submit(self):
        self.value_company = self.entry_company.get()
        self.value_content = self.entry_content.get()
        self.value_shelf = self.entry_shelf.get()
        self.value_name_json = self.entry_name_json.get()
        print("Arquivo selecionado:", self.file_path_selected)
        print("Empresa:", self.value_company)
        print("Conteúdo:", self.value_content)
        print("Prateleira:", self.value_shelf)
        print("Nome do JSON:", self.value_name_json)
        self.root.destroy()

    # CONTINUAR A MEXER (FUNÇÃO PARA MENSAGEM DE ALERTA CASO ESQUEÇA DE COLOCAR ALGUMA INFORMAÇÃO)
    @staticmethod
    def show_warning(message):
        messagebox.showwarning("Aviso", message)
