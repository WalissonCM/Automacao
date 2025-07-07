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

    # Store the handle of the original window (intimations list)
    original_window = driver.current_window_handle
    print(f"Original window handle: {original_window}")

    # --- Loop para cada TR e clique no botão 'Detalhes do Processo' ---
    # Find all table rows that contain process details.
    process_rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'tr-class')]")))

    for i in range(len(process_rows)):
        # Re-find the rows inside the loop to avoid StaleElementReferenceException
        current_process_rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'tr-class')]")))

        row = current_process_rows[i]

        first_new_tab_handle = None
        second_new_tab_handle = None

        try:
            # 1. Click 'Detalhes do Processo' button (opens First New Tab)
            detales_button = WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.//img[@mattooltip='Detalhes do Processo']]")))
            detales_button.click()

            # Wait for the first new tab to appear (now 2 windows: original + first new)
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            all_window_handles = driver.window_handles
            first_new_tab_handle = None
            for handle in all_window_handles:
                if handle != original_window:
                    first_new_tab_handle = handle
                    break

            if not first_new_tab_handle:
                print("Error: First new tab handle not found. Skipping to next row.")
                continue # Skip this iteration if the tab didn't open

            driver.switch_to.window(first_new_tab_handle)
            print(f"Switched to first new tab (Detalhes do Processo) with handle: {first_new_tab_handle}")
            time.sleep(3) 

            # --- Actions on the First New Tab (Detalhes do Processo page) ---
            # These elements are on the first new tab, so use driver
            preparar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Abre a tarefa do processo']")))
            print("Clicking 'Abre a tarefa do processo' button (opens Second New Tab)...")
            preparar_button.click()

            # Wait for the second new tab to appear (now 3 windows: original + first new + second new)
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
            all_window_handles_after_second_click = driver.window_handles
            second_new_tab_handle = None
            for handle in all_window_handles_after_second_click:
                if handle != original_window and handle != first_new_tab_handle:
                    second_new_tab_handle = handle
                    break

            if not second_new_tab_handle:
                print("Error: Second new tab handle not found. Closing first tab and skipping to next row.")
                driver.close() # Close the first new tab before continuing
                driver.switch_to.window(original_window)
                continue # Skip this iteration if the tab didn't open

            driver.switch_to.window(second_new_tab_handle)
            print(f"Switched to second new tab with handle: {second_new_tab_handle}")
            time.sleep(5) 

            # --- Actions on the Second New Tab (Task/Expedient page) ---
            # These elements are on the second new tab, so use driver
            tipo_expediente_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(.,'Tipo de Expediente')]")))
            tipo_expediente_button.click()

            # Wait for options to load for Tipo de Expediente
            tipo_expediente_selecao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-option[contains(.,' Intimação ')]")))
            tipo_expediente_selecao.click()

            prazo_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Prazo em dias úteis']")))
            prazo_button.clear()
            prazo_button.send_keys("15")

            confeccionar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Confeccionar ato agrupado']")))
            confeccionar_button.click()
            
            time.sleep(5) 

            # Assuming 'Descrição' input is on the same (second) tab
            descricao_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Descrição']")))
            descricao_input.clear()
            descricao_input.send_keys("Decisão Monocrática")
            

            # This 'documentos_button' looks like it might be a tab within the current (second) page
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

                    print("Found target <li> element with 'Decisão', '(Decisão)', and 'fa-gavel' icon.")
                    
                    link_to_click = WebDriverWait(li_element, 5).until(
                        EC.element_to_be_clickable((By.XPATH, ".//a[contains(@class, 'tl-documento') and .//span[text()='Decisão'] and .//span[text()='(Decisão) ']]"))
                    )
                    link_text = link_to_click.text
                    print(f"Clicking on the link: '{link_text}'")
                    link_to_click.click()
                    found_target_li = True
                    time.sleep(5) 
                    break 

                except:                  
                    continue

            if not found_target_li:
                print("No matching <li> element with 'Decisão', '(Decisão)', and 'fa-gavel' icon was found.")

            importar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Importar conteúdo']")))
            importar_button.click()

            time.sleep(5)

            excluir_figure = driver.find_element(By.XPATH, "//pje-editor/div/div[2]/div/div[2]/div/div[1]/figure/div")
            time.sleep(1)
            excluir_figure.click()
            time.sleep(1)
            ActionChains(driver).send_keys(Keys.DELETE).perform()
            print("Deleted content from the table.")

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

            salvar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//pje-duas-colunas/div/div[1]/form/div/div[1]/button")))
            salvar_button.click()

            time.sleep(1)

            finalizar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Finalizar minuta']")))
            finalizar_button.click()
            
            time.sleep(1)
       
            intimar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "btnIntimarTodosPolos")))
            intimar_button.click()
            
            time.sleep(5)

            try:
                expedientes_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//pje-data-table/div/table/tbody")))
                print("Found 'Expedientes' table.")

                table_rows = expedientes_table.find_elements(By.TAG_NAME, "tr")
                print(f"Found {len(table_rows)} rows in 'Expedientes' table.")

                for row_index, row_element in enumerate(table_rows):
                    try:
                        materia_button = WebDriverWait(row_element, 5).until(EC.presence_of_element_located((By.XPATH, "//mat-select[@placeholder='Matéria Diário Eletrônico')]")))
                        materia_button.click()

                        materia_select = WebDriverWait(row_element, 5).until(EC.presence_of_element_located((By.XPATH, "//mat-option[@name='Decisão Monocrática']")))
                        materia_select.click()

                        time.sleep(10) # Wait for the selection to be processed
                        
                    except Exception as row_e:
                        print(f"Matéria Diário Eletrônico not found or error in row {row_index + 1}: {row_e}")
                        continue # Continue to the next row even if one fails

            except Exception as table_e:
                print(f"Error finding or processing 'Expedientes' table: {table_e}")
            # --- End: New logic ---


            # --- After actions on Second New Tab ---
            driver.close() # Close the second new tab
            print("Second tab closed.")

            # Switch back to the first new tab (Detalhes do Processo)
            driver.switch_to.window(first_new_tab_handle)
            print("Switched back to first new tab.")
            time.sleep(2) 



            # --- After actions on First New Tab ---
            driver.close() # Close the first new tab
            print("First tab closed.")

            # Switch back to the original window (Intimações list)
            driver.switch_to.window(original_window)
            print("Switched back to original window for next iteration.")
            time.sleep(5) # Wait for the list to be fully visible and interactive

        except Exception as e:
            print(f"Error processing row {i+1} or new tabs: {e}")
            # Robust error handling for multiple tabs:
            # First, check if we are on the second new tab and close it
            if second_new_tab_handle and driver.current_window_handle == second_new_tab_handle:
                driver.close()
                print("Closed second tab due to error.")
                # Then try to switch to the first new tab and close it
                try:
                    driver.switch_to.window(first_new_tab_handle)
                    driver.close()
                    print("Closed first tab due to error.")
                except:
                    pass # First tab might already be closed or handle invalid

            # Finally, ensure we are back on the original window
            driver.switch_to.window(original_window)
            print("Switched back to original window after error for next iteration.")
            time.sleep(5) # Give it time to load after potential error and switch
            continue # Continue to the next row

except Exception as e:
    print(f"An error occurred during the automation process: {e}")

finally:
    if driver:
        driver.quit()
        print("Browser closed.")