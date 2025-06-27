import os
import re
from datetime import datetime

# Caminhos das pastas de sessão
caminho_oe = r"C:\Users\wally\Desktop\Sessoes local\OE"
caminho_tp = r"C:\Users\wally\Desktop\Sessoes local\PLENO"
caminho_sdc = r"C:\Users\wally\Desktop\Sessoes local\SDC"

# Caminhos das pastas de sessão do Drive
caminho_drive_oe = r"C:\Users\wally\Desktop\Sessoes drive\OE"
caminho_drive_tp = r"C:\Users\wally\Desktop\Sessoes drive\PLENO"
caminho_drive_sdc = r"C:\Users\wally\Desktop\Sessoes drive\SDC"

def encontrar_pasta_com_ano_atual(caminho_base):

    ano_atual = str(datetime.now().year)
    pastas_encontradas = []

    if not os.path.isdir(caminho_base):
        print(f"Caminho base não encontrado ou não é um diretório: {caminho_base}")
        return None

    for nome_item in os.listdir(caminho_base):
        caminho_completo_item = os.path.join(caminho_base, nome_item)

        if os.path.isdir(caminho_completo_item):
            # Prioriza a busca exata pelo ano como palavra completa
            if re.search(r'\b' + ano_atual + r'\b', nome_item):
                pastas_encontradas.append(caminho_completo_item)
            # Caso contrário, tenta encontrar 4 dígitos e verifica se são o ano atual
            elif re.search(r'\b(\d{4})\b', nome_item):
                match = re.search(r'\b(\d{4})\b', nome_item)
                if match and match.group(1) == ano_atual:
                    pastas_encontradas.append(caminho_completo_item)

    if pastas_encontradas:
        return pastas_encontradas
   
def encontrar_arquivos_pdf_com_underline(caminho_pasta_base):

    arquivos_encontrados = []
    if not caminho_pasta_base or not os.path.isdir(caminho_pasta_base):
        print(f"Caminho inválido ou não encontrado para buscar arquivos: {caminho_pasta_base}")
        return arquivos_encontrados # Retorna lista vazia se o caminho for None ou não for um diretório

    for root, dirs, files in os.walk(caminho_pasta_base):
        for file in files:
            if file.lower().endswith('.pdf') and file.startswith('_'):
                caminho_completo_arquivo = os.path.join(root, file)
                arquivos_encontrados.append(caminho_completo_arquivo)
    return arquivos_encontrados


# Dicionário para armazenar as pastas do ano encontradas (chave: nome do grupo, valor: caminho da pasta)
pastas_do_ano_caminhos = {}

# Encontrando as pastas do ano atual para Sessoes local
pastas_do_ano_caminhos['local_oe'] = encontrar_pasta_com_ano_atual(caminho_oe)
pastas_do_ano_caminhos['local_tp'] = encontrar_pasta_com_ano_atual(caminho_tp)
pastas_do_ano_caminhos['local_sdc'] = encontrar_pasta_com_ano_atual(caminho_sdc)

# Encontrando as pastas do ano atual para Sessoes drive (apenas identificando, não buscando arquivos aqui)
pastas_do_ano_caminhos['drive_oe'] = encontrar_pasta_com_ano_atual(caminho_drive_oe)
pastas_do_ano_caminhos['drive_tp'] = encontrar_pasta_com_ano_atual(caminho_drive_tp)
pastas_do_ano_caminhos['drive_sdc'] = encontrar_pasta_com_ano_atual(caminho_drive_sdc)

# Dicionário para armazenar os arquivos encontrados para upload (apenas das pastas locais)
arquivos_para_upload = {}

# Vamos iterar apenas sobre as chaves que correspondem às pastas locais
local_keys = ['local_oe', 'local_tp', 'local_sdc']

for key in local_keys:
    caminho_pasta_ano = pastas_do_ano_caminhos.get(key) # Usa .get para evitar KeyError se a chave não existir

    if caminho_pasta_ano: # Garante que só tentará buscar se a pasta do ano foi encontrada
        print(f"\nBuscando em: {caminho_pasta_ano}")
        arquivos = encontrar_arquivos_pdf_com_underline(caminho_pasta_ano)
        arquivos_para_upload[key] = arquivos
        if arquivos:
            for arq in arquivos:
                print(f"  Encontrado: {arq}")
        else:
            print(f"  Nenhum arquivo PDF começando com '_' encontrado em {caminho_pasta_ano}")
    else:
        print(f"\nNão foi possível buscar arquivos para '{key}' pois a pasta do ano não foi encontrada.")

print("\n--- Pastas do ano atual identificadas ---")
for key, path in pastas_do_ano_caminhos.items():
    print(f"{key.replace('_', ' ').title()}: {path if path else 'Não encontrada'}")

print("\n--- Arquivos encontrados para upload (APENAS LOCAIS) ---")
for key, arquivos in arquivos_para_upload.items():
    print(f"Para {key.replace('local_', '').upper()}: {len(arquivos)} arquivos encontrados.")
   