import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from typing import Tuple, Set, List

load_dotenv()

SUMMARY_ROW_NAMES = ["Batch Accuracy", "Tempo do Batch", "Tokens do Batch"]
DEFAULT_RESULTS_DIR = "Results"

def resolve_spreadsheet_paths(base_filename: str) -> Tuple[Path, str]:
    """
    Resolve o diretório e o nome base para as planilhas.
    Se nenhum diretório for especificado (ex: 'results.csv'), direciona para 'Results/'.
    Garante que a pasta de destino exista.
    """
    path_obj = Path(base_filename)
    if path_obj.parent == Path("."):
        dir_path = Path(DEFAULT_RESULTS_DIR)
    else:
        dir_path = path_obj.parent
        
    dir_path.mkdir(parents=True, exist_ok=True)
    base_stem = path_obj.stem
    return dir_path, base_stem

def format_tokens_string(tokens: dict) -> str:
    prompt = tokens.get("prompt", 0)
    candidates = tokens.get("candidates", 0)
    thoughts = tokens.get("thoughts", 0)
    total = tokens.get("total", 0)
    return f"Total: {total} (Prompt: {prompt}, Resposta: {candidates}, Pensamento: {thoughts})"

def format_time_string(timing: dict) -> str:
    total = timing.get("total", 0.0)
    reasoning = timing.get("reasoning", 0.0)
    formatting = timing.get("formatting", 0.0)
    return f"Total: {total:.2f}s (Raciocínio: {reasoning:.2f}s, Formatação: {formatting:.2f}s)"

def get_completed_tasks(base_filename: str, model_col_name: str = None) -> Set[str]:
    """
    Retorna o conjunto de nomes de tasks que já foram processadas com sucesso para este modelo.
    """
    model_col_name = model_col_name or os.getenv("GEMMA_MODEL", "AI_Model")
    dir_path, base = resolve_spreadsheet_paths(base_filename)
    acc_file = os.path.join(dir_path, f"{base}_accuracy.csv")
    
    if not os.path.exists(acc_file):
        return set()
        
    try:
        df = pd.read_csv(acc_file)
        if "Task" not in df.columns or model_col_name not in df.columns:
            return set()
            
        completed = set()
        for _, row in df.iterrows():
            task = str(row["Task"]).strip()
            if task in SUMMARY_ROW_NAMES:
                continue
            val = str(row[model_col_name]).strip()
            if val and val.lower() != "nan" and not val.startswith("ERROR"):
                completed.add(task)
        return completed
    except Exception as e:
        print(f"Aviso ao verificar tasks já concluídas: {e}")
        return set()

def get_retry_tasks(base_filename: str, retry_mode: str = "incorrect", model_col_name: str = None) -> List[str]:
    """
    Retorna a lista de nomes de tasks a serem reexecutadas com base no filtro:
      - 'incorrect': Todas as tasks com status INCORRECT, ERROR ou UNKNOWN na planilha de acurácia.
      - 'insufficient': Tasks com falha que também contenham 'insufficient data' na planilha de reasoning.
    """
    model_col_name = model_col_name or os.getenv("GEMMA_MODEL", "AI_Model")
    dir_path, base = resolve_spreadsheet_paths(base_filename)
    
    acc_file = os.path.join(dir_path, f"{base}_accuracy.csv")
    rea_file = os.path.join(dir_path, f"{base}_reasoning.csv")
    
    if not os.path.exists(acc_file):
        print(f"[!] Arquivo de acurácia '{acc_file}' não encontrado para aplicar o filtro de retry.")
        return []
        
    try:
        df_acc = pd.read_csv(acc_file)
        if "Task" not in df_acc.columns or model_col_name not in df_acc.columns:
            return []
            
        reasoning_map = {}
        if os.path.exists(rea_file):
            try:
                df_rea = pd.read_csv(rea_file)
                if "Task" in df_rea.columns and model_col_name in df_rea.columns:
                    for _, row in df_rea.iterrows():
                        reasoning_map[str(row["Task"]).strip()] = str(row[model_col_name])
            except Exception:
                pass
                
        tasks_to_retry = []
        for _, row in df_acc.iterrows():
            task_name = str(row["Task"]).strip()
            if task_name in SUMMARY_ROW_NAMES:
                continue
                
            status_val = str(row[model_col_name]).strip()
            is_failed = (status_val != "CORRECT" and status_val != "nan" and status_val != "")
            
            if not is_failed:
                continue
                
            if retry_mode == "incorrect":
                tasks_to_retry.append(task_name)
            elif retry_mode == "insufficient":
                rea_val = reasoning_map.get(task_name, "").lower()
                if "insufficient data" in rea_val:
                    tasks_to_retry.append(task_name)
                    
        return tasks_to_retry
    except Exception as e:
        print(f"Erro ao buscar tasks para retry: {e}")
        return []

def save_entry_to_csv(filepath: str, task_name: str, model_col_name: str, value: str, append: bool):
    """
    Salva ou anexa uma linha em um arquivo CSV de forma idempotente, mantendo linhas de resumo ao final.
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df_new = pd.DataFrame({
        "Task": [task_name],
        model_col_name: [value]
    })
    
    if append and os.path.exists(filepath):
        try:
            df_existing = pd.read_csv(filepath)
            if model_col_name not in df_existing.columns:
                df_existing[model_col_name] = pd.NA
                
            if task_name in df_existing["Task"].values:
                df_existing.loc[df_existing["Task"] == task_name, model_col_name] = value
            else:
                # Se não é uma linha de resumo, insere antes de quaisquer linhas de resumo já existentes
                if task_name not in SUMMARY_ROW_NAMES:
                    is_summary = df_existing["Task"].isin(SUMMARY_ROW_NAMES)
                    task_rows = df_existing[~is_summary]
                    summary_df = df_existing[is_summary]
                    df_existing = pd.concat([task_rows, df_new, summary_df], ignore_index=True)
                else:
                    df_existing = pd.concat([df_existing, df_new], ignore_index=True)
                    
            df_existing.to_csv(filepath, index=False)
        except Exception as e:
            print(f"Erro ao salvar no CSV ({filepath}): {e}")
    else:
        df_new.to_csv(filepath, index=False)

def save_task_to_split_spreadsheets(base_filename: str, task_name: str, result: dict, append: bool):
    """
    Salva os dados de uma única task nos 5 arquivos CSV separados dentro da pasta Results:
      1. <nome>_accuracy.csv -> Status de acerto (CORRECT / INCORRECT)
      2. <nome>_tokens.csv   -> Detalhamento de tokens usados
      3. <nome>_reasoning.csv-> Apenas o resumo do raciocínio
      4. <nome>_grids.csv    -> Apenas a matriz / grid predita
      5. <nome>_times.csv    -> Detalhamento de tempos
    """
    model_col_name = os.getenv("GEMMA_MODEL", "AI_Model")
    dir_path, base = resolve_spreadsheet_paths(base_filename)
    
    # 1. Accuracy
    acc_file = os.path.join(dir_path, f"{base}_accuracy.csv")
    save_entry_to_csv(acc_file, task_name, model_col_name, result.get("status", "UNKNOWN"), append)
    
    # 2. Tokens
    tok_file = os.path.join(dir_path, f"{base}_tokens.csv")
    tok_str = format_tokens_string(result.get("tokens", {}))
    save_entry_to_csv(tok_file, task_name, model_col_name, tok_str, append)
    
    # 3. Reasoning
    rea_file = os.path.join(dir_path, f"{base}_reasoning.csv")
    save_entry_to_csv(rea_file, task_name, model_col_name, result.get("reasoning", ""), append)
    
    # 4. Grids
    grid_file = os.path.join(dir_path, f"{base}_grids.csv")
    save_entry_to_csv(grid_file, task_name, model_col_name, result.get("grid", ""), append)
    
    # 5. Times
    time_file = os.path.join(dir_path, f"{base}_times.csv")
    time_str = format_time_string(result.get("timing", {}))
    save_entry_to_csv(time_file, task_name, model_col_name, time_str, append)
    
    print(f"[+] Dados salvos em {dir_path}/ ({base}_accuracy, _tokens, _reasoning, _grids, _times.csv)")

def save_batch_summary_to_split_spreadsheets(
    base_filename: str,
    total_tasks: int,
    correct_tasks: int,
    batch_timing: dict,
    batch_tokens: dict
):
    """
    Adiciona/atualiza a linha final de resumo do batch nas planilhas apropriadas,
    calculando a acurácia global com base em todas as tasks do arquivo.
    """
    model_col_name = os.getenv("GEMMA_MODEL", "AI_Model")
    dir_path, base = resolve_spreadsheet_paths(base_filename)
    
    # 1. Accuracy - Calcula com base em todas as tasks da planilha para refletir o total acumulado
    acc_file = os.path.join(dir_path, f"{base}_accuracy.csv")
    global_total = total_tasks
    global_correct = correct_tasks
    if os.path.exists(acc_file):
        try:
            df = pd.read_csv(acc_file)
            if "Task" in df.columns and model_col_name in df.columns:
                valid_rows = df[~df["Task"].isin(SUMMARY_ROW_NAMES)]
                non_empty = valid_rows[valid_rows[model_col_name].notna() & (valid_rows[model_col_name] != "") & (valid_rows[model_col_name] != "nan")]
                if len(non_empty) > 0:
                    global_total = len(non_empty)
                    global_correct = len(non_empty[non_empty[model_col_name] == "CORRECT"])
        except Exception:
            pass
            
    acc_pct = (global_correct / global_total * 100) if global_total > 0 else 0.0
    acc_summary = f"{acc_pct:.2f}% ({global_correct}/{global_total})"
    save_entry_to_csv(acc_file, "Batch Accuracy", model_col_name, acc_summary, True)
    
    # 2. Tokens
    tok_file = os.path.join(dir_path, f"{base}_tokens.csv")
    tok_summary = format_tokens_string(batch_tokens)
    save_entry_to_csv(tok_file, "Tokens do Batch", model_col_name, tok_summary, True)
    
    # 3. Times
    time_file = os.path.join(dir_path, f"{base}_times.csv")
    time_summary = format_time_string(batch_timing)
    save_entry_to_csv(time_file, "Tempo do Batch", model_col_name, time_summary, True)
    
    print(f"[+] Resumo do Batch atualizado em {dir_path}/ ({base}_*.csv)!")