import json
import re
from typing import Optional
from llmhandler import generate_chat

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def grid_to_text(grid):
    return "\n".join(" ".join(str(x) for x in row) for row in grid)

def build_reasoning_prompt(task: dict) -> str:
    train = task.get("train", [])
    test = task.get("test", [])
    
    # Prompt da Fase 1: Livre para pensar e raciocinar
    s = (
        "You are an expert puzzle solver for the ARC dataset.\n"
        "Analyze the following training examples and determine the underlying logical rule.\n"
        "Think step-by-step to figure out how the input grid transforms into the output grid.\n"
        "Apply your rule to the TEST INPUT to determine the final output grid.\n\n"
    )

    if train:
        s += "### TRAINING EXAMPLES ###\n"
        for i, ex in enumerate(train):
            s += f"Example {i+1} Input:\n{grid_to_text(ex['input'])}\n"
            s += f"Example {i+1} Output:\n{grid_to_text(ex['output'])}\n\n"

    if test:
        s += "### TEST INPUT ###\n"
        s += f"{grid_to_text(test[0]['input'])}\n\n"

    s += "What is the logical rule, and what is the exact final grid for the TEST INPUT?"
    return s

def extract_answer_from_text(text: str) -> Optional[dict]:
    # 1. Tentativa principal: Procurar as tags <prediction>
    m = re.search(r"<prediction>\s*(.*?)\s*</prediction>", text, re.IGNORECASE | re.DOTALL)
    if m:
        grid_text = m.group(1).strip()
        
        if re.match(r"^\d+$", grid_text):
            return {"prediction": [[int(grid_text)]], "reasoning_summary": "Escalar extraído da tag <prediction>."}
            
        rows = []
        for line in grid_text.split('\n'):
            line = line.strip()
            if re.match(r"^[0-9\s\[\],]+$", line) and len(re.findall(r"\d+", line)) > 0:
                digits = [int(d) for d in re.findall(r"\d+", line)]
                if digits:
                    rows.append(digits)
        if rows:
            return {"prediction": rows, "reasoning_summary": "Matriz extraída via tag <prediction>."}

    # 2. Nova Tentativa Flexível: Capturar "Output: X" EM QUALQUER LUGAR
    # Removi a âncora '$' que exigia que fosse no final do texto. 
    # Agora, se ele falar "Output: 1" no meio do texto, nós pegamos!
    m_out = re.search(r"(?:Output|Result|Final Matrix|should be):\s*(\d+)", text, re.IGNORECASE)
    if m_out:
        return {"prediction": [[int(m_out.group(1))]], "reasoning_summary": "Escalar extraído via texto livre."}

    # 3. Fallback Regex
    blocks = []
    current_block = []
    for line in text.split('\n'):
        line = line.strip()
        line = re.sub(r"^(?:Row\s*\d+:?|\[|\]|Output:?|Result:?)\s*", "", line, flags=re.IGNORECASE)
        
        if re.match(r"^[0-9\s\[\],]+$", line) and len(re.findall(r"\d+", line)) > 0:
            digits = [int(d) for d in re.findall(r"\d+", line)]
            if digits: 
                current_block.append(digits)
        else:
            if current_block:
                blocks.append(current_block)
                current_block = []
                
    if current_block:
        blocks.append(current_block)
        
    if blocks:
        return {"prediction": blocks[-1], "reasoning_summary": "Recuperado via Regex de Fallback."}

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

def solve_task(path, num_votes=3):
    task = load_json(path)
    reasoning_prompt = build_reasoning_prompt(task)
    
    predictions_counter = {}
    reasoning_map = {}
    
    print(f"Buscando {num_votes} soluções (2-Step Prompting)...")
    
    for i in range(num_votes):
        try:
            # ETAPA 1: Pede para o modelo pensar livremente
            chat_history = [
                {"role": "user", "parts": [{"text": reasoning_prompt}]}
            ]
            
            print(f"  [Tentativa {i+1}] Etapa 1: Pensando...")
            raw_thought = generate_chat(chat_history, temperature=0.6, max_tokens=4096)
            
            # --- LIMITE REMOVIDO: AGORA VOCÊ VÊ O TEXTO INTEIRO NO TERMINAL ---
            print("\n--- LLM REASONING ---")
            print(raw_thought)
            print("---------------------\n")
            
            # ETAPA 2: Muda o papel do modelo para um formatador de dados estrito
            chat_history.append({"role": "model", "parts": [{"text": raw_thought}]})
            
            formatting_prompt = (
                "You are a strict data parser. You must extract the final predicted grid or scalar value from your reasoning above.\n"
                "CRITICAL: Do NOT write any explanations, summaries, or conversational text. Output NOTHING but the <prediction> tags containing the numbers.\n\n"
                "Example format for a grid:\n"
                "<prediction>\n"
                "1 2\n"
                "3 4\n"
                "</prediction>\n\n"
                "Example format for a single number:\n"
                "<prediction>\n"
                "7\n"
                "</prediction>"
            )
            chat_history.append({"role": "user", "parts": [{"text": formatting_prompt}]})
            
            print(f"  [Tentativa {i+1}] Etapa 2: Formatando a saída...")
            # Temperatura reduzida para quase zero para evitar criatividade e focar na cópia exata do formato
            raw_prediction = generate_chat(chat_history, temperature=0.1, max_tokens=1024)
            print("\n--- LLM FINAL EXTRACTION ---")
            print(raw_prediction)
            print("----------------------------\n")
            
            # Parseia o resultado final
            parsed = extract_answer_from_text(raw_prediction) 
            
            if parsed and "prediction" in parsed:
                pred = parsed["prediction"]
                pred_norm = normalize_grid(pred)
                
                if not pred_norm:
                    continue
                
                pred_tuple = tuple(tuple(row) for row in pred_norm)
                predictions_counter[pred_tuple] = predictions_counter.get(pred_tuple, 0) + 1
                
                if pred_tuple not in reasoning_map:
                    reasoning_map[pred_tuple] = raw_thought
                    
        except Exception as e:
            print(f"Erro na tentativa {i+1}: {e}")
            continue

    if not predictions_counter:
        return False, "O modelo falhou em gerar um formato válido.", []

    best_pred_tuple = max(predictions_counter, key=predictions_counter.get)
    final_prediction = [list(row) for row in best_pred_tuple]
    final_reasoning = reasoning_map[best_pred_tuple]

    correct = None
    test = task.get("test", [])
    
    if test and "output" in test[0]:
        expected = normalize_grid(test[0]["output"])
        correct = (final_prediction == expected)

    return correct, final_reasoning, final_prediction