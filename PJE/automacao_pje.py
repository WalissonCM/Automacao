import os
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
   
    # --- Login ---
    login_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSsoPdpj")))
    login_button1.click()

    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_input.send_keys(password)

    login_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "kc-form-buttons")))
    login_button2.click()
    
    print("Login realizado com sucesso!")

    time.sleep(5)

    orgao_julgador = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Trocar Órgão Julgador ou Perfil']")))
    orgao_julgador.click()

    time.sleep(1) 

    orgao_julgador_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Presidência - Admissibilidade - Secretário']")))
    orgao_julgador_selecao.click()

    time.sleep(5)

    painel_global_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Painel Global")))
    painel_global_button.click() 

    analise_processo_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Analisar processo')]")))
    analise_processo_button.click()

    time.sleep(5)

    chips = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Chips')]")))
    chips.click()

    time.sleep(5)

    chips_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Nova Decisão')]")))
    chips_selecao.click()

    filter_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/button/span[1]/i")))
    filter_button1.click()
    
    time.sleep(5)

    processo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Tarefa do processo')]")))
    processo.click()

    time.sleep(5)

    processo_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Análise de secretaria")))
    processo_selecao.click()

    filter_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/button/span[1]/i")))
    filter_button2.click()

    time.sleep(5)

    responsavel = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Usuário Responsável')]")))
    responsavel.click()

    time.sleep(5)

    responsavel_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Sem responsável')]")))
    responsavel_selecao.click()

    filter_button3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/button/span[1]/i")))
    filter_button3.click()

    time.sleep(5)

    scrollable_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "mat-sidenav-content.mat-drawer-content.mat-sidenav-content")))

    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_container)

    time.sleep(2)
    
    linhas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-paginador/div/mat-form-field[2]/div/div/div")))
    linhas.click()

    time.sleep(2)

    linhas_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(.,'100')]")))
    linhas_selecao.click()

    time.sleep(5)

    driver.execute_script("arguments[0].scrollTop = 0;", scrollable_container)

    time.sleep(2)
    
    desde = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-data-table/div[1]/table/thead/tr/th[7]/div/div")))
    desde.click()

    time.sleep(5)

    marcar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Marcar todos")))
    marcar.click()

    movimentar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Movimentar em Lote']")))
    movimentar.click()

    time.sleep(5)

    tarefas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-movimentacao-lote/div/div[1]/div/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span")))
    tarefas.click()

    tarefas_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(.,' Comunicações e expedientes ')]")))
    tarefas_selecao.click()

    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_container)
   
    time.sleep(2)

    print("Tarefas movimentadas com sucesso!")

except Exception as e:
    print(f"Erro ao realizar login: {e}")

finally:
    if driver:
        driver.quit()
