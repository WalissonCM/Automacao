import re

def parse_time_to_seconds(time_str):
    """
    Converte uma string de tempo no formato [MM:SS] para segundos totais.
    Retorna None se o formato não for válido.
    """
    match = re.match(r'\[(\d{2}):(\d{2})\]', time_str)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return minutes * 60 + seconds
    return None

def format_seconds_to_time(total_seconds):
    """
    Converte segundos totais de volta para o formato [MM:SS].
    """
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"[{minutes:02d}:{seconds:02d}]"

def get_content_lines_and_duration(raw_content):
    """
    Extrai as linhas de conteúdo e a duração total de um arquivo,
    ignorando a linha "Interlocutor 0:" e armazenando timestamps e texto.
    """
    content_lines_data = []
    last_timestamp_seconds = 0
    
    # Divide o conteúdo em linhas e remove linhas vazias
    lines = [line for line in raw_content.split('\n') if line.strip()]

    for line in lines:
        if line.strip() == "Interlocutor 0:":
            continue # Ignora a linha do interlocutor
        
        # Tenta encontrar o timestamp no início da linha
        time_match = re.match(r'\[\d{2}:\d{2}\]\s*(.*)', line)
        if time_match:
            time_str = line[time_match.start():time_match.end() - len(time_match.group(1))].strip()
            text = time_match.group(1).strip()
            
            seconds = parse_time_to_seconds(time_str)
            if seconds is not None:
                content_lines_data.append((seconds, text))
                last_timestamp_seconds = seconds # Atualiza a última timestamp encontrada
            else:
                # Se o timestamp não for válido, trata como texto sem timestamp
                content_lines_data.append((None, line.strip()))
        else:
            # Se não houver timestamp, adiciona a linha como texto sem timestamp
            content_lines_data.append((None, line.strip()))
            
    return content_lines_data, last_timestamp_seconds


# Nomes dos arquivos
file_names = ["Parte 1.txt", "Parte 2.txt", "Parte 3.txt"]
all_files_data = []
all_files_durations = []

# 1. Ler e pré-processar todos os arquivos
for file_name in file_names:
    try:
        # Busca o conteúdo do arquivo
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Obtém as linhas de conteúdo e a duração original de cada arquivo
        lines_data, duration = get_content_lines_and_duration(content)
        all_files_data.append(lines_data)
        all_files_durations.append(duration)
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_name}: {e}")
        # Se um arquivo não puder ser lido, continua com os outros, mas com dados vazios para este
        all_files_data.append([])
        all_files_durations.append(0)


final_output_lines = ["Interlocutor 0:"] # A linha do interlocutor aparece apenas uma vez no início
current_offset_seconds = 0

# 2. Processar cada parte e combinar
for i, file_data in enumerate(all_files_data):
    if not file_data: # Pula se o arquivo estiver vazio ou não pôde ser lido
        continue

    # Verifica a regra de mesclagem para a Parte 2 e Parte 3
    if i > 0 and file_data[0][0] == 0: # Se o primeiro timestamp for [00:00]
        # Anexa o texto da primeira linha ao final da última linha do output
        if final_output_lines:
            last_line_in_output = final_output_lines[-1]
            # Garante que a última linha não seja apenas "Interlocutor 0:"
            if last_line_in_output == "Interlocutor 0:":
                final_output_lines.append(file_data[0][1])
            else:
                final_output_lines[-1] = last_line_in_output + " " + file_data[0][1]
        else:
            final_output_lines.append(file_data[0][1]) # Adiciona se não houver linhas anteriores
        
        # Processa as linhas restantes do arquivo (a partir da segunda linha)
        lines_to_process = file_data[1:]
    else:
        # Processa todas as linhas do arquivo
        lines_to_process = file_data

    # Adiciona as linhas processadas ao output final
    for seconds, text in lines_to_process:
        if seconds is not None:
            new_seconds = seconds + current_offset_seconds
            formatted_time = format_seconds_to_time(new_seconds)
            final_output_lines.append(f"{formatted_time} {text}")
        else:
            final_output_lines.append(text)
    
    # Atualiza o offset para o próximo arquivo
    current_offset_seconds += all_files_durations[i]

# Junta todas as linhas processadas em uma única string
combined_text = "\n".join(final_output_lines)

# Salva o texto combinado em um novo arquivo
output_file_name = "Arquivo_trascricao_unico.txt"
try:
    with open(output_file_name, 'w', encoding='utf-8') as f:
        f.write(combined_text)
    print(f"Conteúdo combinado salvo com sucesso em '{output_file_name}'")
except Exception as e:
    print(f"Erro ao salvar o arquivo: {e}")
