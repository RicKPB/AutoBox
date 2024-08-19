import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils.systemAutoCode import show_input_dialog, register_data_in_system, process_data
from utils.dataEncryption import load_key, load_credentials


key = load_key()
filename = 'Y:/AUTOBOX/CriptografiaLinkQuantico/linkSistema.enc'
credentials = load_credentials(filename, key)

link = credentials['link']

# MAIN (ATUALIZAR METODO DO JSON PARA SALVAR DENTRO DO SERVER [VER COM O GABRIEL AONDE POSSO SALVAR ESSES ARQUIVOS])
if __name__ == '__main__':
    file_path, company, department, shelf_code, name_json = show_input_dialog()
    spreadsheet_reader = pd.read_excel(file_path)
    print(spreadsheet_reader)

    service = Service(ChromeDriverManager().install())
    browserWeb = webdriver.Chrome(service=service)
    clickMouse = ActionChains(browserWeb)
    browserWeb.implicitly_wait(4)
    browserWeb.get(link)
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
