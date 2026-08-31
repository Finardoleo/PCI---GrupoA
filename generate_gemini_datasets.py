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

def run_gemini_generation():
    print("=================================================================")
    print("  INICIANDO GERAÇÃO DE NOVAS TASKS PARA O GEMINI 3.5 FLASH LITE")
    print("=================================================================")

    # 1. Obter lista de tasks acertadas pelo Gemini 3.5 Flash Lite
    acc_csv = "Results/Gemini_3.5_Flash_Lite/Training Data Set/train_results_accuracy.csv"
    if not os.path.exists(acc_csv):
        raise FileNotFoundError(f"Planilha de acurácia não encontrada: {acc_csv}")

    df_acc = pd.read_csv(acc_csv)
    col_task = df_acc.columns[0]
    col_status = df_acc.columns[1]

    is_task_row = ~df_acc[col_task].astype(str).str.startswith("[+]") & ~df_acc[col_task].astype(str).str.startswith("Batch")
    df_tasks = df_acc[is_task_row]
    correct_df = df_tasks[df_tasks[col_status].astype(str).str.strip().str.upper() == "CORRECT"]

    correct_filenames = [os.path.basename(str(x).strip()) for x in correct_df[col_task]]
    correct_filenames = [x if x.endswith(".json") else f"{x}.json" for x in correct_filenames]
    correct_filenames = sorted(list(dict.fromkeys(correct_filenames)))

    print(f"[+] Total de tasks CORRECT identificadas para Gemini: {len(correct_filenames)}")
    assert len(correct_filenames) == 270, f"Esperado 270 tasks corretas, encontrado {len(correct_filenames)}"

    # 2. Criar e copiar para pasta Answered Correctly Training Tasks do Gemini
    gemini_correct_dir = "Results/Gemini_3.5_Flash_Lite/Training Data Set/Answered Correctly Training Tasks"
    os.makedirs(gemini_correct_dir, exist_ok=True)

    copied_correct = 0
    source_task_paths = []
    for fname in correct_filenames:
        src_p = os.path.join("data", "training", fname)
        if not os.path.exists(src_p):
            src_p = os.path.join("data", "evaluation", fname)
        if not os.path.exists(src_p):
            print(f"[!] Aviso: task {fname} não encontrada em data/")
            continue
        dest_p = os.path.join(gemini_correct_dir, fname)
        shutil.copy2(src_p, dest_p)
        source_task_paths.append(src_p)
        copied_correct += 1

    print(f"[+] Copiadas {copied_correct} tasks para '{gemini_correct_dir}'.")

    # 3. Arquivar tasks anteriores do Gemma em New Tasks/Gemma/
    gemma_archive_dir = "New Tasks/Gemma"
    os.makedirs(gemma_archive_dir, exist_ok=True)
    
    # Se ainda não foi arquivado, move/copia
    for cat in ["Rotation", "Reflexion", "Coloration", "Merged"]:
        cat_src = os.path.join("New Tasks", cat)
        cat_dst = os.path.join(gemma_archive_dir, cat)
        if os.path.exists(cat_src) and not os.path.exists(cat_dst):
            shutil.copytree(cat_src, cat_dst)
            print(f"[+] Arquivo do Gemma copiado: '{cat_src}' -> '{cat_dst}'")

    if os.path.exists("New Tasks/transformed_tasks.csv") and not os.path.exists(os.path.join(gemma_archive_dir, "transformed_tasks.csv")):
        shutil.copy2("New Tasks/transformed_tasks.csv", os.path.join(gemma_archive_dir, "transformed_tasks.csv"))
        print(f"[+] Metadata do Gemma arquivado em '{gemma_archive_dir}/transformed_tasks.csv'.")

    # 4. Limpar pastas ativas em New Tasks/ para receber o novo dataset do Gemini
    for cat in ["Rotation", "Reflexion", "Coloration", "Merged"]:
        target_dir = os.path.join("New Tasks", cat)
        os.makedirs(target_dir, exist_ok=True)
        # Limpa arquivos .json existentes na raiz da categoria
        for old_json in glob.glob(f"{target_dir}/*.json"):
            os.remove(old_json)
        # Limpa subpasta Different Input-Output se houver
        diff_dir = os.path.join(target_dir, "Different Input-Output")
        if os.path.exists(diff_dir):
            shutil.rmtree(diff_dir)

    # Coleta todos os IDs existentes para evitar colisões
    all_existing_ids = set()
    for f in glob.glob("**/*.json", recursive=True):
        tid = os.path.splitext(os.path.basename(f))[0]
        all_existing_ids.add(tid)

    def generate_new_unique_id():
        while True:
            candidate = uuid.uuid4().hex[:8]
            if candidate not in all_existing_ids:
                all_existing_ids.add(candidate)
                return candidate

    rotation_records = []
    reflection_records = []
    coloration_records = []
    merged_records = []

    print("\n[+] Gerando novas tasks a partir das 270 acertadas pelo Gemini...")

    for i, src_p in enumerate(source_task_paths):
        orig_name = os.path.basename(src_p)
        with open(src_p, 'r', encoding='utf-8') as f:
            task_data = json.load(f)

        # --- A. ROTAÇÃO (Input == Output idênticos) ---
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
        
        rot_id = generate_new_unique_id()
        with open(f"New Tasks/Rotation/{rot_id}.json", 'w', encoding='utf-8') as out_f:
            json.dump(rot_task, out_f, indent=2)
        rotation_records.append({
            "New_Task_ID": rot_id,
            "Original_Task": orig_name,
            "Input_Transformation": rot_name,
            "Output_Transformation": rot_name
        })

        # --- B. REFLEXÃO (Input == Output idênticos) ---
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

        ref_id = generate_new_unique_id()
        with open(f"New Tasks/Reflexion/{ref_id}.json", 'w', encoding='utf-8') as out_f:
            json.dump(ref_task, out_f, indent=2)
        reflection_records.append({
            "New_Task_ID": ref_id,
            "Original_Task": orig_name,
            "Input_Transformation": ref_name,
            "Output_Transformation": ref_name
        })

        # --- C. COLORAÇÃO (Input == Output idênticos, com suporte à cor 0) ---
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

        col_id = generate_new_unique_id()
        with open(f"New Tasks/Coloration/{col_id}.json", 'w', encoding='utf-8') as out_f:
            json.dump(col_task, out_f, indent=2)
        coloration_records.append({
            "New_Task_ID": col_id,
            "Original_Task": orig_name,
            "Input_Transformation": color_desc,
            "Output_Transformation": color_desc
        })

        # --- D. MERGED (2 variações compostas com transformações distintas em input e output) ---
        for var_idx in range(2):
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

            merged_id = generate_new_unique_id()
            with open(f"New Tasks/Merged/{merged_id}.json", 'w', encoding='utf-8') as out_f:
                json.dump(merged_task, out_f, indent=2)
            merged_records.append({
                "New_Task_ID": merged_id,
                "Original_Task": orig_name,
                "Input_Transformation": final_in_desc_m,
                "Output_Transformation": final_out_desc_m
            })

    print(f"\n[+] Tasks geradas com sucesso:")
    print(f"    - Rotação:   {len(rotation_records)} tasks (100% in == out)")
    print(f"    - Reflexão:  {len(reflection_records)} tasks (100% in == out)")
    print(f"    - Coloração: {len(coloration_records)} tasks (100% in == out)")
    print(f"    - Merged:    {len(merged_records)} tasks (2 por problema original)")

    # 5. Salvar New Tasks/transformed_tasks.csv ordenado:
    # Rotação (270) -> Reflexão (270) -> Coloração (270) -> Merged (540)
    all_gemini_records = rotation_records + reflection_records + coloration_records + merged_records
    df_gemini_meta = pd.DataFrame(all_gemini_records)
    
    meta_path = "New Tasks/transformed_tasks.csv"
    df_gemini_meta.to_csv(meta_path, index=False)
    print(f"[+] Metadados salvos em '{meta_path}' ({len(df_gemini_meta)} registros).")

    # Também espelhar cópia em New Tasks/Gemini/ para redundância e clareza
    gemini_explicit_dir = "New Tasks/Gemini"
    os.makedirs(gemini_explicit_dir, exist_ok=True)
    df_gemini_meta.to_csv(os.path.join(gemini_explicit_dir, "transformed_tasks.csv"), index=False)
    for cat in ["Rotation", "Reflexion", "Coloration", "Merged"]:
        dst = os.path.join(gemini_explicit_dir, cat)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join("New Tasks", cat), dst)
    print(f"[+] Cópia espelhada salva em '{gemini_explicit_dir}/'.")

    print("\n=================================================================")
    print("  VERIFICAÇÃO FINAL")
    print("=================================================================")
    rot_cnt = len(glob.glob("New Tasks/Rotation/*.json"))
    ref_cnt = len(glob.glob("New Tasks/Reflexion/*.json"))
    col_cnt = len(glob.glob("New Tasks/Coloration/*.json"))
    merg_cnt = len(glob.glob("New Tasks/Merged/*.json"))

    print(f"New Tasks/Rotation:   {rot_cnt} JSONs")
    print(f"New Tasks/Reflexion:  {ref_cnt} JSONs")
    print(f"New Tasks/Coloration: {col_cnt} JSONs")
    print(f"New Tasks/Merged:     {merg_cnt} JSONs")
    print(f"Total de Novas Tasks para o Gemini: {rot_cnt + ref_cnt + col_cnt + merg_cnt}")
    print("=================================================================\n")

if __name__ == "__main__":
    run_gemini_generation()
