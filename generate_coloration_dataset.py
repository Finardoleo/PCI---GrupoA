import os
import glob
import json
import random
import uuid
import pandas as pd
from pathlib import Path

from transforms import (
    generate_color_mapping,
    format_color_map_description,
    color_permute
)

def run_coloration_generation():
    print("=================================================================")
    print("  GERANDO NOVO DATASET DE COLORAÇÃO (PERMUTAÇÃO DE CORES 1:1)")
    print("=================================================================")

    # 1. Carregar tarefas originais acertadas
    source_dir = "Results/Gemma/Training Data Set/Answered Correctly Training Tasks"
    source_files = sorted(glob.glob(f"{source_dir}/*.json"))
    print(f"[+] Coletadas {len(source_files)} tasks originais de '{source_dir}'.")
    assert len(source_files) == 304, f"Esperado 304 tasks, encontrado {len(source_files)}"

    # 2. Preparar pasta New Tasks/Coloration
    coloration_dir = "New Tasks/Coloration"
    os.makedirs(coloration_dir, exist_ok=True)
    
    # Limpar quaisquer arquivos JSON residuais em New Tasks/Coloration
    existing_in_col = glob.glob(f"{coloration_dir}/*.json")
    if existing_in_col:
        print(f"[!] Removendo {len(existing_in_col)} arquivos antigos residuais em '{coloration_dir}'.")
        for old_f in existing_in_col:
            os.remove(old_f)

    # 3. Coletar todos os IDs de tarefas existentes no workspace para garantir unicidade estrita
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

    coloration_records = []

    # 4. Processar cada uma das 304 tasks originais
    zero_permuted_count = 0
    for i, src_p in enumerate(source_files):
        orig_name = os.path.basename(src_p)
        with open(src_p, 'r', encoding='utf-8') as f:
            task_data = json.load(f)

        # Decide se inclui a cor 0 na permutação para esta task (~65% das tasks permutam o 0)
        include_zero = (random.random() < 0.65)
        color_map = generate_color_mapping(task_data, include_zero=include_zero)
        
        # Se não houver cores ativas para mudar (raríssimo), força um mapeamento
        if not color_map:
            color_map = {1: 2, 2: 1} if not include_zero else {0: 1, 1: 0}

        if 0 in color_map and color_map[0] != 0:
            zero_permuted_count += 1

        # Aplica a MESMA permutação em todos os inputs e outputs de treino e teste
        new_task = {"train": [], "test": []}
        for split in ["train", "test"]:
            for pair in task_data.get(split, []):
                new_pair = {}
                if "input" in pair:
                    new_pair["input"] = color_permute(pair["input"], color_map=color_map)
                if "output" in pair:
                    new_pair["output"] = color_permute(pair["output"], color_map=color_map)
                new_task[split].append(new_pair)

        # Descrição formatada da permutação de cor
        color_desc = format_color_map_description(color_map)

        new_id = generate_new_unique_id()
        dest_json = os.path.join(coloration_dir, f"{new_id}.json")
        with open(dest_json, 'w', encoding='utf-8') as out_f:
            json.dump(new_task, out_f, indent=2)

        coloration_records.append({
            "New_Task_ID": new_id,
            "Original_Task": orig_name,
            "Input_Transformation": color_desc,
            "Output_Transformation": color_desc
        })

    print(f"[+] Geradas com sucesso {len(coloration_records)} tasks de Coloração em '{coloration_dir}/'.")
    print(f"    - Tasks com a cor '0' permutada: {zero_permuted_count} / {len(coloration_records)}")
    print(f"    - Tasks com a cor '0' preservada: {len(coloration_records) - zero_permuted_count} / {len(coloration_records)}")

    # 5. Atualizar New Tasks/transformed_tasks.csv na ordem solicitada:
    # Rotação (304) -> Reflexão (304) -> PermutaçãoCor (304) -> Merged (591)
    meta_path = "New Tasks/transformed_tasks.csv"
    df_existing = pd.read_csv(meta_path)
    
    rot_records = df_existing.iloc[:304].to_dict('records')
    ref_records = df_existing.iloc[304:608].to_dict('records')
    merged_records = df_existing.iloc[608:].to_dict('records')

    print(f"[+] Verificação dos blocos existentes:")
    print(f"    - Rotação: {len(rot_records)} registros")
    print(f"    - Reflexão: {len(ref_records)} registros")
    print(f"    - Coloração (Novos): {len(coloration_records)} registros")
    print(f"    - Merged: {len(merged_records)} registros")

    all_ordered_records = rot_records + ref_records + coloration_records + merged_records
    df_final = pd.DataFrame(all_ordered_records)
    df_final.to_csv(meta_path, index=False)

    print(f"\n[+] 'New Tasks/transformed_tasks.csv' salvo com sucesso! Total de linhas: {len(df_final)}")

    # 6. Validação e Auditoria
    print("\n=================================================================")
    print("  AUDITORIA E VALIDAÇÃO DOS DADOS")
    print("=================================================================")
    rot_files = len(glob.glob("New Tasks/Rotation/*.json"))
    ref_files = len(glob.glob("New Tasks/Reflexion/*.json"))
    col_files = len(glob.glob("New Tasks/Coloration/*.json"))
    merg_files = len(glob.glob("New Tasks/Merged/*.json"))

    print(f"New Tasks/Rotation:   {rot_files} JSONs")
    print(f"New Tasks/Reflexion:  {ref_files} JSONs")
    print(f"New Tasks/Coloration: {col_files} JSONs")
    print(f"New Tasks/Merged:     {merg_files} JSONs")

    assert rot_files == 304, f"Rotation deveria ter 304, tem {rot_files}"
    assert ref_files == 304, f"Reflexion deveria ter 304, tem {ref_files}"
    assert col_files == 304, f"Coloration deveria ter 304, tem {col_files}"
    assert merg_files == 591, f"Merged deveria ter 591, tem {merg_files}"

    # Validar que todas as 304 de coloração possuem input == output
    col_slice = df_final.iloc[608:912]
    same_col = (col_slice['Input_Transformation'] == col_slice['Output_Transformation']).sum()
    assert same_col == 304, f"Nem todas as de coloração têm input==output: {same_col}/304"
    print(f"[+] Verificação de Igualdade Input-Output em Coloração: 304 / 304 (100% idênticos).")
    print("=================================================================\n")

if __name__ == "__main__":
    run_coloration_generation()
