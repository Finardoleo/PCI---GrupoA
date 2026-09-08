import os
import glob
import json
import shutil
import random
import uuid
import pandas as pd
from pathlib import Path

from transforms import (
    ROTATION_TRANSFORMS,
    REFLECTION_TRANSFORMS,
    build_composed_transformation,
    generate_color_mapping,
    format_color_map_description,
    color_permute
)

def collect_all_existing_ids():
    all_ids = set()
    for f in glob.glob("**/*.json", recursive=True):
        tid = os.path.splitext(os.path.basename(f))[0]
        all_ids.add(tid)
    return all_ids

def generate_datasets_for_model(model_name: str, acc_csv_path: str, incorrect_dir: str, output_base_dir: str, existing_ids: set):
    print("\n" + "="*75)
    print(f"  GERANDO DATASETS DE TAREFAS INCORRETAS PARA: {model_name}")
    print("="*75)

    if not os.path.exists(acc_csv_path):
        raise FileNotFoundError(f"Planilha de acurácia não encontrada: {acc_csv_path}")

    df_acc = pd.read_csv(acc_csv_path)
    col_task = df_acc.columns[0]
    col_status = df_acc.columns[1]

    # Filtrar tasks INCORRECT
    is_task_row = ~df_acc[col_task].astype(str).str.startswith("[+]") & ~df_acc[col_task].astype(str).str.startswith("Batch")
    df_tasks = df_acc[is_task_row]
    
    def is_incorrect(val):
        s = str(val).strip().upper()
        return s in ["INCORRECT", "0", "0.0", "FALSE", "ERROU", "FAIL"]

    incorrect_df = df_tasks[df_tasks[col_status].apply(is_incorrect)]
    incorrect_filenames = [os.path.basename(str(x).strip()) for x in incorrect_df[col_task]]
    incorrect_filenames = [x if x.endswith(".json") else f"{x}.json" for x in incorrect_filenames]
    incorrect_filenames = sorted(list(dict.fromkeys(incorrect_filenames)))

    print(f"[+] Total de tasks INCORRECT identificadas: {len(incorrect_filenames)}")

    # Garantir pasta de tasks incorretas original
    os.makedirs(incorrect_dir, exist_ok=True)
    source_task_paths = []
    copied_count = 0

    for fname in incorrect_filenames:
        dest_p = os.path.join(incorrect_dir, fname)
        if not os.path.exists(dest_p):
            src_p = os.path.join("data", "training", fname)
            if not os.path.exists(src_p):
                src_p = os.path.join("data", "evaluation", fname)
            if os.path.exists(src_p):
                shutil.copy2(src_p, dest_p)
                copied_count += 1
            else:
                print(f"[!] Aviso: task {fname} não encontrada em data/")
                continue
        source_task_paths.append(dest_p)

    print(f"[+] Base original de incorretas garantida em: '{incorrect_dir}' ({len(source_task_paths)} arquivos).")

    # Preparar subpastas de saída
    for cat in ["Rotation", "Reflexion", "Coloration", "Merged"]:
        cat_dir = os.path.join(output_base_dir, cat)
        os.makedirs(cat_dir, exist_ok=True)
        for old_json in glob.glob(f"{cat_dir}/*.json"):
            os.remove(old_json)

    def get_unique_id():
        while True:
            cand = uuid.uuid4().hex[:8]
            if cand not in existing_ids:
                existing_ids.add(cand)
                return cand

    rotation_records = []
    reflection_records = []
    coloration_records = []
    merged_records = []

    for src_p in source_task_paths:
        orig_name = os.path.basename(src_p)
        with open(src_p, 'r', encoding='utf-8') as f:
            task_data = json.load(f)

        # 1. ROTAÇÃO (Input == Output)
        rot_name, _, rot_func = random.choice(ROTATION_TRANSFORMS)
        rot_task = {"train": [], "test": []}
        for split in ["train", "test"]:
            for pair in task_data.get(split, []):
                new_pair = {}
                if "input" in pair:
                    new_pair["input"] = rot_func(pair["input"])
                if "output" in pair:
                    new_pair["output"] = rot_func(pair["output"])
                rot_task[split].append(new_pair)

        rot_id = get_unique_id()
        with open(os.path.join(output_base_dir, "Rotation", f"{rot_id}.json"), 'w', encoding='utf-8') as out_f:
            json.dump(rot_task, out_f, indent=2)
        rotation_records.append({
            "New_Task_ID": rot_id,
            "Original_Task": orig_name,
            "Category": "Rotation",
            "Input_Transformation": rot_name,
            "Output_Transformation": rot_name
        })

        # 2. REFLEXÃO (Input == Output)
        ref_name, _, ref_func = random.choice(REFLECTION_TRANSFORMS)
        ref_task = {"train": [], "test": []}
        for split in ["train", "test"]:
            for pair in task_data.get(split, []):
                new_pair = {}
                if "input" in pair:
                    new_pair["input"] = ref_func(pair["input"])
                if "output" in pair:
                    new_pair["output"] = ref_func(pair["output"])
                ref_task[split].append(new_pair)

        ref_id = get_unique_id()
        with open(os.path.join(output_base_dir, "Reflexion", f"{ref_id}.json"), 'w', encoding='utf-8') as out_f:
            json.dump(ref_task, out_f, indent=2)
        reflection_records.append({
            "New_Task_ID": ref_id,
            "Original_Task": orig_name,
            "Category": "Reflexion",
            "Input_Transformation": ref_name,
            "Output_Transformation": ref_name
        })

        # 3. COLORAÇÃO (Input == Output com suporte à cor 0)
        include_zero = (random.random() < 0.65)
        color_map = generate_color_mapping(task_data, include_zero=include_zero)
        if not color_map:
            color_map = {1: 2, 2: 1} if not include_zero else {0: 1, 1: 0}
        color_desc = format_color_map_description(color_map)

        col_task = {"train": [], "test": []}
        for split in ["train", "test"]:
            for pair in task_data.get(split, []):
                new_pair = {}
                if "input" in pair:
                    new_pair["input"] = color_permute(pair["input"], color_map=color_map)
                if "output" in pair:
                    new_pair["output"] = color_permute(pair["output"], color_map=color_map)
                col_task[split].append(new_pair)

        col_id = get_unique_id()
        with open(os.path.join(output_base_dir, "Coloration", f"{col_id}.json"), 'w', encoding='utf-8') as out_f:
            json.dump(col_task, out_f, indent=2)
        coloration_records.append({
            "New_Task_ID": col_id,
            "Original_Task": orig_name,
            "Category": "Coloration",
            "Input_Transformation": color_desc,
            "Output_Transformation": color_desc
        })

        # 4. MERGED (2 variações com transformações compostas distintas)
        for _ in range(2):
            in_desc_m, in_fams, in_func_m = build_composed_transformation("merged")
            out_desc_m, out_fams, out_func_m = build_composed_transformation("merged")

            needs_color = ("Coloration" in in_fams) or ("Coloration" in out_fams)
            color_map_m = generate_color_mapping(task_data, include_zero=True) if needs_color else {}
            color_desc_m = format_color_map_description(color_map_m)

            final_in_desc_m = in_desc_m.replace("color_permute", color_desc_m)
            final_out_desc_m = out_desc_m.replace("color_permute", color_desc_m)

            merged_task = {"train": [], "test": []}
            for split in ["train", "test"]:
                for pair in task_data.get(split, []):
                    new_pair = {}
                    if "input" in pair:
                        new_pair["input"] = in_func_m(pair["input"], color_map=color_map_m)
                    if "output" in pair:
                        new_pair["output"] = out_func_m(pair["output"], color_map=color_map_m)
                    merged_task[split].append(new_pair)

            merged_id = get_unique_id()
            with open(os.path.join(output_base_dir, "Merged", f"{merged_id}.json"), 'w', encoding='utf-8') as out_f:
                json.dump(merged_task, out_f, indent=2)
            merged_records.append({
                "New_Task_ID": merged_id,
                "Original_Task": orig_name,
                "Category": "Merged",
                "Input_Transformation": final_in_desc_m,
                "Output_Transformation": final_out_desc_m
            })

    # Salvar metadata CSV
    all_records = rotation_records + reflection_records + coloration_records + merged_records
    df_meta = pd.DataFrame(all_records)
    meta_path = os.path.join(output_base_dir, "transformed_tasks.csv")
    df_meta.to_csv(meta_path, index=False)

    print(f"[+] Datasets gerados com sucesso em '{output_base_dir}':")
    print(f"    - Rotation:   {len(rotation_records)} tasks")
    print(f"    - Reflexion:  {len(reflection_records)} tasks")
    print(f"    - Coloration: {len(coloration_records)} tasks")
    print(f"    - Merged:     {len(merged_records)} tasks")
    print(f"    - Total:      {len(all_records)} tasks (Metadados: {meta_path})")

    return len(rotation_records), len(reflection_records), len(coloration_records), len(merged_records)

def main():
    existing_ids = collect_all_existing_ids()
    print(f"[+] Total de IDs existentes coletados para prevenir colisões: {len(existing_ids)}")

    # 1. Gemma 4 (31B-IT) - Incorretas (96 tasks)
    generate_datasets_for_model(
        model_name="Gemma 4 (31B-IT)",
        acc_csv_path="Results/Gemma/Training Data Set/train_results_accuracy.csv",
        incorrect_dir="Results/Gemma/Training Data Set/Answered Incorrectly Training Tasks",
        output_base_dir="New Tasks/Incorrect/Gemma",
        existing_ids=existing_ids
    )

    # 2. Gemini 3.5 Flash Lite - Incorretas (130 tasks)
    generate_datasets_for_model(
        model_name="Gemini 3.5 Flash Lite",
        acc_csv_path="Results/Gemini_3.5_Flash_Lite/Training Data Set/train_results_accuracy.csv",
        incorrect_dir="Results/Gemini_3.5_Flash_Lite/Training Data Set/Answered Incorrectly Training Tasks",
        output_base_dir="New Tasks/Incorrect/Gemini",
        existing_ids=existing_ids
    )

    print("\n" + "="*75)
    print("  TODOS OS DATASETS DE TASKS INCORRETAS FORAM GERADOS COM SUCESSO!")
    print("="*75)

if __name__ == "__main__":
    main()
