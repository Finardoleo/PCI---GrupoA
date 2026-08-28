import argparse
import os
import json
import uuid
import random
import glob
from pathlib import Path
import pandas as pd
from typing import Set, Tuple, List, Dict

from transforms import (
    build_composed_transformation,
    generate_color_mapping,
    format_color_map_description
)

CATEGORY_FOLDERS = ["Rotation", "Reflexion", "Coloration", "Merged"]

def ensure_directories(output_dir: str):
    """Cria a pasta New Tasks e as 4 subpastas de categorias."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    for cat in CATEGORY_FOLDERS:
        (out_path / cat).mkdir(parents=True, exist_ok=True)

def determine_category(in_families: List[str], out_families: List[str]) -> str:
    """
    Determina a pasta de destino com base nas famílias de transformações ativas.
    """
    active_families = set(f for f in (in_families + out_families) if f != "Identity")
    
    if not active_families:
        return "Rotation"
    elif len(active_families) == 1:
        fam = next(iter(active_families))
        if fam in CATEGORY_FOLDERS:
            return fam
        return "Merged"
    else:
        return "Merged"

def load_existing_metadata(csv_path: str) -> Tuple[Set[Tuple[str, str, str]], Set[str]]:
    """
    Carrega combinações já existentes (Original_Task, Input_Transformation, Output_Transformation)
    e conjunto de IDs já utilizados para evitar duplicações.
    """
    if not os.path.exists(csv_path):
        return set(), set()
        
    try:
        df = pd.read_csv(csv_path)
        required_cols = ["New_Task_ID", "Original_Task", "Input_Transformation", "Output_Transformation"]
        if not all(col in df.columns for col in required_cols):
            return set(), set()
            
        existing_combos = set()
        existing_ids = set(df["New_Task_ID"].astype(str).str.strip())
        
        for _, row in df.iterrows():
            combo = (
                str(row["Original_Task"]).strip(),
                str(row["Input_Transformation"]).strip(),
                str(row["Output_Transformation"]).strip()
            )
            existing_combos.add(combo)
            
        return existing_combos, existing_ids
    except Exception as e:
        print(f"Aviso ao carregar metadata existente: {e}")
        return set(), set()

def append_to_metadata_csv(csv_path: str, new_id: str, orig_task: str, in_desc: str, out_desc: str):
    """Adiciona a nova task gerada ao arquivo CSV de metadados."""
    df_new = pd.DataFrame([{
        "New_Task_ID": new_id,
        "Original_Task": orig_task,
        "Input_Transformation": in_desc,
        "Output_Transformation": out_desc
    }])
    
    if os.path.exists(csv_path):
        df_new.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df_new.to_csv(csv_path, index=False)

def generate_unique_id(existing_ids: Set[str], data_dir: str = "data", output_dir: str = "New Tasks") -> str:
    """Gera um ID hexadecimal de 8 caracteres único que ainda não exista."""
    while True:
        candidate = uuid.uuid4().hex[:8]
        if candidate in existing_ids:
            continue
            
        # Verifica se por acaso já existe como arquivo .json
        if glob.glob(f"{data_dir}/**/{candidate}.json", recursive=True):
            continue
        if glob.glob(f"{output_dir}/**/{candidate}.json", recursive=True):
            continue
            
        existing_ids.add(candidate)
        return candidate

def transform_task(
    task_data: dict,
    in_choice: str,
    out_choice: str,
    same_transform: bool = False
) -> Tuple[dict, str, str, str]:
    """
    Aplica as transformações no input e output de uma task.
    Se same_transform for True ou in_choice == out_choice (diferente de random/merged),
    aplica EXATAMENTE a mesma transformação atômica/composta para ambos input e output.
    Retorna (novo_task_data, categoria, in_desc_final, out_desc_final).
    """
    if same_transform or (in_choice == out_choice and in_choice not in ['random', 'merged']):
        trans_desc, trans_fams, trans_func = build_composed_transformation(in_choice)
        in_desc, in_fams, in_func = trans_desc, trans_fams, trans_func
        out_desc, out_fams, out_func = trans_desc, trans_fams, trans_func
    else:
        in_desc, in_fams, in_func = build_composed_transformation(in_choice)
        out_desc, out_fams, out_func = build_composed_transformation(out_choice)
    
    category = determine_category(in_fams, out_fams)
    
    # Gera mapeamento de cores se alguma das transformações utilizar coloração
    needs_color = ("Coloration" in in_fams) or ("Coloration" in out_fams)
    color_map = generate_color_mapping(task_data) if needs_color else {}
    
    # Formata a descrição da transformação de cor se ela ocorreu
    color_desc_str = format_color_map_description(color_map)
    final_in_desc = in_desc.replace("color_permute", color_desc_str)
    final_out_desc = out_desc.replace("color_permute", color_desc_str)
    
    new_task = {"train": [], "test": []}
    
    for split in ["train", "test"]:
        for pair in task_data.get(split, []):
            transformed_pair = {}
            if "input" in pair:
                transformed_pair["input"] = in_func(pair["input"], color_map=color_map)
            if "output" in pair:
                transformed_pair["output"] = out_func(pair["output"], color_map=color_map)
            new_task[split].append(transformed_pair)
            
    return new_task, category, final_in_desc, final_out_desc

def collect_source_tasks(data_dir: str = "data") -> List[str]:
    """Coleta todos os arquivos JSON originais na pasta data."""
    tasks = glob.glob(f"{data_dir}/**/*.json", recursive=True)
    unique_tasks = sorted(list(dict.fromkeys(tasks)))
    return [t.replace("\\", "/") for t in unique_tasks]

def run_generator(
    data_dir: str = "data",
    output_dir: str = "New Tasks",
    input_transform: str = "random",
    output_transform: str = "random",
    num_tasks: str = "10",
    seed: int = None
):
    if seed is not None:
        random.seed(seed)
        
    ensure_directories(output_dir)
    metadata_csv = os.path.join(output_dir, "transformed_tasks.csv")
    existing_combos, existing_ids = load_existing_metadata(metadata_csv)
    
    all_source_tasks = collect_source_tasks(data_dir)
    if not all_source_tasks:
        print(f"[!] Nenhuma task encontrada em '{data_dir}'.")
        return
        
    # Seleção das tasks originais
    if str(num_tasks).strip().lower() == "all":
        selected_tasks = all_source_tasks
        print(f"[+] Modo ALL selecionado: Processando todas as {len(selected_tasks)} tasks originais.")
    else:
        try:
            n = int(num_tasks)
            n = min(n, len(all_source_tasks))
            selected_tasks = random.sample(all_source_tasks, n)
            print(f"[+] Selecionadas {len(selected_tasks)} tasks aleatórias (sem repetição).")
        except ValueError:
            print(f"[!] Valor inválido para num_tasks: {num_tasks}. Usando 10.")
            selected_tasks = random.sample(all_source_tasks, min(10, len(all_source_tasks)))
            
    generated_count = 0
    skipped_duplicates = 0
    
    print(f"[+] Iniciando geração de novas tasks...")
    print(f"    Transformação Input: {input_transform}")
    print(f"    Transformação Output: {output_transform}")
    print(f"    Diretório de Saída: '{output_dir}'")
    print(f"    Metadados: '{metadata_csv}'\n")
    
    for i, orig_path in enumerate(selected_tasks):
        orig_filename = Path(orig_path).name
        
        try:
            with open(orig_path, 'r', encoding='utf-8') as f:
                orig_data = json.load(f)
        except Exception as e:
            print(f"[!] Erro ao carregar '{orig_path}': {e}")
            continue
            
        # Tenta gerar uma transformação única (até 15 tentativas para evitar duplicatas exatas)
        success = False
        is_same = (input_transform == output_transform and input_transform not in ['random', 'merged'])
        for attempt in range(15):
            new_task_data, category, in_desc, out_desc = transform_task(
                orig_data,
                in_choice=input_transform,
                out_choice=output_transform,
                same_transform=is_same
            )
            
            combo = (orig_filename, in_desc, out_desc)
            if combo not in existing_combos:
                existing_combos.add(combo)
                new_id = generate_unique_id(existing_ids, data_dir, output_dir)
                
                # Salva o arquivo JSON na subpasta de categoria correspondente
                target_json_path = os.path.join(output_dir, category, f"{new_id}.json")
                with open(target_json_path, 'w', encoding='utf-8') as out_f:
                    json.dump(new_task_data, out_f, indent=2)
                    
                # Registra no CSV de metadados
                append_to_metadata_csv(metadata_csv, new_id, orig_filename, in_desc, out_desc)
                
                print(f"[{i+1}/{len(selected_tasks)}] Gerada Task '{new_id}' em '{category}/' (Original: {orig_filename})")
                print(f"    Input:  {in_desc}")
                print(f"    Output: {out_desc}")
                
                generated_count += 1
                success = True
                break
                
        if not success:
            print(f"[-] [{i+1}/{len(selected_tasks)}] Task '{orig_filename}' pulada: todas as transformações tentadas já existem no CSV.")
            skipped_duplicates += 1
            
    print(f"\n========================================")
    print(f"[+] GERAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"    Novas Tasks Criadas: {generated_count}")
    print(f"    Tasks Puladas (já existentes): {skipped_duplicates}")
    print(f"    CSV de Metadados: {metadata_csv}")
    print(f"========================================\n")

def main():
    parser = argparse.ArgumentParser(description="ARC-AGI Task Generator (2D Transformations)")
    parser.add_argument("--input-transform", choices=['identity', 'rotation', 'reflection', 'coloration', 'merged', 'random'], 
                        default='random', help="Transformação aplicada aos inputs (padrão: random)")
    parser.add_argument("--output-transform", choices=['identity', 'rotation', 'reflection', 'coloration', 'merged', 'random'], 
                        default='random', help="Transformação aplicada aos outputs (padrão: random)")
    parser.add_argument("--transform", choices=['identity', 'rotation', 'reflection', 'coloration', 'merged', 'random'], 
                        default=None, help="Aplica a mesma transformação a ambos input e output")
    parser.add_argument("--num-tasks", default="10", 
                        help="Número de tasks originais para transformar (ex: 10, 50) ou 'all' para todas (padrão: 10)")
    parser.add_argument("--data-dir", default="data", 
                        help="Diretório onde estão os JSONs originais (padrão: data)")
    parser.add_argument("--output-dir", default="New Tasks", 
                        help="Diretório onde as novas tasks e o CSV serão salvos (padrão: New Tasks)")
    parser.add_argument("--seed", type=int, default=None, 
                        help="Seed aleatório opcional para reproducibilidade")
    
    args = parser.parse_args()
    
    in_t = args.transform if args.transform else args.input_transform
    out_t = args.transform if args.transform else args.output_transform
    
    run_generator(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        input_transform=in_t,
        output_transform=out_t,
        num_tasks=args.num_tasks,
        seed=args.seed
    )

if __name__ == "__main__":
    main()
