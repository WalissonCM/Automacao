import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Login com a Variável de Ambiente
username = os.environ.get('MEU_USUARIO') 
password = os.environ.get('MINHA_SENHA')

try:
    # --- Iniciar o Navegador ---
    driver = webdriver.Chrome() # options=chrome_options
    driver.maximize_window()
    driver.get("https://pje.tst.jus.br/tst/login.seam")
    driver.implicitly_wait(10) 

    # --- Login ---
    login_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSsoPdpj")))
    login_button1.click()

    driver.implicitly_wait(10) 

    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_input.send_keys(password)

    login_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "kc-form-buttons")))
    login_button2.click()
    
    print("Login realizado com sucesso!")

    time.sleep(20)
    
    #element = driver.find_element(By.ID, "meuElemento") # Encontre o elemento
    #driver.execute_script("arguments[0].scrollIntoView();", element) 

except Exception as e:
    print(f"Erro ao realizar login: {e}")

finally:
    if driver:
        driver.quit()
