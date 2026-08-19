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
        model_col_name: [cell_data]  # Aqui está a coluna dinâmica!
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

def process_file(filepath: str, output_file: str, append: bool):
    if not Path(filepath).exists():
        print(f"Arquivo não encontrado: {filepath}")
        return
        
    task_name = Path(filepath).name
    is_correct, reasoning, grid = solve_task(filepath)
    
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

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI Solver")
    parser.add_argument("--mode", choices=['single', 'batch'], required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="results.xlsx")
    parser.add_argument("--new", action="store_true")
    
    args = parser.parse_args()
    append_mode = not args.new
    
    if args.mode == 'single':
        process_file(args.input, args.output, append_mode)
    elif args.mode == 'batch':
        with open(args.input, 'r') as f:
            tasks = [line.strip() for line in f if line.strip()]
        for task_path in tasks:
            process_file(task_path, args.output, append_mode)

if __name__ == "__main__":
    main()