import os
import time
import shutil  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


google_drive = r"G:\Meu Drive\Automação" 

login_url = "https://secretaria-eletronica.tst.jus.br/sala-sessao"

# Login com a Variável de Ambiente
username = os.environ.get('MEU_USUARIO') 
password = os.environ.get('MINHA_SENHA')

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
driver.get(login_url)

try:
    # --- Login ---
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user")))
    username_input.send_keys(username)
    
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_input.send_keys(password)
    
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logar")))
    login_button.click()

    time.sleep(30)

    # --- Download ---
    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='no-print']/div/div[1]/div/div[1]/div/div[2]/div[7]")))
    download_button.click()

    time.sleep(10)

    # --- Mover o arquivo para o Google Drive ---
    caminho_do_arquivo_baixado = os.path.join(os.path.expanduser("~"), "Downloads")
    caminho_de_destino_no_drive = google_drive

    for nome_arquivo in os.listdir(caminho_do_arquivo_baixado):
        if nome_arquivo.endswith(".csv"):
            caminho_completo_origem = os.path.join(caminho_do_arquivo_baixado, nome_arquivo)
            caminho_completo_destino = os.path.join(caminho_de_destino_no_drive, nome_arquivo)
            shutil.move(caminho_completo_origem, caminho_completo_destino)

except Exception as e:
    print(f"Ocorreu um erro no processo: {e}")


driver.quit()
 