import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login_url = "https://secretaria-eletronica.tst.jus.br/sala-sessao"

# login com a Variavel de Ambiente
username = os.environ.get('MEU_USUARIO') 
password = os.environ.get('MINHA_SENHA')

# Chrome
driver = webdriver.Chrome()
driver.get(login_url)

try:

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user"))
    )
    username_input.send_keys(username)

    
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.send_keys(password)

    
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logar"))
    )
    login_button.click()

    titulo = WebDriverWait(driver, 40).until(
          EC.visibility_of_element_located((By.XPATH, "//div[@id='PdivProcesso-21433-29.2016.5.04.0013']/div/div/div[1]/div[2]/div/button/div"))
    )
    
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='no-print']/div/div[1]/div/div[1]/div/div[2]/div[7]"))
    )
    download_button.click()

except Exception as e:
        print(f"An error occurred: {e}")


driver.quit
