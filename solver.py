import json
import re
import time
from llmhandler import generate_chat

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def grid_to_text(grid):
    if not isinstance(grid, list):
        return str(grid)
    if grid and isinstance(grid[0], list):
        return "\n".join(" ".join(str(x) for x in row) for row in grid)
    return " ".join(str(x) for x in grid)


def _normalize_prediction_value(value):
    """Converts the model output into a grid-like structure when needed."""
    if value is None:
        return None
    if isinstance(value, list):
        if value and isinstance(value[0], list):
            return value
        if value and isinstance(value[0], (int, float)):
            return [value]
        return value
    if isinstance(value, tuple):
        return [_normalize_prediction_value(item) for item in value]
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        compact = value.strip()
        if not compact:
            return None
        try:
            parsed = json.loads(compact)
            return _normalize_prediction_value(parsed)
        except Exception:
            numbers = re.findall(r"-?\d+", compact)
            if numbers:
                if "\n" in compact or " " in compact:
                    rows = []
                    for line in compact.splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        row_numbers = re.findall(r"-?\d+", line)
                        if row_numbers:
                            rows.append([int(n) for n in row_numbers])
                    return rows if rows else [int(n) for n in numbers]
                return [int(n) for n in numbers]
            return compact
    return value


def extract_prediction_payload(text: str):
    """Extracts a structured JSON payload from noisy model output and normalizes it."""
    if not isinstance(text, str):
        return {"summary": "", "prediction": None}

    cleaned = text.strip()

    if not cleaned:
        return {"summary": "", "prediction": None}

    json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if json_match:
        candidate = json_match.group(0)
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                summary = str(parsed.get("summary", "")).strip()
                prediction = _normalize_prediction_value(parsed.get("prediction"))
                return {"summary": summary, "prediction": prediction}
        except Exception:
            pass

    summary_match = re.search(r"<summary>(.*?)</summary>", cleaned, re.DOTALL | re.IGNORECASE)
    pred_match = re.search(r"<prediction>(.*?)</prediction>", cleaned, re.DOTALL | re.IGNORECASE)

    summary = summary_match.group(1).strip() if summary_match else ""
    prediction_raw = pred_match.group(1).strip() if pred_match else cleaned

    prediction = _normalize_prediction_value(prediction_raw)
    if isinstance(prediction, str):
        try:
            parsed = json.loads(prediction)
            prediction = _normalize_prediction_value(parsed)
        except Exception:
            pass

    if isinstance(prediction, list) and prediction and isinstance(prediction[0], list):
        final_prediction = prediction
    elif isinstance(prediction, list) and prediction and isinstance(prediction[0], (int, float)):
        final_prediction = [prediction]
    else:
        final_prediction = prediction

    return {"summary": summary, "prediction": final_prediction}


def parse_grid_from_text(text: str):
    """
    Converte uma string contendo um grid ou valores numéricos em uma lista 2D de inteiros.
    """
    if not text or not isinstance(text, str):
        return []

    structured = extract_prediction_payload(text)
    if structured.get("prediction") is not None:
        prediction = structured["prediction"]
        if isinstance(prediction, list):
            if prediction and isinstance(prediction[0], list):
                return prediction
            if prediction and isinstance(prediction[0], (int, float)):
                return [prediction]
        if isinstance(prediction, (int, float)):
            return [[prediction]]

    content = text.strip()
    content = re.sub(r"```(?:json|python)?", "", content).replace("```", "").strip()

    try:
        loaded = json.loads(content)
        if isinstance(loaded, list):
            return loaded
        if isinstance(loaded, int):
            return [[loaded]]
    except Exception:
        pass

    grid = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        numbers = re.findall(r"-?\d+", line)
        if numbers:
            grid.append([int(n) for n in numbers])

    return grid


def extract_tags(text: str):
    """
    Extrai o resumo e a previsão de forma limpa.
    Retorna (summary_str, prediction_grid_str, formatted_full_str).
    """
    payload = extract_prediction_payload(text)
    summary = payload.get("summary", "")
    prediction = payload.get("prediction")
    prediction_str = json.dumps(prediction, ensure_ascii=False) if prediction is not None else ""

    formatted_parts = []
    if summary:
        formatted_parts.append(f"<summary>\n{summary}\n</summary>")
    formatted_parts.append(f"<prediction>\n{prediction_str}\n</prediction>")

    return summary, prediction_str, "\n\n".join(formatted_parts)


def evaluate_prediction(task: dict, raw_prediction: str):
    """
    Compara o grid predito com o ground truth de test[0]['output'].
    Retorna (is_correct, status_str, clean_grid_str, clean_summary_str).
    """
    payload = extract_prediction_payload(raw_prediction)
    summary_str = payload.get("summary", "")
    pred_value = payload.get("prediction")
    pred_str = json.dumps(pred_value, ensure_ascii=False) if pred_value is not None else raw_prediction
    parsed_grid = parse_grid_from_text(pred_str if pred_str else raw_prediction)

    test_cases = task.get("test", [])
    if not test_cases or "output" not in test_cases[0]:
        return False, "UNKNOWN", pred_str, summary_str

    ground_truth = test_cases[0]["output"]
    is_correct = (parsed_grid == ground_truth)
    status_str = "CORRECT" if is_correct else "INCORRECT"

    if parsed_grid:
        clean_grid_str = grid_to_text(parsed_grid)
    else:
        clean_grid_str = pred_str

    return is_correct, status_str, clean_grid_str, summary_str


def build_reasoning_prompt(task: dict) -> str:
    train = task.get("train", [])
    test = task.get("test", [])

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

    s += (
        "What is the logical rule, and what is the exact final grid for the TEST INPUT?\n"
        "Your final answer must be a single JSON object with exactly these keys:\n"
        "{\"summary\": \"short rule description\", \"prediction\": [[...], [...]]}\n"
        "Do not include any extra prose, markdown fences, explanations, self-checks, or confirmation text.\n"
        "The answer must be valid JSON only."
    )
    return s

def solve_task(path, api_key: str = None):
    task = load_json(path)
    reasoning_prompt = build_reasoning_prompt(task)
    
    print(f"Processando task (2-Step Prompting com High Thinking)...")
    
    tokens = {
        "prompt": 0,
        "candidates": 0,
        "thoughts": 0,
        "total": 0
    }
    total_latency = 0.0
    
    try:
        # ETAPA 1: Raciocínio Profundo (Thinking Mode: HIGH)
        chat_1 = [{"role": "user", "parts": [{"text": reasoning_prompt}]}]
        
        print(f"  Etapa 1: Pensando com High Thinking...")
        res_1 = generate_chat(chat_1, api_key=api_key, temperature=0.6, max_tokens=16384, thinking_level="HIGH")
        raw_thought = res_1["text"]
        latency_1 = res_1["latency"]
        total_latency += latency_1
        
        for k in tokens:
            tokens[k] += res_1["tokens"].get(k, 0)
            
        print("\n--- LLM REASONING ---")
        print(raw_thought[:1000] + ("..." if len(raw_thought) > 1000 else ""))
        print(f"Latency Stage 1: {latency_1:.2f}s | Tokens: {res_1['tokens']}")
        print("---------------------\n")
        
        # ETAPA 2: Extração e Formatação Estrita (Thinking Mode: MINIMAL para evitar monólogo interno)
        example_json = '{"summary":"Inverted the colors and shifted diagonal pixels down by one.","prediction":[[0,1,0],[1,0,1],[0,1,0]]}'
        formatting_prompt = f"""You are a strict post-processor. Ignore all conversational chatter, self-checks, and confirmations.
Your ONLY job is to extract the final answer from the reasoning text below and return it as valid JSON.
Return ONLY one JSON object with keys "summary" and "prediction".
No markdown fences, no tags, no extra prose, no explanations.

Example output:
{example_json}

[REASONING TEXT BEGIN]
{raw_thought}
[REASONING TEXT END]"""
        
        chat_2 = [{"role": "user", "parts": [{"text": formatting_prompt}]}]
        
        print(f"  Etapa 2: Formatando a saída (Thinking: MINIMAL)...")
        res_2 = generate_chat(chat_2, api_key=api_key, temperature=0.1, max_tokens=8192, thinking_level="MINIMAL")
        raw_prediction = res_2["text"]
        latency_2 = res_2["latency"]
        total_latency += latency_2
        
        for k in tokens:
            tokens[k] += res_2["tokens"].get(k, 0)
            
        print("\n--- LLM RAW EXTRACTION ---")
        print(raw_prediction)
        print(f"Latency Stage 2: {latency_2:.2f}s | Tokens: {res_2['tokens']}")
        print("----------------------------\n")
        
        # Avaliação de acurácia em relação ao ground truth
        is_correct, status_str, clean_grid, clean_summary = evaluate_prediction(task, raw_prediction)
        
        # Se a etapa 2 falhar na extração do grid, tenta recuperar da etapa 1
        if not clean_grid and "<prediction>" in raw_thought:
            is_correct, status_str, clean_grid, clean_summary = evaluate_prediction(task, raw_thought)

        timing = {
            "reasoning": latency_1,
            "formatting": latency_2,
            "total": total_latency
        }

        print(f"STATUS DA TASK: [{status_str}] | TEMPO: {total_latency:.2f}s | TOKENS: {tokens['total']}\n")
        
        return {
            "is_correct": is_correct,
            "status": status_str,
            "grid": clean_grid,
            "reasoning": clean_summary,
            "timing": timing,
            "solve_time": total_latency,
            "tokens": tokens
        }
                
    except Exception as e:
        print(f"Erro na execução da task: {e}")
        return {
            "is_correct": False,
            "status": f"ERROR: {e}",
            "grid": "",
            "reasoning": f"ERRO: {e}",
            "timing": {
                "reasoning": 0.0,
                "formatting": 0.0,
                "total": total_latency
            },
            "solve_time": total_latency,
            "tokens": tokens
        }