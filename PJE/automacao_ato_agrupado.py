import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Login com a Variável de Ambiente
username = os.environ.get('MEU_USUARIO') 
password = os.environ.get('MINHA_SENHA')

try:
    # --- Iniciar o Navegador ---
    driver = webdriver.Chrome()
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

    print("Órgão Julgador selecionado com sucesso!")

    time.sleep(5)

    painel_global_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Painel Global")))
    painel_global_button.click() 

    intimacao_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Intimações')]")))
    intimacao_button.click()

    linhas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-paginador/div/mat-form-field[2]/div/div/div")))
    linhas.click()

    time.sleep(1)

    linhas_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(.,'100')]")))
    linhas_selecao.click()

    time.sleep(5)

    chips = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Chips')]")))
    chips.click()

    time.sleep(5)

    chips_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Nova Decisão')]")))
    chips_selecao.click()

    filter_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/button/span[1]/i")))
    filter_button1.click()

    time.sleep(5)

    responsavel = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Usuário Responsável')]")))
    responsavel.click()

    time.sleep(5)

    responsavel_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Sem responsável')]")))
    responsavel_selecao.click()

    filter_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/button/span[1]/i")))
    filter_button2.click()

    time.sleep(5)

    desde = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-data-table/div[1]/table/thead/tr/th[7]/div/div")))
    desde.click()

    print("Filtros aplicados com sucesso!")

    time.sleep(10)

    original_window = driver.current_window_handle

    process_rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'tr-class')]")))

    for i in range(len(process_rows)):
            
        current_process_rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'tr-class')]")))
        row = current_process_rows[i]

        try:
                
            detales_button = WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[.//img[@mattooltip='Detalhes do Processo']]")))
            detales_button.click()

            time.sleep(10)

            # Pegue o identificador da janela original
            all_window_handles = driver.window_handles
            new_window_handle = None

            # Procure o novo identificador de janela
            for handle in all_window_handles:
                if handle != original_window:
                    new_window_handle = handle
                    break

            if new_window_handle:
                # Mude para a nova janela
                driver.switch_to.window(new_window_handle)
                
                driver.close()
                
                # Volte para a janela original
                driver.switch_to.window(original_window)
                
            else:
                print("Error: New window handle not found.")
        
                continue

        except Exception as e:
            print(f"Error processing row {i+1} or new tab: {e}")
            if driver.current_window_handle != original_window and len(driver.window_handles) > 1:
                driver.close() 
                driver.switch_to.window(original_window)
                print("Switched back to original window after error.")
            continue 


except Exception as e:
    print(f"Erro ao realizar login: {e}")

finally:
    if driver:
        driver.quit()