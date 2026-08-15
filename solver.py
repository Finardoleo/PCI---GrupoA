import json
import re
from typing import Optional
from llmhandler import generate_text
from utils import load_json

def grid_to_text(grid):
    return "\n".join(" ".join(str(x) for x in row) for row in grid)

def build_prompt(task: dict) -> str:
    train = task.get("train", [])
    test = task.get("test", [])
    
    # Prompt focado em concisão extrema para evitar estouro de tokens
    s = (
        "You are an expert puzzle solver for the ARC dataset.\n"
        "CRITICAL RULES:\n"
        "1. BE EXTREMELY CONCISE. DO NOT write long, exhaustive coordinate checks.\n"
        "2. Think briefly (max 5 sentences), then IMMEDIATELY output the final JSON.\n"
        "3. Output format must be EXACTLY like this block:\n"
        "```json\n"
        "{\n"
        "  \"reasoning_summary\": \"Very short rule explanation.\",\n"
        "  \"prediction\": [[0, 0], [0, 0]]\n"
        "}\n"
        "```\n\n"
    )

    if train:
        s += "### TRAINING EXAMPLES ###\n"
        for i, ex in enumerate(train):
            s += f"Example {i+1} Input:\n{grid_to_text(ex['input'])}\n"
            s += f"Example {i+1} Output:\n{grid_to_text(ex['output'])}\n\n"

    if test:
        s += "### TEST INPUT ###\n"
        s += f"{grid_to_text(test[0]['input'])}\n\n"

    s += "Now, briefly state the rule and provide the JSON."
    return s

def extract_json_from_text(text: str) -> Optional[dict]:
    # Tentativa 1: Parsear direto (se a API retornar limpo)
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Tentativa 2: Extrair bloco JSON via Regex
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
            
    # Tentativa 3 (O PLANO B SALVADOR): Extrair as matrizes soltas no texto
    # Essa regex vai caçar as respostas que o Gemma solta como "Row 1: 8 8 0 0 1"
    rows = []
    for line in text.split('\n'):
        line = line.strip()
        # Remove a sujeira "Row 0:", "Row 1:", etc.
        line = re.sub(r"^(?:Row\s*\d+:?|\[|\])\s*", "", line, flags=re.IGNORECASE)
        
        # Se a linha sobrou apenas com números, espaços e vírgulas...
        if re.match(r"^[0-9\s\[\],]+$", line) and len(re.findall(r"\d", line)) > 0:
            # Pega todos os dígitos soltos
            digits = [int(d) for d in re.findall(r"\d+", line)]
            
            # Se tiver mais de 1 número, assumimos que é uma linha da matriz ARC
            if len(digits) > 1: 
                rows.append(digits)
    
    if rows:
        return {
            "prediction": rows, 
            "reasoning_summary": "Recuperado via Regex de Fallback (O modelo ignorou o JSON, mas acertou a matriz no texto livre)."
        }

    return None

def normalize_grid(g):
    if not g:
        return []
    if isinstance(g, list):
        out = []
        for row in g:
            if isinstance(row, list):
                out.append([int(v) for v in row])
            elif isinstance(row, str) and row.isdigit():
                out.append([int(c) for c in row])
        return out
    return []

def solve_task_file(path, num_votes=3):
    task = load_json(path)
    prompt = build_prompt(task)
    
    predictions_counter = {}
    reasoning_map = {}
    
    print(f"Buscando {num_votes} soluções do modelo...")
    
    for i in range(num_votes):
        try:
            # Temperatura em 0.6 para viabilizar caminhos lógicos diferentes
            raw = generate_text(prompt, temperature=0.6, max_tokens=4096)

            # --- ADICIONE ESTE BLOCO DE PRINT PARA O DEBUG ---
            print(f"\n--- RAW OUTPUT TENTATIVA {i+1} ---")
            print(raw)
            print("-----------------------------------\n")
            # -------------------------------------------------
            
            parsed = extract_json_from_text(raw)
            
            if parsed and "prediction" in parsed:
                pred = parsed["prediction"]
                pred_norm = normalize_grid(pred)
                
                if not pred_norm:
                    continue
                
                # Tupla para viabilizar hash no dicionário
                pred_tuple = tuple(tuple(row) for row in pred_norm)
                predictions_counter[pred_tuple] = predictions_counter.get(pred_tuple, 0) + 1
                
                if pred_tuple not in reasoning_map:
                    reasoning_map[pred_tuple] = parsed.get("reasoning_summary", "(Sem resumo)")
                    
        except Exception as e:
            print(f"Erro na tentativa {i+1}: {e}")
            continue

    if not predictions_counter:
        return {
            "prediction": [], 
            "reasoning": "O modelo falhou em gerar um JSON válido em todas as tentativas.", 
            "correct": False,
            "confidence": f"0/{num_votes}"
        }

    # Calcula a Moda
    best_pred_tuple = max(predictions_counter, key=predictions_counter.get)
    max_votes = predictions_counter[best_pred_tuple]
    
    final_prediction = [list(row) for row in best_pred_tuple]
    final_reasoning = reasoning_map[best_pred_tuple]

    correct = None
    test = task.get("test", [])
    
    if test and "output" in test[0]:
        expected = normalize_grid(test[0]["output"])
        correct = final_prediction == expected

    return {
        "prediction": final_prediction, 
        "reasoning": final_reasoning, 
        "correct": correct,
        "confidence": f"{max_votes}/{num_votes} votos"
    }