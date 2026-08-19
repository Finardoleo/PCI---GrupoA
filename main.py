import argparse
from pathlib import Path
import pandas as pd
import os
from dotenv import load_dotenv
from solver import solve_task

# Carrega as variáveis do .env
load_dotenv()

def save_to_spreadsheet(filename: str, task_name: str, is_correct: bool, reasoning: str, append: bool):
    status = "CORRECT" if is_correct else "INCORRECT"
    if is_correct is None:
        status = "UNKNOWN (No test output)"
        
    cell_data = f"{status}\n\nReasoning:\n{reasoning}"
    
    # Puxa o nome do modelo do seu .env. Se não achar, usa "AI_Model" como padrão.
    model_col_name = os.getenv("GEMMA_MODEL", "AI_Model")
    
    df_new = pd.DataFrame({
        "Task": [task_name],
        model_col_name: [cell_data]
    })
    
    if append and os.path.exists(filename):
        try:
            df_existing = pd.read_excel(filename)
            if task_name in df_existing['Task'].values:
                df_existing.loc[df_existing['Task'] == task_name, model_col_name] = cell_data
            else:
                df_existing = pd.concat([df_existing, df_new], ignore_index=True)
            df_existing.to_excel(filename, index=False)
        except Exception as e:
            print(f"Erro salvando no Excel: {e}")
    else:
        df_new.to_excel(filename, index=False)

def process_file(filepath: str, output_file: str, append: bool, votes: int):
    try:
        if not Path(filepath).exists():
            print(f"Arquivo não encontrado: {filepath}")
            return
            
        task_name = Path(filepath).name
        
        is_correct, reasoning, grid = solve_task(filepath, num_votes=votes)
        
        print(f"\n========================================")
        print(f"Task: {task_name}")
        print(f"Status: {is_correct}")
        print(f"========================================")
        print(f"Winning Reasoning:\n{reasoning}\n")
        print("Predicted Grid:")
        if grid:
            for row in grid:
                print(row)
        else:
            print("[No grid returned or parsing failed]")
        print(f"========================================\n")
        
        save_to_spreadsheet(output_file, task_name, is_correct, reasoning, append)
        
    except Exception as e:
        # Captura qualquer erro de código, API ou parse, garantindo que o lote continue
        print(f"\n[!] ERRO CRÍTICO ao processar a task {filepath}: {e}")
        
        # Salva o erro na planilha para você saber exatamente o que falhou na análise posterior
        task_name = Path(filepath).name if Path(filepath).exists() else str(filepath)
        save_to_spreadsheet(output_file, task_name, False, f"ERRO DE EXECUÇÃO: {e}", append)

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI Solver")
    parser.add_argument("--mode", choices=['single', 'batch'], required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="results.xlsx")
    parser.add_argument("--new", action="store_true")
    parser.add_argument("--votes", type=int, default=3, help="Número de chamadas à API por task (Padrão: 3)")
    
    args = parser.parse_args()
    
    if args.mode == 'single':
        append_mode = not args.new
        process_file(args.input, args.output, append_mode, args.votes)
        
    elif args.mode == 'batch':
        with open(args.input, 'r') as f:
            tasks = [line.strip() for line in f if line.strip()]
            
        for i, task_path in enumerate(tasks):
            print(f"\n>>> LOTE: Processando {i+1}/{len(tasks)} -> {task_path}")
            
            # BUG FIX: Se a flag --new for passada no modo batch, ela só deve criar um arquivo novo 
            # na PRIMEIRA iteração. Em todas as iterações seguintes, ela deve adicionar os dados (append).
            if args.new and i == 0:
                current_append = False
            else:
                current_append = True
                
            process_file(task_path, args.output, current_append, args.votes)

if __name__ == "__main__":
    main()