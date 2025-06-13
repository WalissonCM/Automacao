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

    time.sleep(20)
    
    # --- Selecione o Orgao Julgador ---
    orgao_button= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='divMenuAppBar']/header/div/div[3]/div[1]")))
    orgao_button.click()

    orgao_oe= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/nav/div[1]")))
    orgao_oe.click() 

    time.sleep(15)
                                                                   
    # --- Download ---
    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='no-print']/div/div[1]/div/div[1]/div/div[2]/div[7]")))
    download_button.click()

    time.sleep(5)
    
    # Caminhos para o Drive
    caminho_base = r"C:\Users\wally\Desktop\Votos\OE"
    pasta_atual = os.path.join(caminho_base, "Atual")
    pasta_antigos = os.path.join(caminho_base, "Antigos")
    pasta_oe = caminho_base

    caminho_do_arquivo_baixado = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Verifica os arquivos baixados e organiza
    for nome_arquivo in os.listdir(caminho_do_arquivo_baixado):
        if nome_arquivo.startswith("votos_OE"):
            caminho_completo_origem = os.path.join(caminho_do_arquivo_baixado, nome_arquivo)
            prefixo = "_".join(nome_arquivo.split("_")[:-1])
            arquivo_igual = None
            for arquivo_atual in os.listdir(pasta_atual):
                if arquivo_atual.startswith(prefixo):
                    arquivo_igual = arquivo_atual
                    break

            caminho_destino_atual = os.path.join(pasta_atual, nome_arquivo)
            caminho_destino_oe = os.path.join(pasta_oe, "VOTOS_OE_SESSAO" + os.path.splitext(nome_arquivo)[1])
            
            # Se já existe um arquivo igual na pasta atual
            if arquivo_igual:
                caminho_arquivo_igual = os.path.join(pasta_atual, arquivo_igual)
                # Compara o conteúdo dos arquivos
                with open(caminho_arquivo_igual, 'rb') as f1, open(caminho_completo_origem, 'rb') as f2:
                    conteudo_igual = f1.read() == f2.read()

                if not conteudo_igual:
                    caminho_destino_antigos = os.path.join(pasta_antigos, arquivo_igual)
                    shutil.move(caminho_arquivo_igual, caminho_destino_antigos)
                    shutil.move(caminho_completo_origem, caminho_destino_atual)
                    shutil.copy2(caminho_destino_atual, caminho_destino_oe)
                else:
                    os.remove(caminho_completo_origem)
                    print(f"Arquivo {nome_arquivo} já existe na pasta atual e é idêntico ao existente.")
   
           
except Exception as e:
    print(f"Ocorreu um erro no processo: {e}")


driver.quit()
