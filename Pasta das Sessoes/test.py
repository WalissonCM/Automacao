import os
import re
import shutil
from datetime import datetime
import traceback

# --- Caminhos das pastas de sessão ---
caminho_oe = r"C:\Users\wally\Desktop\Sessoes local\OE"
caminho_tp = r"C:\Users\wally\Desktop\Sessoes local\PLENO"
caminho_sdc = r"C:\Users\wally\Desktop\Sessoes local\SDC"

# --- Caminhos das pastas de sessão do Drive ---
caminho_drive_oe = r"C:\Users\wally\Desktop\Sessoes drive\OE"
caminho_drive_tp = r"C:\Users\wally\Desktop\Sessoes drive\PLENO"
caminho_drive_sdc = r"C:\Users\wally\Desktop\Sessoes drive\SDC"

# --- Mapeamentos de Pastas do Drive ---
PASTA_SESSAO_DRIVE_MAP = {
    'OE': {
        'Extraordinária': lambda num: f"{num}ª Extraordinária OE",
        'Ordinária': lambda num: f"{num}ª Sessão Ordinária OE"
    },
    'PLENO': {
        'Extraordinária': lambda num: f"{num}ª Extraordinária TP",
        'Ordinária': lambda num: f"{num}ª Sessão Ordinária TP"
    },
    'SDC': {
        'Sessão': lambda num: f"{num}ª Sessão SDC"
    }
}

# Chaves corrigidas para refletir os nomes de pasta LOCAIS realmente encontrados
PASTA_TIPO_PAUTA_DRIVE_MAP = {
    "P A U T A_administrativa": "Pauta Administrativa",
    "Retornos de VR e Adiados": "Retorno de Vista Regimental",
    "P A U T A": "Pauta Judicial",
}

# --- Expressões regulares com o padrão "XX_Xª Sessão..." ---
# O padrão espera "dígito_dígitoª/º" no início, seguido de qualquer coisa (.*?)
# e então o tipo da sessão.
# Capture o número da sessão diretamente no primeiro grupo
# Ajuste: Removido \b final para maior flexibilidade em 'Ordinária' e 'Extraordinária'
REGEX_SESSAO_ORDINARIA = r'^\d{2}_(\d+)[ªº].*?Ordinária'
REGEX_SESSAO_EXTRAORDINARIA = r'^\d{2}_(\d+)[ªº].*?Extraordinária'
REGEX_SESSAO_SDC = r'^\d{2}_(\d+)[ªº].*?Sessão' # SDC mantém, já que não temos um caso de falha aqui

# --- Funções Auxiliares ---

def encontrar_pasta_com_ano_atual(caminho_base):
    """
    Encontra a pasta que contém o ano atual no nome dentro de um diretório base.
    """
    ano_atual = str(datetime.now().year)
    pastas_encontradas = []

    if not os.path.isdir(caminho_base):
        print(f"Caminho base não encontrado ou não é um diretório: {caminho_base}")
        return None

    for nome_item in os.listdir(caminho_base):
        caminho_completo_item = os.path.join(caminho_base, nome_item)

        if os.path.isdir(caminho_completo_item):
            if re.search(r'\b' + ano_atual + r'\b', nome_item):
                pastas_encontradas.append(caminho_completo_item)
            elif re.search(r'\b(\d{4})\b', nome_item):
                match = re.search(r'\b(\d{4})\b', nome_item)
                if match and match.group(1) == ano_atual:
                    pastas_encontradas.append(caminho_completo_item)

    if pastas_encontradas:
        if len(pastas_encontradas) > 1:
            print(f"Atenção: Múltiplas pastas com o ano atual '{ano_atual}' encontradas em '{caminho_base}'. Pegando a primeira: {pastas_encontradas[0]}")
        return pastas_encontradas[0]
    else:
        print(f"Nenhuma pasta contendo o ano atual ({ano_atual}) encontrada em: {caminho_base}")
        return None

def encontrar_arquivos_pdf_com_underline(caminho_pasta_base):
    """
    Encontra arquivos PDF que começam com '_' em um diretório e suas subpastas.
    """
    arquivos_encontrados = []
    if not caminho_pasta_base or not os.path.isdir(caminho_pasta_base):
        print(f"Caminho inválido ou não encontrado para buscar arquivos: {caminho_pasta_base}")
        return arquivos_encontrados

    for root, dirs, files in os.walk(caminho_pasta_base):
        for file in files:
            if file.lower().endswith('.pdf') and file.startswith('_'):
                caminho_completo_arquivo = os.path.join(root, file)
                arquivos_encontrados.append(caminho_completo_arquivo)
    return arquivos_encontrados

# --- Função Principal para Copiar Arquivos ---

def copiar_arquivos_para_drive(arquivos_locais_para_copiar, pastas_do_ano_caminhos):
    print("\n--- Iniciando Cópia de Arquivos para o Drive ---")

    for local_key, arquivos_na_categoria in arquivos_locais_para_copiar.items():
        if not arquivos_na_categoria:
            print(f"Nenhum arquivo para copiar para a categoria {local_key.replace('local_', '').upper()}.")
            continue

        categoria_sigla = local_key.replace('local_', '').upper() # OE, TP, SDC
        
        caminho_base_local_ano = pastas_do_ano_caminhos.get(local_key)
        if not caminho_base_local_ano:
            print(f"Erro interno: Caminho base local do ano não encontrado para {local_key}. Pulando.")
            continue

        drive_key = local_key.replace('local_', 'drive_')
        caminho_base_drive_ano = pastas_do_ano_caminhos.get(drive_key)

        if not caminho_base_drive_ano:
            print(f"Erro: Pasta do ano no Drive não encontrada para {categoria_sigla}. Pulando arquivos desta categoria.")
            continue

        print(f"\nProcessando arquivos para {categoria_sigla}...")

        for caminho_arquivo_origem in arquivos_na_categoria:
            try:
                dir_arquivo = os.path.dirname(caminho_arquivo_origem)
                caminho_relativo_a_ano = os.path.relpath(dir_arquivo, caminho_base_local_ano)
                partes_relativas = caminho_relativo_a_ano.split(os.sep)

                pasta_da_sessao_local = None
                pasta_da_pauta_local = None

                # Itera de trás para frente para encontrar a pasta da pauta e a pasta da sessão
                for i in range(len(partes_relativas) - 1, -1, -1):
                    parte_atual = partes_relativas[i]
                    if parte_atual in PASTA_TIPO_PAUTA_DRIVE_MAP:
                        pasta_da_pauta_local = parte_atual
                        if i > 0:
                            pasta_da_sessao_local = partes_relativas[i-1]
                        break

                if not pasta_da_sessao_local or not pasta_da_pauta_local:
                    print(f"Não foi possível identificar a pasta da sessão ou da pauta local para: {caminho_arquivo_origem}. Partes relativas: {partes_relativas}. Pulando.")
                    continue
                
                # Limpa a string da pasta da sessão antes de usar regex
                pasta_da_sessao_local_limpa = pasta_da_sessao_local.strip()
                categoria_origem = categoria_sigla

                num_sessao = None
                chave_mapeamento_sessao = None

                # Tenta casar com Extraordinária primeiro (mais específico)
                match_extraordinaria = re.search(REGEX_SESSAO_EXTRAORDINARIA, pasta_da_sessao_local_limpa, re.IGNORECASE)
                if match_extraordinaria:
                    num_sessao = int(match_extraordinaria.group(1)) # Usa o grupo capturado pela regex
                    chave_mapeamento_sessao = 'Extraordinária'
                else: # Se não for extraordinária, tenta ordinária (ou geral para SDC)
                    if categoria_origem == 'OE' or categoria_origem == 'PLENO':
                        match_ordinaria = re.search(REGEX_SESSAO_ORDINARIA, pasta_da_sessao_local_limpa, re.IGNORECASE)
                        if match_ordinaria:
                            num_sessao = int(match_ordinaria.group(1)) # Usa o grupo capturado pela regex
                            chave_mapeamento_sessao = 'Ordinária'
                    elif categoria_origem == 'SDC':
                        match_sessao = re.search(REGEX_SESSAO_SDC, pasta_da_sessao_local_limpa, re.IGNORECASE)
                        if match_sessao:
                            num_sessao = int(match_sessao.group(1)) # Usa o grupo capturado pela regex
                            chave_mapeamento_sessao = 'Sessão'

                if num_sessao is None or chave_mapeamento_sessao is None:
                    # Mensagem de debug mais detalhada para o caso falho
                    print(f"DEBUG: Falha ao extrair tipo/número para a pasta: '{pasta_da_sessao_local}'")
                    print(f"DEBUG: String limpa usada na regex: '{pasta_da_sessao_local_limpa}'")
                    print(f"Não foi possível extrair número/tipo da sessão do nome da pasta local: '{pasta_da_sessao_local}' para categoria '{categoria_origem}'. Pulando.")
                    continue
                
                funcao_nome_sessao_drive = PASTA_SESSAO_DRIVE_MAP[categoria_origem].get(chave_mapeamento_sessao)
                if not funcao_nome_sessao_drive:
                    print(f"Mapeamento de função de nome de sessão não encontrado para {categoria_origem} - {chave_mapeamento_sessao}. Pulando.")
                    continue
                
                nome_pasta_sessao_drive = funcao_nome_sessao_drive(num_sessao)

                nome_subpasta_pauta_drive = PASTA_TIPO_PAUTA_DRIVE_MAP.get(pasta_da_pauta_local)
                if not nome_subpasta_pauta_drive:
                    print(f"Erro inesperado: Mapeamento de pasta de pauta '{pasta_da_pauta_local}' não encontrado. Pulando.")
                    continue

                # 2. Construir o caminho de destino no Drive
                caminho_destino_sessao = os.path.join(caminho_base_drive_ano, nome_pasta_sessao_drive)
                caminho_destino_final = os.path.join(caminho_destino_sessao, nome_subpasta_pauta_drive)

                if not os.path.exists(caminho_destino_final):
                    print(f"Criando diretório de destino: {caminho_destino_final}")
                    os.makedirs(caminho_destino_final, exist_ok=True)

                nome_arquivo_original = os.path.basename(caminho_arquivo_origem)
                nome_arquivo_destino = nome_arquivo_original
                if nome_arquivo_destino.startswith('_'):
                    nome_arquivo_destino = nome_arquivo_destino[1:]

                caminho_arquivo_destino = os.path.join(caminho_destino_final, nome_arquivo_destino)

                print(f"Copiando '{nome_arquivo_original}' (local) para '{nome_arquivo_destino}' (Drive) em:\n  '{caminho_destino_final}'")
                shutil.copy2(caminho_arquivo_origem, caminho_arquivo_destino)
                print("Cópia bem-sucedida!")

            except Exception as e:
                print(f"Erro ao processar o arquivo '{caminho_arquivo_origem}': {e}")
                print(f"Detalhes do erro:\n{traceback.format_exc()}")

# --- Execução Principal do Script ---
if __name__ == "__main__":
    pastas_do_ano_caminhos = {}

    print("--- Encontrando pastas do ano atual (Sessões Locais) ---")
    pastas_do_ano_caminhos['local_oe'] = encontrar_pasta_com_ano_atual(caminho_oe)
    pastas_do_ano_caminhos['local_tp'] = encontrar_pasta_com_ano_atual(caminho_tp)
    pastas_do_ano_caminhos['local_sdc'] = encontrar_pasta_com_ano_atual(caminho_sdc)

    print("\n--- Encontrando pastas do ano atual (Sessões Drive) ---")
    pastas_do_ano_caminhos['drive_oe'] = encontrar_pasta_com_ano_atual(caminho_drive_oe)
    pastas_do_ano_caminhos['drive_tp'] = encontrar_pasta_com_ano_atual(caminho_drive_tp)
    pastas_do_ano_caminhos['drive_sdc'] = encontrar_pasta_com_ano_atual(caminho_drive_sdc)

    arquivos_para_upload_locais = {}

    print("\n--- Buscando arquivos PDF com '_' nas pastas LOCAIS do ano ---")
    local_keys = ['local_oe', 'local_tp', 'local_sdc']

    for key in local_keys:
        caminho_pasta_ano = pastas_do_ano_caminhos.get(key)
        if caminho_pasta_ano:
            print(f"\nBuscando em: {caminho_pasta_ano}")
            arquivos = encontrar_arquivos_pdf_com_underline(caminho_pasta_ano)
            arquivos_para_upload_locais[key] = arquivos
            if arquivos:
                for arq in arquivos:
                    print(f"  Encontrado: {arq}")
            else:
                print(f"  Nenhum arquivo PDF começando com '_' encontrado em {caminho_pasta_ano}")
        else:
            print(f"\nNão foi possível buscar arquivos para '{key}' pois a pasta do ano não foi encontrada.")

    copiar_arquivos_para_drive(arquivos_para_upload_locais, pastas_do_ano_caminhos)

    print("\n--- Processo de automação concluído ---")