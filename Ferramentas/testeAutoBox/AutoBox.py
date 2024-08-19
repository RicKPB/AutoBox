import json
import platform
import tkinter as tk
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from model.inputBox import InputBox

# Verificar arquitetura do Python
print(f"Arquitetura do Python: {platform.architecture()}")

# Verificar versão do ChromeDriver
try:
    driver_service = Service(ChromeDriverManager().install())
    print(f"Versão do ChromeDriver instalada em: {driver_service.path}")
except Exception as e:
    print(f"Erro ao verificar a versão do ChromeDriver: {e}")


# FUNÇÃO PARA TELA DE CADASTRO APARECER E PASSAR OS VALORES POR ELA (INPUTBOX)
def show_input_dialog():
    root = tk.Tk()
    input_box = InputBox(root)
    root.mainloop()
    return (input_box.file_path_selected,
            input_box.value_company,
            input_box.value_content,
            input_box.value_shelf,
            input_box.value_name_json)


# Função para processar e armazenar os dados das caixas
def process_data(spreadsheet_reader):
    boxes = []
    current_box = None
    current_description = None
    current_observation = None
    documents_box = []

    for spreadsheet_line in spreadsheet_reader.index:
        serial = spreadsheet_reader.loc[spreadsheet_line, 'N DE CAIXA']
        description = spreadsheet_reader.loc[spreadsheet_line, 'DESCRICAO']
        observation = spreadsheet_reader.loc[spreadsheet_line, 'OBSERVACAO']
        content = spreadsheet_reader.loc[spreadsheet_line, 'DOCUMENTOS']

        if pd.isna(serial) and pd.isna(description) and pd.isna(observation) and pd.isna(content):
            if current_box is not None:
                current_box_data = {
                    'box': current_box,
                    'description': current_description,
                    'observation': current_observation if current_observation is not None else "",
                    'documents': list(dict.fromkeys(documents_box))  # Remove duplicates, preserves order
                }
                boxes.append(current_box_data)
            current_box = None
            current_description = None
            current_observation = None
            documents_box = []
            continue

        if pd.isna(serial):
            if current_box is not None and not pd.isna(content):
                documents_box.append(content)
        else:
            if current_box is not None:
                current_box_data = {
                    'box': current_box,
                    'description': current_description,
                    'observation': current_observation if current_observation is not None else "",
                    'documents': list(dict.fromkeys(documents_box))  # Remove duplicates, preserves order
                }
                boxes.append(current_box_data)
            current_box = f'caixa{int(float(serial))}'
            current_description = description if not pd.isna(description) else None
            current_observation = observation if not pd.isna(observation) else None
            documents_box = []
            if not pd.isna(content):
                documents_box.append(content)

    if current_box is not None:
        current_box_data = {
            'box': current_box,
            'description': current_description,
            'observation': current_observation if current_observation is not None else "",
            'documents': list(dict.fromkeys(documents_box))  # Remove duplicates, preserves order
        }
        boxes.append(current_box_data)

    return boxes


# FUNÇÃO PRINCIPAL (SISTEMA DA RPA PARA CADASTRAR DENTRO DO QDOC)
# MEXER COM TRY E EXCEPT DENTRO DAS PARTES DE DETEÇÃO DE ESCRITA NAS CAIXAS DE TEXTO
def register_data_in_system(box, browserWeb, company, department, code_shelf):
    wait = WebDriverWait(browserWeb, 15)
    actions = ActionChains(browserWeb)

    button_register_box = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/header/div[2]/div/nav/div/ul/li[4]/a")))
    button_register_box.click()

    button_register_box_page = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="topnav-menu-content"]/ul/li[4]/div/a[1]')))
    button_register_box_page.click()

    client = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-owns='bs-select-1']")))
    client.send_keys(company)
    client.send_keys(Keys.ENTER)

    content = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='id_conteudo']")))
    content.send_keys(department)
    content.send_keys(Keys.ENTER)

    shelf = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-owns='bs-select-2']")))
    shelf.send_keys(code_shelf)
    shelf.send_keys(Keys.ENTER)

    field_description = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='descricao']")))
    field_description.send_keys(str(box['description']))

    observation_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@name="observacoes"]')))
    if box['observation']:
        observation_field.send_keys(box['observation'])
    else:
        observation_field.clear()

    button_register = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary btn-block"]')))
    actions.double_click(button_register).perform()

    initial_URL = browserWeb.current_url

    print(initial_URL)

    try:
        WebDriverWait(browserWeb, 10).until(EC.url_changes(initial_URL))
        print("A URL mudou após o registro.")

    except:
        # Se a URL não mudou, tenta registrar novamente
        content = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='id_conteudo']")))
        content.send_keys(department)
        content.send_keys(Keys.ENTER)

    button_registration_documents = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-primary"]')))
    button_registration_documents.click()

    for box_document in box['documents']:
        field_content_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@name="dados_excel"]')))
        field_content_box.send_keys(str(box_document) + '\n')

    button_confirm_registration_documents = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-primary btn-block"]')))
    button_confirm_registration_documents.click()
    button_confirm_registration_documents.click()


def load_key():
    return open(
        "../test_criptografia/linkCriptografia/keySecretLinkSystem.key",
        "rb"
    ).read()


# MAIN (ATUALIZAR METODO DO JSON PARA SALVAR DENTRO DO SERVER [VER COM O GABRIEL AONDE POSSO SALVAR ESSES ARQUIVOS])
if __name__ == '__main__':
    file_path, company, department, shelf_code, name_json = show_input_dialog()
    spreadsheet_reader = pd.read_excel(file_path)
    print(spreadsheet_reader)

    key = load_key()

    service = Service(ChromeDriverManager().install())
    browserWeb = webdriver.Chrome(service=service)
    clickMouse = ActionChains(browserWeb)
    browserWeb.implicitly_wait(4)
    browserWeb.get('https://sistema.qdoc.com.br/')
    browserWeb.maximize_window()

    if browserWeb.find_element(By.ID, 'login'):
        usernameInput = browserWeb.find_element(By.XPATH, '//*[@id="login"]')
        passwordInput = browserWeb.find_element(By.XPATH, '//*[@id="senha"]')
        buttonLogin = browserWeb.find_element(By.XPATH, '//*[@id="BtnLogin"]')
        usernameInput.send_keys('henrique.bernardo')
        passwordInput.send_keys('we23rs45@')
        buttonLogin.click()

    boxes = process_data(spreadsheet_reader)

    with open(f'{name_json}.json', 'w', encoding='utf-8') as f:
        json.dump(boxes, f, ensure_ascii=False, indent=4)

    print(f'Dados armazenados em {name_json}.json')

    for quantity_boxes in range(1):
        for box in boxes:
            register_data_in_system(box, browserWeb, company, department, shelf_code)

    browserWeb.quit()
