import os
import time
import shutil  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login_url = "https://secretaria-eletronica.tst.jus.br/sala-sessao"

# Login com a Variável de Ambiente
username = os.environ.get('MEU_USUARIO') 
password = os.environ.get('MINHA_SENHA')

# Configuracao do Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
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
    
    # --- Selecione o Orgao Julgador ---
    orgao_button= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='divMenuAppBar']/header/div/div[3]/div[1]")))
    orgao_button.click()

    orgao_tp= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/nav/div[2]")))
    orgao_tp.click()  

    time.sleep(15)

    # --- Download ---
    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='no-print']/div/div[1]/div/div[1]/div/div[2]/div[7]")))
    download_button.click()

    time.sleep(5)
    
except Exception as e:
   print(f"Ocorreu um erro: {e}")

driver.quit()

# Caminhos para o Drive
caminho_base = r"C:\Users\wally\Desktop\Votos\PLENO"
pasta_atual = os.path.join(caminho_base, "Atual")
pasta_antigos = os.path.join(caminho_base, "Antigos")
pasta_tp = caminho_base
caminho_downloads  = os.path.join(os.path.expanduser("~"), "Downloads")

# Verifica os arquivos baixados e organiza
for nome_arquivo_novo in os.listdir(caminho_downloads):
    if nome_arquivo_novo.startswith("votos_PLENO") and nome_arquivo_novo.endswith(".csv"):
        caminho_novo = os.path.join(caminho_downloads, nome_arquivo_novo)

         # Verifica se o arquivo já existe na pasta atual
        nome_arquivo_antigo = None
        for f in os.listdir(pasta_atual):
            if f.startswith("votos_PLENO") and f.endswith(".csv"):
                nome_arquivo_antigo = f
                break
       
        if nome_arquivo_antigo:
            caminho_antigo = os.path.join(pasta_atual, nome_arquivo_antigo)
            
            # Se o arquivo já existe na pasta atual, compara o conteúdo
            with open(caminho_novo, 'rb') as f_novo, open(caminho_antigo, 'rb') as f_antigo:
                conteudo_igual = f_novo.read() == f_antigo.read()
            
            # Se o arquivo já existe na pasta atual e é diferente, move e copia
            if not conteudo_igual:
                shutil.move(caminho_antigo, os.path.join(pasta_antigos, nome_arquivo_antigo))
                shutil.move(caminho_novo, os.path.join(pasta_atual, nome_arquivo_novo))
                shutil.copy2(os.path.join(pasta_atual, nome_arquivo_novo), os.path.join(pasta_tp, "VOTOS_PLENO_SESSAO.csv"))
                
            # Se o arquivo é igual, remove o arquivo baixado
            else:
                os.remove(caminho_novo)
                
        # Se o arquivo não existe na pasta atual, move e copia
        else:
            shutil.move(caminho_novo, os.path.join(pasta_atual, nome_arquivo_novo))
            shutil.copy2(os.path.join(pasta_atual, nome_arquivo_novo), os.path.join(pasta_tp, "VOTOS_PLENO_SESSAO.csv"))


    





