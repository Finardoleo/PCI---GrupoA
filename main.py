import argparse
from pathlib import Path
import pandas as pd
import os
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
            # Mantém a estrutura: se a task já existe, atualiza a coluna do modelo específico
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
        
        # Recebe apenas a string final bruta
        final_extract = solve_task(filepath)
        
        print(f"\n========================================")
        print(f"Task: {task_name}")
        print(f"========================================\n")
        
        # Salva o texto bruto na planilha
        save_to_spreadsheet(output_file, task_name, final_extract, append)
        
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
            
        for i, task_path in enumerate(tasks):
            print(f"\n>>> LOTE: Processando {i+1}/{len(tasks)} -> {task_path}")
            
            # Controle seguro para criar novo arquivo apenas na primeira iteração do batch
            current_append = not (args.new and i == 0)
                
            process_file(task_path, args.output, current_append)

if __name__ == "__main__":
    main()