import os
import time
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Login com a Variável de Ambiente
username = os.environ.get('MEU_USUARIO')
password = os.environ.get('MINHA_SENHA')

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")

driver = None 

try:
    # --- Iniciar o Navegador ---
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://pje.tst.jus.br/tst/login.seam")

    # --- Login ---
    login_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSsoPdpj")))
    login_button1.click()
    
    time.sleep(1)

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

    time.sleep(3)

    painel_global_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Painel Global")))
    painel_global_button.click()

    intimacao_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Intimações')]")))
    intimacao_button.click()

    chips = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Chips')]")))
    chips.click()

    time.sleep(3)

    chips_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Nova Decisão')]")))
    chips_selecao.click()

    filter_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/button/span[1]/i")))
    filter_button1.click()

    time.sleep(3)

    responsavel = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Usuário Responsável')]")))
    responsavel.click()

    time.sleep(3)

    responsavel_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Sem responsável')]")))
    responsavel_selecao.click()

    filter_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/button/span[1]/i")))
    filter_button2.click()

    time.sleep(3)

    desde = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-data-table/div[1]/table/thead/tr/th[7]/div/div")))
    desde.click()

    time.sleep(5)

    linhas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-paginador/div/mat-form-field[2]/div/div/div")))
    linhas.click()

    time.sleep(1)

    linhas_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(.,'100')]")))
    linhas_selecao.click()

    time.sleep(5)
        
    # Armazenar o Handle da Janela Original
    original_window = driver.current_window_handle
    print(f"Original window handle: {original_window}")

    # Processar as Linhas da Tabela de Intimações
    process_rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'tr-class')]")))

    for i in range(len(process_rows)):
        current_process_rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'tr-class')]")))

        row = current_process_rows[i]

        first_new_tab_handle = None
        second_new_tab_handle = None

        try:
            print("Começando a processar a linha do processo...")
            print(f"Processo a linha {i+1} de {len(current_process_rows)}")

            # Click para abrir a linha do processo
            detales_button = WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, ".//button[.//img[@mattooltip='Detalhes do Processo']]")))
            detales_button.click()

            # Esperar até que a nova aba seja aberta
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            all_window_handles = driver.window_handles
            first_new_tab_handle = None
            for handle in all_window_handles:
                if handle != original_window:
                    first_new_tab_handle = handle
                    break

            if not first_new_tab_handle:
                print("Error: O primeiro identificador da nova aba não foi encontrado. Indo para a próxima linha.")
                continue 
            
            # Trocar para a primeira nova aba (Detalhes do Processo)
            driver.switch_to.window(first_new_tab_handle)
            print(f"Mudou para a primeira nova aba (Detalhes do Processo) com handle: {first_new_tab_handle}")
            
            time.sleep(3) 

            # --- Ações na Primeira Nova Aba (Detalhes do Processo) ---
            preparar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Abre a tarefa do processo']")))
            print("Clicando no botão 'Abre a tarefa do processo' (abre a segunda nova aba)...")
            preparar_button.click()

            # Esperar até que a segunda aba seja aberta
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
            all_window_handles_after_second_click = driver.window_handles
            second_new_tab_handle = None
            for handle in all_window_handles_after_second_click:
                if handle != original_window and handle != first_new_tab_handle:
                    second_new_tab_handle = handle
                    break

            if not second_new_tab_handle:
                print("Error: Segundo identificador de nova aba não encontrado. Fechando a primeira aba e pulando para a próxima linha.")
                driver.close() 
                driver.switch_to.window(original_window)
                continue 
            
            # Trocar para a segunda nova aba 
            driver.switch_to.window(second_new_tab_handle)
            print(f"Mudou para a segunda nova aba com handle: {second_new_tab_handle}")
            
            time.sleep(5) 

            # --- Ações na Segunda Nova Aba --- 
            print("Realizando ações do ato agrupado...")

            tipo_expediente_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Tipo de Expediente')]")))
            tipo_expediente_button.click()

            tipo_expediente_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(.,' Intimação ')]")))
            tipo_expediente_selecao.click()

            prazo_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Prazo em dias úteis']")))
            prazo_button.clear()
            prazo_button.send_keys("15")

            confeccionar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Confeccionar ato agrupado']")))
            confeccionar_button.click()
            
            time.sleep(5) 

            descricao_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Descrição']")))
            descricao_input.clear()
            descricao_input.send_keys("Decisão Monocrática")
            
            documentos_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-tab-header/div[2]/div/div/div[4]/div")))
            documentos_button.click()
            
            timeline_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='pje-timeline']")))

            list_items = timeline_list.find_elements(By.XPATH, "./li[contains(@class, 'tl-item-container')]")

            found_target_li = False
            for li_element in list_items:
                try:
                    span_decisao = li_element.find_element(By.XPATH, ".//span[text()='Decisão']")
                    span_decisao_paren = li_element.find_element(By.XPATH, ".//span[text()='(Decisão) ']")                  
                    gavel_icon = li_element.find_element(By.XPATH, ".//i[contains(@class, 'fa-gavel')]")

                    print("Elemento alvo <li> elemento encontrado 'Decisão', '(Decisão)', e 'fa-gavel' icon.")
                    
                    link_to_click = WebDriverWait(li_element, 5).until(
                        EC.element_to_be_clickable((By.XPATH, ".//a[contains(@class, 'tl-documento') and .//span[text()='Decisão'] and .//span[text()='(Decisão) ']]"))
                    )
                    link_text = link_to_click.text
                    print(f"Clicou no link: '{link_text}'")
                    link_to_click.click()
                    found_target_li = True
                    time.sleep(5) 
                    break 

                except:                  
                    continue

            if not found_target_li:
                print("Nenhum elemento <li> correspondente com 'Decisão', '(Decisão)', e 'fa-gavel' icon foi encontrado.")

            importar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Importar conteúdo']")))
            importar_button.click()

            time.sleep(3)

            excluir_figure = driver.find_element(By.XPATH, "//pje-editor/div/div[2]/div/div[2]/div/div[1]/figure/div")
            time.sleep(1)
            excluir_figure.click()
            time.sleep(1)
            ActionChains(driver).send_keys(Keys.DELETE).perform()

            time.sleep(1)
            
            pesquisar_substituir_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-editor/div/div[1]/div/div/div/div[1]/button")))
            pesquisar_substituir_button.click()

            time.sleep(1)

            pesquisar_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//pje-editor/div/div[1]/div/div/div/div[1]/div/form/fieldset[1]/div/div[1]/input")))
            pesquisar_input.send_keys("BrasÃ­lia")

            time.sleep(1)
            
            pesquisar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-editor/div/div[1]/div/div/div/div[1]/div/form/fieldset[1]/button[1]")))
            pesquisar_button.click()

            time.sleep(1)

            substituir_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//pje-editor/div/div[1]/div/div/div/div[1]/div/form/fieldset[2]/div[1]/div[1]/input")))
            substituir_input.send_keys("Brasília")

            time.sleep(1)
            
            substituir_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-editor/div/div[1]/div/div/div/div[1]/div/form/fieldset[2]/button[1]")))
            substituir_button.click()

            time.sleep(1)

            salvar_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Salvar']")))
            salvar_button1.click()

            time.sleep(1)

            finalizar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Finalizar minuta']")))
            finalizar_button.click()

            print("Finalizando ato agrupado...")
            
            time.sleep(1)
       
            intimar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "btnIntimarTodosPolos")))
            intimar_button.click()
            
            time.sleep(5)

            try:
                expedientes_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//pje-data-table/div/table/tbody")))
                print("Encontrada a tabela 'Expedientes'.")

                table_rows = expedientes_table.find_elements(By.TAG_NAME, "tr")
                print(f"Encontradas {len(table_rows)} linhas na tabela 'Expedientes'.")

                for row_index, row_element in enumerate(table_rows):
                    try:
                        materia_button = row_element.find_element(By.XPATH, ".//mat-select[@placeholder='Matéria Diário Eletrônico']")
                        materia_button.click()

                        materia_select = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//mat-option[@name='Decisão Monocrática']")))
                        materia_select.click()

                        time.sleep(1)

                    except Exception as row_e:
                        print(f"Matéria Diário Eletrônico não encontrada ou erro na linha {row_index + 1}: {row_e}")
                        continue 

            except Exception as table_e:
                print(f"Erro ao localizar ou processar a tabela 'Expedientes': {table_e}")

            salvar_button2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Salva os expedientes']")))
            salvar_button2.click()

            print("Salvando expedientes...")

            time.sleep(5)

            # --- Feche a segunda nova aba ---
            driver.close()
            print("Segunda aba fechada.")

            # Voltar para a primeira nova aba (Detalhes do Processo)
            driver.switch_to.window(first_new_tab_handle)
            print("Voltou para a primeira nova aba.")

            time.sleep(5)

            # --- Ações na Primeira Nova Aba (Detalhes do Processo) ---

            print("Removendo chip 'Nova Decisão' e incluindo chip 'Analisar'...")

            remover_chip = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Remover Chip Nova Decisão']")))
            remover_chip.click()
            
            time.sleep(1)

            remover_chip_sim = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-dialog-container/ng-component/div/div[3]/button[1]")))
            remover_chip_sim.click()

            time.sleep(1)

            incluir_chip = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Incluir Chip Amarelo']")))
            incluir_chip.click()

            time.sleep(1)

            nome_chip_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@data-placeholder='Nome do chip']")))
            nome_chip_input.send_keys("Analisar")

            time.sleep(1)

            select_analisar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-data-table/div/table/tbody/tr[1]/td[1]/mat-checkbox")))
            select_analisar.click()

            time.sleep(1)

            incluir_chip_salvar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-inclui-etiquetas-dialogo/div/div/button[1]")))
            incluir_chip_salvar.click()
            
            time.sleep(5)

            # --- Feche a primeira nova aba (Detalhes do Processo) ---
            driver.close() 
            print("Primeira aba fechada.")

            # Voltar para a janela original
            driver.switch_to.window(original_window)
            print("Retornar à janela original para a próxima iteração.")       

        except Exception as e:
            print(f"Erro ao processar a linha {i+1} ou novas guias: {e}")
            # Fechar as abas abertas em caso de erro
            if second_new_tab_handle and driver.current_window_handle == second_new_tab_handle:
                driver.close()
                print("Segunda aba fechada devido a um erro.")
                
                try:
                    driver.switch_to.window(first_new_tab_handle)
                    driver.close()
                    print("Primeira aba fechada devido a um erro.")
                except:
                    pass 
            # Retornar à janela original
            driver.switch_to.window(original_window)
            print("Retornar à janela original após o erro na próxima iteração.")

            time.sleep(5) 
            continue 

except Exception as e:
    print(f"Ocorreu um erro durante o processo de automação: {e}")

finally:
    if driver:
        driver.quit()
        print("Navegador fechado.")