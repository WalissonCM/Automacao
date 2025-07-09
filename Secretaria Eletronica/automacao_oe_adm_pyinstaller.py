import os
import time
import shutil  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Login com a Variável de Ambiente
username = os.environ.get('MEU_USUARIO') 
password = os.environ.get('MINHA_SENHA')

if not username:
    raise EnvironmentError("A variável de ambiente 'MEU_USUARIO' não está definida.")
if not password:
    raise EnvironmentError("A variável de ambiente 'MINHA_SENHA' não está definida.")

# Configuracao dos Arquivos do Chrome
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_PATH = os.path.join(SCRIPT_DIR, "chromedriver-win64", "chromedriver.exe")
CHROME_BINARY_PATH = os.path.join(SCRIPT_DIR, "chrome-win64", "chrome.exe")

# Opções do Chrome
chrome_options = Options()
chrome_options.binary_location = CHROME_BINARY_PATH
chrome_options.add_argument("--headless")    
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
service = Service(executable_path=CHROME_DRIVER_PATH)

driver = None 

try:
    # --- Iniciar o Navegador ---
    driver = webdriver.Chrome(service=service, options=chrome_options)
   #driver.maximize_window()
    driver.get("https://secretaria-eletronica.tst.jus.br/sala-sessao")

    # --- Login ---
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user")))
    username_input.send_keys(username)
    
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
    password_input.send_keys(password)
    
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logar")))
    login_button.click()
    '''
    time.sleep(5)
    
    Localizacao_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "localizacao")))
    Localizacao_input.click()

    Localizacao_option_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[2]/div/div/div/ul/li[5]")))
    Localizacao_option_input.click()

    Localizacao_button_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "escolher-localizacao")))
    Localizacao_button_input.click()
    '''
    print("Login realizado com sucesso!")

    time.sleep(30)
    
    # --- Selecione o Orgao Julgador ---
    orgao_button= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='divMenuAppBar']/header/div/div[3]/div[1]")))
    orgao_button.click()

    orgao_oe= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/div/nav/div[1]")))
    orgao_oe.click() 

    print("Órgão julgador selecionado com sucesso!")

    time.sleep(20)
                                                                
    # --- Download ---
    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='no-print']/div/div[1]/div/div[1]/div/div[2]/div[7]")))
    download_button.click()

    print("Download concluído com sucesso!")

    time.sleep(5)

except Exception as e:
    print(f"Ocorreu um erro durante o teste")

finally:
    if driver:
        driver.quit()
        print("Navegador fechado.")

# Caminhos para o Drive
caminho_base = r"C:\Users\wally\Desktop\Votos\OE"
pasta_atual = os.path.join(caminho_base, "Atual")
pasta_antigos = os.path.join(caminho_base, "Antigos")
pasta_oe = caminho_base
caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# Cria as pastas se não existirem
os.makedirs(pasta_atual, exist_ok=True)
os.makedirs(pasta_antigos, exist_ok=True)

# Verifica os arquivos baixados e organiza
for nome_arquivo_novo in os.listdir(caminho_downloads):
    if nome_arquivo_novo.startswith("votos_OE") and nome_arquivo_novo.endswith(".csv"):
        caminho_novo = os.path.join(caminho_downloads, nome_arquivo_novo)

         # Verifica se o arquivo já existe na pasta atual
        nome_arquivo_antigo = None
        for f in os.listdir(pasta_atual):
            if f.startswith("votos_OE") and f.endswith(".csv"):
                nome_arquivo_antigo = f
                break
       
        if nome_arquivo_antigo:
            caminho_antigo = os.path.join(pasta_atual, nome_arquivo_antigo)
            
            # Se o arquivo já existe na pasta atual, compara o conteúdo
            with open(caminho_novo, 'rb') as f_novo, open(caminho_antigo, 'rb') as f_antigo:
                conteudo_igual = f_novo.read() == f_antigo.read()

                print(f"Comparando {nome_arquivo_novo} com {nome_arquivo_antigo}: {'Conteúdo igual' if conteudo_igual else 'Conteúdo diferente'}")
            
            # Se o arquivo já existe na pasta atual e é diferente, move e copia
            if not conteudo_igual:
                shutil.move(caminho_antigo, os.path.join(pasta_antigos, nome_arquivo_antigo))
                shutil.move(caminho_novo, os.path.join(pasta_atual, nome_arquivo_novo))
                shutil.copy2(os.path.join(pasta_atual, nome_arquivo_novo), os.path.join(pasta_oe, "VOTOS_OE_SESSAO.csv"))

                print(f"Arquivo {nome_arquivo_novo} movido para a pasta atual e copiado para a pasta OE.")
                
            # Se o arquivo é igual, remove o arquivo baixado
            else:
                os.remove(caminho_novo)
                print(f"Arquivo {nome_arquivo_novo} é igual ao existente, removido do download.")
                
        # Se o arquivo não existe na pasta atual, move e copia
        else:
            shutil.move(caminho_novo, os.path.join(pasta_atual, nome_arquivo_novo))
            shutil.copy2(os.path.join(pasta_atual, nome_arquivo_novo), os.path.join(pasta_oe, "VOTOS_OE_SESSAO.csv"))
            print(f"Arquivo {nome_arquivo_novo} movido para a pasta atual e copiado para a pasta OE.")

time.sleep(10)

print("Finalizado com sucesso!")


    





