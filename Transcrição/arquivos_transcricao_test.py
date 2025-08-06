import re
import tkinter as tk
from tkinter import filedialog, messagebox

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
    
    lines = [line for line in raw_content.split('\n') if line.strip()]

    for line in lines:
        if line.strip() == "Interlocutor 0:":
            continue

        time_match = re.match(r'\[(\d{2}:\d{2})\]\s*(.*)', line)
        if time_match:
            time_str = f"[{time_match.group(1)}]"
            text = time_match.group(2).strip()
            
            seconds = parse_time_to_seconds(time_str)
            if seconds is not None:
                content_lines_data.append((seconds, text))
                last_timestamp_seconds = seconds
            else:
                content_lines_data.append((None, line.strip()))
        else:
            content_lines_data.append((None, line.strip()))
            
    return content_lines_data, last_timestamp_seconds


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Combinar Arquivos de Transcrição")
        self.geometry("500x300")
        
        self.file_names = []
        
        self.create_widgets()

    def create_widgets(self):
        # Frame para os botões e lista
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=5)

        # Botão para adicionar arquivos
        add_button = tk.Button(button_frame, text="Adicionar Arquivos", command=self.add_files)
        add_button.pack(side=tk.LEFT, padx=50)

        # Botão para remover arquivos
        remove_button = tk.Button(button_frame, text="Remover Selecionado", command=self.remove_file)
        remove_button.pack(side=tk.LEFT, padx=50)
        
        # Lista para exibir os arquivos
        self.listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=10)
        self.listbox.pack(fill="both", expand=True)
        
        # Botão para processar
        process_button = tk.Button(frame, text="Processar e Salvar", command=self.process_files)
        process_button.pack(pady=5)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Selecione os arquivos de transcrição",
            filetypes=[("Arquivos de Texto", "*.txt")]
        )
        if files:
            for file_path in files:
                self.file_names.append(file_path)
                self.listbox.insert(tk.END, file_path)

    def remove_file(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado para remoção.")
            return

        # Para cada índice selecionado (mesmo que seja apenas um)
        for index in reversed(selected_indices):  # Itera de trás para frente para evitar problemas de índice
            # Remove da lista interna de caminhos
            del self.file_names[index]
            # Remove da listbox da interface
            self.listbox.delete(index)

    def process_files(self):
        if not self.file_names:
            messagebox.showwarning("Aviso", "Nenhum arquivo foi adicionado.")
            return

        all_files_data = []
        all_files_durations = []

        # 1. Ler e pré-processar todos os arquivos
        for file_name in self.file_names:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines_data, duration = get_content_lines_and_duration(content)
                all_files_data.append(lines_data)
                all_files_durations.append(duration)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler o arquivo {file_name}: {e}")
                return

        final_output_lines = ["Interlocutor 0:"]
        current_offset_seconds = 0

        # 2. Processar cada parte e combinar
        for i, file_data in enumerate(all_files_data):
            if not file_data:
                continue

            if i > 0 and file_data[0][0] == 0:
                if final_output_lines and final_output_lines[-1] != "Interlocutor 0:":
                    final_output_lines[-1] += " " + file_data[0][1]
                else:
                    final_output_lines.append(file_data[0][1])
                
                lines_to_process = file_data[1:]
            else:
                lines_to_process = file_data

            for seconds, text in lines_to_process:
                if seconds is not None:
                    new_seconds = seconds + current_offset_seconds
                    formatted_time = format_seconds_to_time(new_seconds)
                    final_output_lines.append(f"{formatted_time} {text}")
                else:
                    final_output_lines.append(text)
            
            if i < len(all_files_durations):
                current_offset_seconds += all_files_durations[i]

        combined_text = "\n".join(final_output_lines)

        # 3. Salvar o arquivo de saída
        self.save_output_file(combined_text)

    def save_output_file(self, content):
        output_file_name = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt")],
            title="Salvar arquivo combinado como"
        )
        if output_file_name:
            try:
                with open(output_file_name, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Sucesso", f"Conteúdo combinado salvo em '{output_file_name}'")
                self.listbox.delete(0, tk.END)
                self.file_names.clear()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()