import argparse
from pathlib import Path
import os
import glob
import time
import queue
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
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
from llmhandler import (
    get_available_api_keys,
    mask_api_key,
    QuotaExhaustedError,
    InvalidApiKeyError
)

# Carrega as variáveis do .env
load_dotenv()

class KeyPoolManager:
    """
    Gerenciador de pool de chaves de API para execução paralela isolada.
    - Cada worker aluga uma chave exclusiva enquanto processa uma task.
    - Se uma chave atinge erro 429 (cota esgotada) ou erro 403 (chave inválida), ela é colocada em quarentena.
    - O restante do lote continua rodando com as chaves saudáveis restantes.
    """
    def __init__(self, api_keys: list):
        self.available_queue = queue.Queue()
        self.all_keys = api_keys
        self.quarantined_keys = set()
        self.lock = threading.Lock()
        
        for k in api_keys:
            self.available_queue.put(k)
            
    def get_key(self, timeout: float = 30.0) -> str:
        """Obtém uma chave disponível da fila. Retorna None se não houver chaves ativas."""
        with self.lock:
            active_count = len(self.all_keys) - len(self.quarantined_keys)
            if active_count == 0:
                return None
        try:
            return self.available_queue.get(timeout=timeout)
        except queue.Empty:
            return None
            
    def release_key(self, key: str):
        """Devolve a chave saudável para a fila de disponíveis."""
        with self.lock:
            if key not in self.quarantined_keys:
                self.available_queue.put(key)
                
    def quarantine_key(self, key: str, reason: str):
        """Isola a chave problemática impedindo que ela seja reutilizada pelos outros workers."""
        with self.lock:
            if key not in self.quarantined_keys:
                self.quarantined_keys.add(key)
                masked = mask_api_key(key)
                remaining = len(self.all_keys) - len(self.quarantined_keys)
                print(f"\n[!] ALERTA: Chave API [{masked}] entrou em QUARENTENA! Motivo: {reason}")
                print(f"[!] Chaves restantes ativas no pool: {remaining}/{len(self.all_keys)}\n")
                
    def has_active_keys(self) -> bool:
        with self.lock:
            return len(self.quarantined_keys) < len(self.all_keys)

def process_file(filepath: str, output_file: str, append: bool, api_key: str = None) -> dict:
    try:
        path_obj = Path(filepath)
        if not path_obj.exists():
            print(f"Arquivo não encontrado: {filepath}")
            return None
            
        task_name = path_obj.name
        masked_key = mask_api_key(api_key) if api_key else "Default"
        
        # Executa a solução da task com a chave dedicada
        result = solve_task(filepath, api_key=api_key)
        
        status = result.get("status", "UNKNOWN")
        timing = result.get("timing", {"reasoning": 0.0, "formatting": 0.0, "total": result.get("solve_time", 0.0)})
        tokens = result.get("tokens", {})
        
        time_str = format_time_string(timing)
        tokens_str = format_tokens_string(tokens)
        
        print(f"\n========================================")
        print(f"Task: {task_name} (Worker Key: {masked_key})")
        print(f"Resultado: [{status}]")
        print(f"Tempo de Inferência: {time_str}")
        print(f"Tokens: {tokens_str}")
        print(f"========================================\n")
        
        # Salva imediatamente nos 5 arquivos CSV separados de forma thread-safe
        save_task_to_split_spreadsheets(output_file, task_name, result, append)
        
        return result
        
    except (QuotaExhaustedError, InvalidApiKeyError):
        raise
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
        save_task_to_split_spreadsheets(output_file, task_name, error_result, append)
        return error_result

def worker_task_wrapper(task_path: str, output_file: str, append: bool, key_mgr: KeyPoolManager) -> dict:
    """Wrapper para execução em thread isolada com aluguel de chave e captura de falhas de cota."""
    key = key_mgr.get_key()
    if not key:
        print(f"[!] Nenhuma chave API saudável disponível para processar '{task_path}'.")
        return None
        
    try:
        res = process_file(task_path, output_file, append=append, api_key=key)
        key_mgr.release_key(key)
        return res
    except QuotaExhaustedError as qe:
        key_mgr.quarantine_key(key, f"Cota de Tokens/RPM excedida (429): {qe}")
        task_name = Path(task_path).name
        error_result = {
            "is_correct": False,
            "status": "ERROR: Quota Exceeded (429)",
            "grid": "",
            "reasoning": f"ERRO DE COTA (429): {qe}",
            "timing": {"reasoning": 0.0, "formatting": 0.0, "total": 0.0},
            "tokens": {"prompt": 0, "candidates": 0, "thoughts": 0, "total": 0}
        }
        save_task_to_split_spreadsheets(output_file, task_name, error_result, append=True)
        return error_result
    except InvalidApiKeyError as ie:
        key_mgr.quarantine_key(key, f"Chave Inválida/Não Autorizada: {ie}")
        task_name = Path(task_path).name
        error_result = {
            "is_correct": False,
            "status": "ERROR: Invalid API Key",
            "grid": "",
            "reasoning": f"ERRO DE CHAVE: {ie}",
            "timing": {"reasoning": 0.0, "formatting": 0.0, "total": 0.0},
            "tokens": {"prompt": 0, "candidates": 0, "thoughts": 0, "total": 0}
        }
        save_task_to_split_spreadsheets(output_file, task_name, error_result, append=True)
        return error_result
    except Exception as e:
        key_mgr.release_key(key)
        task_name = Path(task_path).name
        error_result = {
            "is_correct": False,
            "status": f"ERROR: {e}",
            "grid": "",
            "reasoning": f"ERRO: {e}",
            "timing": {"reasoning": 0.0, "formatting": 0.0, "total": 0.0},
            "tokens": {"prompt": 0, "candidates": 0, "thoughts": 0, "total": 0}
        }
        save_task_to_split_spreadsheets(output_file, task_name, error_result, append=True)
        return error_result

def find_task_filepath(task_name: str, data_dir: str = "data") -> str:
    """Localiza o caminho completo de um arquivo JSON pelo nome da task."""
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
    """Descobre recursivamente todas as tasks JSON no diretório informado."""
    base_path = Path(data_dir)
    tasks = []
    
    if not base_path.exists():
        print(f"[!] Diretório não encontrado: {data_dir}")
        return []
    
    if split == "training":
        search_patterns = [str(base_path / "training" / "*.json")]
    elif split == "evaluation":
        search_patterns = [str(base_path / "evaluation" / "*.json")]
    else:
        search_patterns = [
            str(base_path / "*.json"),
            str(base_path / "**" / "*.json")
        ]
        
    for pattern in search_patterns:
        matched = glob.glob(pattern, recursive=True)
        for p in matched:
            tasks.append(p.replace("\\", "/"))
            
    unique_tasks = sorted(list(dict.fromkeys(tasks)))
    return unique_tasks

def run_tasks_batch(
    tasks: list,
    output_file: str,
    is_new: bool,
    is_retry: bool = False,
    max_workers: int = None
):
    """
    Executa uma lista de tasks em paralelo com pool de chaves API e isolamento de falhas.
    """
    if not tasks:
        print("Nenhuma task encontrada para processar.")
        return

    model_name = os.getenv("GEMMA_MODEL", "AI_Model")
    available_keys = get_available_api_keys()
    
    if not available_keys:
        print("[!] ERRO: Nenhuma chave de API configurada no .env!")
        return
        
    # Define o número de workers com base nas chaves e no argumento
    num_keys = len(available_keys)
    if max_workers is not None:
        workers = max(1, min(int(max_workers), num_keys, 4))
    else:
        workers = max(1, min(num_keys, 4))
        
    key_mgr = KeyPoolManager(available_keys)
    
    print(f"\n========================================")
    print(f"[+] Configuração de Execução:")
    print(f"    Chaves de API Carregadas: {num_keys} ({[mask_api_key(k) for k in available_keys]})")
    print(f"    Workers Simultâneos: {workers}")
    print(f"    Total de Tasks no Lote: {len(tasks)}")
    print(f"========================================\n")
    
    # Se for retry ou new, não pula tasks da lista
    if is_new or is_retry:
        completed_tasks = set()
    else:
        completed_tasks = get_completed_tasks(output_file, model_name)
        if completed_tasks:
            print(f"[i] Detectadas {len(completed_tasks)} tasks já concluídas na planilha para '{model_name}'. Elas serão puladas.")

    # Filtra as tasks pendentes
    pending_tasks = []
    for t in tasks:
        t_name = Path(t).name
        if not is_retry and t_name in completed_tasks:
            continue
        pending_tasks.append(t)
        
    if not pending_tasks:
        print(f"\n[+] Todas as {len(tasks)} tasks já estão concluídas na planilha.")
        return

    print(f"[+] Iniciando processamento de {len(pending_tasks)} tasks pendentes...")

    batch_start_wall_time = time.time()
    correct_count = 0
    newly_processed_count = 0
    batch_timing = {"reasoning": 0.0, "formatting": 0.0, "total": 0.0}
    batch_tokens = {"prompt": 0, "candidates": 0, "thoughts": 0, "total": 0}
    
    interrupted = False
    
    try:
        if workers == 1:
            # Execução sequencial tradicional
            for i, task_path in enumerate(pending_tasks):
                if not key_mgr.has_active_keys():
                    print("[!] Todas as chaves entraram em quarentena. Interrompendo lote.")
                    break
                    
                print(f"\n>>> PROCESSANDO {i+1}/{len(pending_tasks)} -> {task_path}")
                current_append = not (is_new and newly_processed_count == 0)
                res = worker_task_wrapper(task_path, output_file, current_append, key_mgr)
                newly_processed_count += 1
                
                if res:
                    if res.get("is_correct", False):
                        correct_count += 1
                    for k in batch_timing:
                        batch_timing[k] += res.get("timing", {}).get(k, 0.0)
                    for k in batch_tokens:
                        batch_tokens[k] += res.get("tokens", {}).get(k, 0)
        else:
            # Execução paralela com ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {}
                for i, task_path in enumerate(pending_tasks):
                    current_append = not (is_new and i == 0)
                    f = executor.submit(worker_task_wrapper, task_path, output_file, current_append, key_mgr)
                    futures[f] = task_path
                    
                for f in as_completed(futures):
                    task_path = futures[f]
                    try:
                        res = f.result()
                        newly_processed_count += 1
                        if res:
                            if res.get("is_correct", False):
                                correct_count += 1
                            for k in batch_timing:
                                batch_timing[k] += res.get("timing", {}).get(k, 0.0)
                            for k in batch_tokens:
                                batch_tokens[k] += res.get("tokens", {}).get(k, 0)
                    except Exception as e:
                        print(f"[!] Exceção na thread para task {task_path}: {e}")
                        
                    if not key_mgr.has_active_keys():
                        print("\n[!] ALERTA CRÍTICO: Todas as chaves de API estão esgotadas. Cancelando tasks pendentes...")
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                        
    except KeyboardInterrupt:
        print("\n\n[!] EXECUÇÃO INTERROMPIDA PELO USUÁRIO!")
        print("[!] Todas as tasks já processadas foram salvas com segurança.")
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
            print(f"    Tempo Puro de Inferência Somado: {batch_time_str}")
            print(f"    Tempo Total de Parede (Wall Time): {batch_wall_time:.2f}s")
            print(f"    Tokens Totais Consumidos: {batch_tokens_str}")
            print(f"========================================\n")
            
            # Atualiza os resumos em Results/ (thread-safe)
            save_batch_summary_to_split_spreadsheets(
                output_file,
                total_tasks=newly_processed_count,
                correct_tasks=correct_count,
                batch_timing=batch_timing,
                batch_tokens=batch_tokens
            )

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI Solver")
    parser.add_argument("--mode", choices=['single', 'batch', 'all', 'folder', 'dir'], required=False, default='all',
                        help="Modo de execução: single (1 task), batch (lista em .txt), all/folder (todas as tasks do diretório informado em --input)")
    parser.add_argument("--input", default="data", 
                        help="Caminho do arquivo JSON (single), arquivo .txt (batch) ou pasta de tasks (all/folder)")
    parser.add_argument("--split", choices=['all', 'training', 'evaluation'], default='all',
                        help="Filtro para o modo all: 'training', 'evaluation' ou 'all' (padrão: all)")
    parser.add_argument("--output", default="results.csv", 
                        help="Nome base para os 5 arquivos CSV de saída (padrão: results.csv, salvos em Results/)")
    parser.add_argument("--new", action="store_true", 
                        help="Sobrescreve os arquivos CSV existentes e reexecuta todas as tasks em vez de pular as já feitas")
    parser.add_argument("--retry", choices=['incorrect', 'insufficient'], default=None,
                        help="Executa novamente apenas tasks da planilha que falharam: 'incorrect' (todas as incorretas) ou 'insufficient' (apenas incorretas com 'Insufficient data' no reasoning)")
    parser.add_argument("--workers", type=int, default=None,
                        help="Número de workers paralelos simultâneos (1 a 4). Padrão: número de chaves API ativas no .env")
    
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
        valid_tasks = [t for t in resolved_tasks if os.path.exists(t)]
        
        if len(valid_tasks) < len(resolved_tasks):
            missing = set(resolved_tasks) - set(valid_tasks)
            print(f"[!] Aviso: {len(missing)} arquivos JSON não foram localizados na pasta data: {missing}")
            
        run_tasks_batch(valid_tasks, args.output, is_new=False, is_retry=True, max_workers=args.workers)
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
        run_tasks_batch(tasks, args.output, args.new, max_workers=args.workers)
        
    elif args.mode in ['all', 'folder', 'dir']:
        print(f"[+] Escaneando tasks no diretório '{data_dir}' (Split: {args.split})...")
        tasks = collect_all_tasks(data_dir=data_dir, split=args.split)
        print(f"[+] Encontradas {len(tasks)} tasks para processamento.")
        run_tasks_batch(tasks, args.output, args.new, max_workers=args.workers)

if __name__ == "__main__":
    main()