import argparse
from pathlib import Path
import os
import glob
import time
from dotenv import load_dotenv
from solver import solve_task
from spreadsheet import (
    save_task_to_split_spreadsheets,
    save_batch_summary_to_split_spreadsheets,
    get_completed_tasks,
    get_retry_tasks,
    format_time_string,
    format_tokens_string
)

# Carrega as variáveis do .env
load_dotenv()

def process_file(filepath: str, output_file: str, append: bool) -> dict:
    try:
        path_obj = Path(filepath)
        if not path_obj.exists():
            print(f"Arquivo não encontrado: {filepath}")
            return None
            
        task_name = path_obj.name
        
        # Executa a solução da task (retorna dict com is_correct, status, grid, reasoning, timing, tokens)
        result = solve_task(filepath)
        
        status = result.get("status", "UNKNOWN")
        timing = result.get("timing", {"reasoning": 0.0, "formatting": 0.0, "total": result.get("solve_time", 0.0)})
        tokens = result.get("tokens", {})
        
        time_str = format_time_string(timing)
        tokens_str = format_tokens_string(tokens)
        
        print(f"\n========================================")
        print(f"Task: {task_name}")
        print(f"Resultado: [{status}]")
        print(f"Tempo de Inferência: {time_str}")
        print(f"Tokens: {tokens_str}")
        print(f"========================================\n")
        
        # Salva imediatamente nos 5 arquivos CSV separados (_accuracy, _tokens, _reasoning, _grids, _times)
        save_task_to_split_spreadsheets(output_file, task_name, result, append)
        
        return result
        
    except Exception as e:
        print(f"\n[!] ERRO CRÍTICO ao processar a task {filepath}: {e}")
        task_name = Path(filepath).name if Path(filepath).exists() else str(filepath)
        error_result = {
            "is_correct": False,
            "status": f"ERROR: {e}",
            "grid": "",
            "reasoning": f"ERRO: {e}",
            "timing": {"reasoning": 0.0, "formatting": 0.0, "total": 0.0},
            "tokens": {"prompt": 0, "candidates": 0, "thoughts": 0, "total": 0}
        }
        # Salva o erro imediatamente para garantir persistência
        save_task_to_split_spreadsheets(output_file, task_name, error_result, append)
        return error_result

def find_task_filepath(task_name: str, data_dir: str = "data") -> str:
    """
    Localiza o caminho completo de um arquivo JSON pelo nome da task.
    """
    if os.path.exists(task_name):
        return task_name.replace("\\", "/")
        
    for sub in ["training", "evaluation", ""]:
        candidate = os.path.join(data_dir, sub, task_name)
        if os.path.exists(candidate):
            return candidate.replace("\\", "/")
            
    matches = glob.glob(f"{data_dir}/**/{task_name}", recursive=True)
    if matches:
        return matches[0].replace("\\", "/")
        
    return task_name

def collect_all_tasks(data_dir: str = "data", split: str = "all") -> list:
    """
    Descobre recursivamente todas as tasks JSON na pasta data.
    """
    base_path = Path(data_dir)
    tasks = []
    
    if split == "training":
        search_patterns = [base_path / "training" / "*.json"]
    elif split == "evaluation":
        search_patterns = [base_path / "evaluation" / "*.json"]
    else:
        search_patterns = [
            base_path / "training" / "*.json",
            base_path / "evaluation" / "*.json",
            base_path / "*.json"
        ]
        
    for pattern in search_patterns:
        matched = glob.glob(str(pattern))
        for p in matched:
            tasks.append(p.replace("\\", "/"))
            
    # Remove duplicatas mantendo a ordem e ordena alfabeticamente
    unique_tasks = sorted(list(dict.fromkeys(tasks)))
    return unique_tasks

def run_tasks_batch(tasks: list, output_file: str, is_new: bool, is_retry: bool = False):
    """
    Executa uma lista de tasks sequencialmente, pulando tasks já concluídas na planilha (a menos que seja retry/new),
    garantindo persistência imediata e salvamento de estatísticas mesmo em caso de interrupção (Ctrl+C).
    """
    if not tasks:
        print("Nenhuma task encontrada para processar.")
        return

    model_name = os.getenv("GEMMA_MODEL", "AI_Model")
    
    # Se for retry ou new, não pula tasks da lista
    if is_new or is_retry:
        completed_tasks = set()
    else:
        completed_tasks = get_completed_tasks(output_file, model_name)
        if completed_tasks:
            print(f"[i] Detectadas {len(completed_tasks)} tasks já concluídas na planilha para '{model_name}'. Elas serão puladas.")

    batch_start_wall_time = time.time()
    correct_count = 0
    newly_processed_count = 0
    batch_timing = {
        "reasoning": 0.0,
        "formatting": 0.0,
        "total": 0.0
    }
    batch_tokens = {
        "prompt": 0,
        "candidates": 0,
        "thoughts": 0,
        "total": 0
    }
    
    interrupted = False
    
    try:
        for i, task_path in enumerate(tasks):
            task_name = Path(task_path).name
            
            # Pula tasks já concluídas se não for retry/new
            if not is_retry and task_name in completed_tasks:
                print(f"[-] [{i+1}/{len(tasks)}] Task '{task_name}' já preenchida para '{model_name}'. Pulando...")
                continue
            
            print(f"\n>>> PROCESSANDO {i+1}/{len(tasks)} -> {task_path}")
            
            # Se for a primeira task e --new foi especificado, sobrescreve o arquivo; depois só dá append
            current_append = not (is_new and newly_processed_count == 0)
            res = process_file(task_path, output_file, current_append)
            newly_processed_count += 1
            
            if res:
                if res.get("is_correct", False):
                    correct_count += 1
                res_timing = res.get("timing", {})
                for k in batch_timing:
                    batch_timing[k] += res_timing.get(k, 0.0)
                    
                res_tokens = res.get("tokens", {})
                for k in batch_tokens:
                    batch_tokens[k] += res_tokens.get(k, 0)
                    
    except KeyboardInterrupt:
        print("\n\n[!] EXECUÇÃO INTERROMPIDA PELO USUÁRIO!")
        print("[!] Todas as tasks já testadas foram salvas nos arquivos CSV.")
        interrupted = True
    except Exception as e:
        print(f"\n\n[!] ERRO INESPERADO DURANTE O LOTE: {e}")
        interrupted = True
    finally:
        total_finished = len(completed_tasks) + newly_processed_count
        if newly_processed_count > 0:
            batch_wall_time = time.time() - batch_start_wall_time
            batch_time_str = format_time_string(batch_timing)
            batch_tokens_str = format_tokens_string(batch_tokens)
            accuracy_pct = (correct_count / newly_processed_count * 100)
            
            status_title = "LOTE PARCIAL FINALIZADO" if interrupted else "LOTE FINALIZADO"
            print(f"\n========================================")
            print(f"[+] {status_title}!")
            print(f"    Tasks Executadas Nesta Rodada: {newly_processed_count}")
            if not is_retry:
                print(f"    Total Acumulado de Tasks na Planilha: {total_finished}/{len(tasks)}")
            print(f"    Acurácia desta rodada: {accuracy_pct:.2f}% ({correct_count}/{newly_processed_count})")
            print(f"    Tempo Puro de Inferência: {batch_time_str}")
            print(f"    Tempo Total Real: {batch_wall_time:.2f}s")
            print(f"    Tokens Totais: {batch_tokens_str}")
            print(f"========================================\n")
            
            # Salva o resumo nos arquivos CSV (recalcula a acurácia global da planilha)
            save_batch_summary_to_split_spreadsheets(
                output_file,
                total_tasks=newly_processed_count,
                correct_tasks=correct_count,
                batch_timing=batch_timing,
                batch_tokens=batch_tokens
            )
        elif completed_tasks and not interrupted:
            print(f"\n[+] Todas as {len(completed_tasks)} tasks do lote já estavam concluídas na planilha para o modelo '{model_name}'.")

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI Solver")
    parser.add_argument("--mode", choices=['single', 'batch', 'all'], required=False, default='all',
                        help="Modo de execução: single (1 task), batch (lista em arquivo .txt), all (todas as tasks da pasta data)")
    parser.add_argument("--input", default="data", 
                        help="Caminho do arquivo JSON (single), arquivo .txt (batch) ou pasta do dataset (all)")
    parser.add_argument("--split", choices=['all', 'training', 'evaluation'], default='all',
                        help="Filtro para o modo all: 'training', 'evaluation' ou 'all' (padrão: all)")
    parser.add_argument("--output", default="results.csv", 
                        help="Nome base para os 5 arquivos CSV de saída (padrão: results.csv)")
    parser.add_argument("--new", action="store_true", 
                        help="Sobrescreve os arquivos CSV existentes e reexecuta todas as tasks em vez de pular as já feitas")
    parser.add_argument("--retry", choices=['incorrect', 'insufficient'], default=None,
                        help="Executa novamente apenas tasks da planilha que falharam: 'incorrect' (todas as incorretas) ou 'insufficient' (apenas incorretas com 'Insufficient data' no reasoning)")
    
    args = parser.parse_args()
    model_name = os.getenv("GEMMA_MODEL", "AI_Model")
    data_dir = args.input if os.path.isdir(args.input) else "data"
    
    # Modo de Retry
    if args.retry:
        print(f"[+] Modo RETRY ativado com filtro '{args.retry}' para o modelo '{model_name}' em '{args.output}'...")
        tasks_to_retry = get_retry_tasks(args.output, args.retry, model_name)
        if not tasks_to_retry:
            print(f"[+] Nenhuma task com filtro '{args.retry}' encontrada na planilha '{args.output}'.")
            return
            
        print(f"[+] Encontradas {len(tasks_to_retry)} tasks para reexecução: {tasks_to_retry}")
        resolved_tasks = [find_task_filepath(t, data_dir) for t in tasks_to_retry]
        
        # Filtra apenas caminhos existentes
        valid_tasks = [t for t in resolved_tasks if os.path.exists(t)]
        if len(valid_tasks) < len(resolved_tasks):
            missing = set(resolved_tasks) - set(valid_tasks)
            print(f"[!] Aviso: {len(missing)} arquivos JSON não foram localizados na pasta data: {missing}")
            
        run_tasks_batch(valid_tasks, args.output, is_new=False, is_retry=True)
        return

    # Execução normal
    if args.mode == 'single':
        if not args.new:
            completed = get_completed_tasks(args.output, model_name)
            task_name = Path(args.input).name
            if task_name in completed:
                print(f"[-] Task '{task_name}' já está preenchida para '{model_name}' em '{args.output}'. Use a flag --new para forçar a reexecução.")
                return
                
        append_mode = not args.new
        process_file(args.input, args.output, append_mode)
        
    elif args.mode == 'batch':
        if not os.path.exists(args.input):
            print(f"Arquivo de lote não encontrado: {args.input}")
            return
            
        with open(args.input, 'r', encoding='utf-8') as f:
            tasks = [line.strip() for line in f if line.strip()]
            
        print(f"[+] Iniciando modo BATCH com {len(tasks)} tasks listadas em '{args.input}'...")
        run_tasks_batch(tasks, args.output, args.new)
        
    elif args.mode == 'all':
        print(f"[+] Escaneando dataset em '{data_dir}' (Split: {args.split})...")
        tasks = collect_all_tasks(data_dir=data_dir, split=args.split)
        print(f"[+] Encontradas {len(tasks)} tasks para processamento.")
        run_tasks_batch(tasks, args.output, args.new)

if __name__ == "__main__":
    main()