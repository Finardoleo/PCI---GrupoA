import argparse
from pathlib import Path
import pandas as pd
import os
import time
from dotenv import load_dotenv
from solver import solve_task

# Carrega as variáveis do .env
load_dotenv()

def save_to_spreadsheet(filename: str, task_name: str, final_extract: str, append: bool):
    # Puxa o nome do modelo do seu .env
    model_col_name = os.getenv("GEMMA_MODEL", "AI_Model")
    
    df_new = pd.DataFrame({
        "Task": [task_name],
        model_col_name: [final_extract]
    })
    
    if append and os.path.exists(filename):
        try:
            df_existing = pd.read_excel(filename)
            if task_name in df_existing['Task'].values:
                df_existing.loc[df_existing['Task'] == task_name, model_col_name] = final_extract
            else:
                df_existing = pd.concat([df_existing, df_new], ignore_index=True)
            df_existing.to_excel(filename, index=False)
        except Exception as e:
            print(f"Erro salvando no Excel: {e}")
    else:
        df_new.to_excel(filename, index=False)

def process_file(filepath: str, output_file: str, append: bool):
    try:
        if not Path(filepath).exists():
            print(f"Arquivo não encontrado: {filepath}")
            return
            
        task_name = Path(filepath).name
        
        # Inicia o cronômetro para esta task específica
        start_time = time.time()
        
        # Recebe apenas a string final bruta
        final_extract = solve_task(filepath)
        
        # Para o cronômetro e calcula o tempo decorrido
        elapsed_time = time.time() - start_time
        
        # Anexa o tempo ao texto que vai para a planilha
        final_extract_with_time = f"{final_extract}\n\nTempo: {elapsed_time:.2f}s"
        
        print(f"\n========================================")
        print(f"Task: {task_name}")
        print(f"Tempo da Task: {elapsed_time:.2f}s")
        print(f"========================================\n")
        
        # Salva o texto bruto (agora com o tempo) na planilha
        save_to_spreadsheet(output_file, task_name, final_extract_with_time, append)
        
    except Exception as e:
        print(f"\n[!] ERRO CRÍTICO ao processar a task {filepath}: {e}")
        task_name = Path(filepath).name if Path(filepath).exists() else str(filepath)
        save_to_spreadsheet(output_file, task_name, f"ERRO DE EXECUÇÃO: {e}", append)

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI Solver")
    parser.add_argument("--mode", choices=['single', 'batch'], required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="results.xlsx")
    parser.add_argument("--new", action="store_true")
    
    args = parser.parse_args()
    
    if args.mode == 'single':
        append_mode = not args.new
        process_file(args.input, args.output, append_mode)
        
    elif args.mode == 'batch':
        with open(args.input, 'r') as f:
            tasks = [line.strip() for line in f if line.strip()]
            
        # Inicia o cronômetro global para o lote inteiro
        batch_start_time = time.time()
            
        for i, task_path in enumerate(tasks):
            print(f"\n>>> LOTE: Processando {i+1}/{len(tasks)} -> {task_path}")
            
            current_append = not (args.new and i == 0)
            process_file(task_path, args.output, current_append)

        # Para o cronômetro do lote e salva o resultado final no Excel
        batch_elapsed_time = time.time() - batch_start_time
        print(f"\n[+] Lote finalizado! Tempo total: {batch_elapsed_time:.2f} segundos.")
        
        # Adiciona a linha final na planilha
        # A primeira coluna será "Tempo do Batch" e a segunda terá os segundos exatos
        save_to_spreadsheet(args.output, "Tempo do Batch", f"{batch_elapsed_time:.2f}s", True)

if __name__ == "__main__":
    main()