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
    REFLECTION_TRANSFORMS
)

def run_restructuring():
    print("=================================================================")
    print("  INICIANDO REESTRUTURAÇÃO DAS TASKS DE ROTAÇÃO E REFLEXÃO")
    print("=================================================================")

    # 1. Carregar metadata atual
    meta_path = "New Tasks/transformed_tasks.csv"
    df_meta = pd.read_csv(meta_path)
    print(f"[+] Carregados {len(df_meta)} registros de metadados em '{meta_path}'.")

    # Mapeamentos rápidos
    meta_by_id = {}
    for _, row in df_meta.iterrows():
        tid = str(row["New_Task_ID"]).strip()
        meta_by_id[tid] = {
            "New_Task_ID": tid,
            "Original_Task": str(row["Original_Task"]).strip(),
            "Input_Transformation": str(row["Input_Transformation"]).strip(),
            "Output_Transformation": str(row["Output_Transformation"]).strip()
        }

    # 2. Criar pastas 'Different Input-Output'
    rot_diff_dir = "New Tasks/Rotation/Different Input-Output"
    ref_diff_dir = "New Tasks/Reflexion/Different Input-Output"
    os.makedirs(rot_diff_dir, exist_ok=True)
    os.makedirs(ref_diff_dir, exist_ok=True)

    # Identificar e mover arquivos com transformações diferentes
    rot_moved = []
    rot_kept = []
    for f in glob.glob("New Tasks/Rotation/*.json"):
        tid = os.path.splitext(os.path.basename(f))[0]
        meta = meta_by_id.get(tid)
        if meta and meta["Input_Transformation"] != meta["Output_Transformation"]:
            dest = os.path.join(rot_diff_dir, os.path.basename(f))
            shutil.move(f, dest)
            rot_moved.append(tid)
        else:
            rot_kept.append(tid)

    ref_moved = []
    ref_kept = []
    for f in glob.glob("New Tasks/Reflexion/*.json"):
        tid = os.path.splitext(os.path.basename(f))[0]
        meta = meta_by_id.get(tid)
        if meta and meta["Input_Transformation"] != meta["Output_Transformation"]:
            dest = os.path.join(ref_diff_dir, os.path.basename(f))
            shutil.move(f, dest)
            ref_moved.append(tid)
        else:
            ref_kept.append(tid)

    print(f"[+] [Rotation] Movidas {len(rot_moved)} tasks com in!=out para '{rot_diff_dir}'. Mantidas {len(rot_kept)} tasks.")
    print(f"[+] [Reflexion] Movidas {len(ref_moved)} tasks com in!=out para '{ref_diff_dir}'. Mantidas {len(ref_kept)} tasks.")

    # 3. Fazer backup e filtrar planilhas em Results/Gemma/
    for category_name, prefix, kept_ids in [
        ("Rotated Training Data Set", "rotated_train_results", rot_kept),
        ("Reflected Training Data Set", "reflected_train_results", ref_kept)
    ]:
        src_folder = f"Results/Gemma/{category_name}"
        dest_folder = f"Results/Gemma/{category_name}/Different Input-Output"
        os.makedirs(dest_folder, exist_ok=True)

        print(f"\n[+] Processando planilhas de '{src_folder}'...")
        kept_set = set(kept_ids)

        for suffix in ["_accuracy.csv", "_grids.csv", "_reasoning.csv", "_times.csv", "_tokens.csv"]:
            csv_name = f"{prefix}{suffix}"
            src_csv = os.path.join(src_folder, csv_name)
            dest_csv = os.path.join(dest_folder, csv_name)

            if os.path.exists(src_csv):
                # 1. Copiar original para Different Input-Output
                shutil.copy2(src_csv, dest_csv)
                print(f"    - Cópia criada: {dest_csv}")

                # 2. Filtrar linhas mantendo apenas tasks com transformações iguais
                df = pd.read_csv(src_csv)
                col_task = df.columns[0]
                
                # Separa linhas de resumo de lote (se houver)
                is_task_row = ~df[col_task].astype(str).str.startswith("[+]") & ~df[col_task].astype(str).str.startswith("Batch") & ~df[col_task].astype(str).str.startswith("Tempo do Batch") & ~df[col_task].astype(str).str.startswith("Tokens do Batch")
                df_tasks = df[is_task_row]
                
                # Identifica task_id
                df_filtered_tasks = df_tasks[df_tasks[col_task].apply(lambda x: os.path.splitext(str(x).strip())[0] in kept_set)]
                
                # Salva o arquivo filtrado no local original
                df_filtered_tasks.to_csv(src_csv, index=False)
                print(f"    - Filtrado '{src_csv}': mantidas {len(df_filtered_tasks)} linhas.")

    # 4. Gerar novas tasks com mesma transformação para todas as 304 Answered Correctly
    source_tasks_dir = "Results/Gemma/Training Data Set/Answered Correctly Training Tasks"
    source_files = sorted(glob.glob(f"{source_tasks_dir}/*.json"))
    print(f"\n[+] Coletadas {len(source_files)} tasks originais de '{source_tasks_dir}'.")

    # Mapear quais originais já estão cobertos pelos kept
    rot_covered_origs = {}
    for tid in rot_kept:
        m = meta_by_id.get(tid)
        if m:
            orig = m["Original_Task"]
            if orig not in rot_covered_origs:
                rot_covered_origs[orig] = tid
            else:
                # Se for duplicata do mesmo original, move a extra para different
                dup_file = f"New Tasks/Rotation/{tid}.json"
                if os.path.exists(dup_file):
                    shutil.move(dup_file, os.path.join(rot_diff_dir, f"{tid}.json"))
                    rot_moved.append(tid)

    ref_covered_origs = {}
    for tid in ref_kept:
        m = meta_by_id.get(tid)
        if m:
            orig = m["Original_Task"]
            if orig not in ref_covered_origs:
                ref_covered_origs[orig] = tid
            else:
                dup_file = f"New Tasks/Reflexion/{tid}.json"
                if os.path.exists(dup_file):
                    shutil.move(dup_file, os.path.join(ref_diff_dir, f"{tid}.json"))
                    ref_moved.append(tid)

    print(f"[+] Originais já cobertos com transformação idêntica:")
    print(f"    - Rotação: {len(rot_covered_origs)} / {len(source_files)}")
    print(f"    - Reflexão: {len(ref_covered_origs)} / {len(source_files)}")

    # Carregar todos os IDs existentes para evitar colisão de hash
    all_existing_ids = set(glob.glob("**/*.json", recursive=True))
    all_existing_ids = {os.path.splitext(os.path.basename(p))[0] for p in all_existing_ids}

    def generate_new_unique_id():
        while True:
            candidate = uuid.uuid4().hex[:8]
            if candidate not in all_existing_ids:
                all_existing_ids.add(candidate)
                return candidate

    new_rotation_records = []
    # Adicionar os mantidos em Rotation
    for orig, tid in rot_covered_origs.items():
        m = meta_by_id[tid]
        new_rotation_records.append({
            "New_Task_ID": tid,
            "Original_Task": orig,
            "Input_Transformation": m["Input_Transformation"],
            "Output_Transformation": m["Output_Transformation"]
        })

    # Gerar os que faltam em Rotation
    rot_generated_count = 0
    for src_p in source_files:
        orig_name = os.path.basename(src_p)
        if orig_name in rot_covered_origs:
            continue

        with open(src_p, 'r', encoding='utf-8') as f:
            task_data = json.load(f)

        # Escolhe UMA rotação aleatória para input e output
        rot_name, _, rot_func = random.choice(ROTATION_TRANSFORMS)
        new_task = {"train": [], "test": []}
        for split in ["train", "test"]:
            for pair in task_data.get(split, []):
                new_pair = {}
                if "input" in pair:
                    new_pair["input"] = rot_func(pair["input"])
                if "output" in pair:
                    new_pair["output"] = rot_func(pair["output"])
                new_task[split].append(new_pair)

        new_id = generate_new_unique_id()
        dest_json = f"New Tasks/Rotation/{new_id}.json"
        with open(dest_json, 'w', encoding='utf-8') as f:
            json.dump(new_task, f, indent=2)

        new_rotation_records.append({
            "New_Task_ID": new_id,
            "Original_Task": orig_name,
            "Input_Transformation": rot_name,
            "Output_Transformation": rot_name
        })
        rot_generated_count += 1

    print(f"[+] [Rotation] Geradas {rot_generated_count} novas tasks com rotação idêntica. Total ativo: {len(new_rotation_records)}")

    new_reflection_records = []
    # Adicionar os mantidos em Reflexion
    for orig, tid in ref_covered_origs.items():
        m = meta_by_id[tid]
        new_reflection_records.append({
            "New_Task_ID": tid,
            "Original_Task": orig,
            "Input_Transformation": m["Input_Transformation"],
            "Output_Transformation": m["Output_Transformation"]
        })

    # Gerar os que faltam em Reflexion
    ref_generated_count = 0
    for src_p in source_files:
        orig_name = os.path.basename(src_p)
        if orig_name in ref_covered_origs:
            continue

        with open(src_p, 'r', encoding='utf-8') as f:
            task_data = json.load(f)

        # Escolhe UMA reflexão aleatória para input e output
        ref_name, _, ref_func = random.choice(REFLECTION_TRANSFORMS)
        new_task = {"train": [], "test": []}
        for split in ["train", "test"]:
            for pair in task_data.get(split, []):
                new_pair = {}
                if "input" in pair:
                    new_pair["input"] = ref_func(pair["input"])
                if "output" in pair:
                    new_pair["output"] = ref_func(pair["output"])
                new_task[split].append(new_pair)

        new_id = generate_new_unique_id()
        dest_json = f"New Tasks/Reflexion/{new_id}.json"
        with open(dest_json, 'w', encoding='utf-8') as f:
            json.dump(new_task, f, indent=2)

        new_reflection_records.append({
            "New_Task_ID": new_id,
            "Original_Task": orig_name,
            "Input_Transformation": ref_name,
            "Output_Transformation": ref_name
        })
        ref_generated_count += 1

    print(f"[+] [Reflexion] Geradas {ref_generated_count} novas tasks com reflexão idêntica. Total ativo: {len(new_reflection_records)}")

    # 5. Coletar registros Merged intactos
    merged_ids = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob("New Tasks/Merged/*.json")]
    merged_records = []
    for tid in merged_ids:
        if tid in meta_by_id:
            merged_records.append(meta_by_id[tid])
    print(f"[+] [Merged] Mantidos {len(merged_records)} registros intactos.")

    # 6. Salvar metadados organizados em New Tasks/transformed_tasks.csv
    # Ordem solicitada: Rotação, depois Reflexão, depois Merged
    df_final_active = pd.DataFrame(new_rotation_records + new_reflection_records + merged_records)
    df_final_active.to_csv(meta_path, index=False)
    print(f"\n[+] 'New Tasks/transformed_tasks.csv' atualizado com {len(df_final_active)} registros ordenados (Rot: {len(new_rotation_records)}, Ref: {len(new_reflection_records)}, Merged: {len(merged_records)}).")

    # Salvar também histórico das tasks movidas em transformed_tasks_different.csv
    diff_records = []
    for tid in rot_moved + ref_moved:
        if tid in meta_by_id:
            diff_records.append(meta_by_id[tid])
    df_diff = pd.DataFrame(diff_records)
    df_diff.to_csv("New Tasks/transformed_tasks_different.csv", index=False)
    print(f"[+] Backup dos metadados das tasks movidas salvo em 'New Tasks/transformed_tasks_different.csv' ({len(df_diff)} registros).")

    print("\n=================================================================")
    print("  VERIFICAÇÃO FINAL DOS ARQUIVOS E PASTAS")
    print("=================================================================")
    rot_files = glob.glob("New Tasks/Rotation/*.json")
    ref_files = glob.glob("New Tasks/Reflexion/*.json")
    merg_files = glob.glob("New Tasks/Merged/*.json")
    rot_diff_files = glob.glob("New Tasks/Rotation/Different Input-Output/*.json")
    ref_diff_files = glob.glob("New Tasks/Reflexion/Different Input-Output/*.json")

    print(f"New Tasks/Rotation: {len(rot_files)} tasks (todas com in == out)")
    print(f"New Tasks/Rotation/Different Input-Output: {len(rot_diff_files)} tasks")
    print(f"New Tasks/Reflexion: {len(ref_files)} tasks (todas com in == out)")
    print(f"New Tasks/Reflexion/Different Input-Output: {len(ref_diff_files)} tasks")
    print(f"New Tasks/Merged: {len(merg_files)} tasks")
    print("=================================================================\n")

if __name__ == "__main__":
    run_restructuring()
