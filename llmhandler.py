import os
from dotenv import load_dotenv
import requests
import json
import time
import re

load_dotenv()

def generate_chat(
    contents: list,
    model: str = None,
    api_key: str = None,
    max_tokens: int = None,
    temperature: float = 0.6,
    thinking_level: str = None,
    thinking_budget: int = None,
    rate_limit_delay: float = 15.0,
    max_retries: int = 3
) -> dict:
    """
    Envia uma requisição para a API Google Gemini / Gemma.
    Retorna um dicionário contendo:
      - text: string de resposta do modelo
      - tokens: dicionário com prompt, candidates, thoughts e total
      - latency: tempo puro da requisição à API (em segundos, sem delay)
      - raw: resposta bruta da API
    """
    api_key = api_key or os.getenv("GEMMA_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = model or os.getenv("GEMMA_MODEL", "gemma-4-31b-it")
    
    if not api_key:
        raise RuntimeError("API KEY environment variable is not set in .env")
    
    endpoint_override = os.getenv("GEMMA_ENDPOINT")

    if str(model).startswith("models/"):
        model_name = str(model).split("/", 1)[1]
    else:
        model_name = str(model)

    if max_tokens is None:
        max_tokens = int(os.getenv("MAX_OUTPUT_TOKENS", "16384"))

    generation_config = {
        "temperature": temperature,
        "candidateCount": 1,
        "maxOutputTokens": max_tokens
    }

    # Configuração do Thinking Mode
    if thinking_level is None and thinking_budget is None:
        thinking_level = os.getenv("THINKING_LEVEL", "HIGH")

    if thinking_budget is not None:
        generation_config["thinkingConfig"] = {
            "thinkingBudget": thinking_budget
        }
    elif thinking_level:
        thinking_str = str(thinking_level).strip().upper()
        if "gemini-2.5" in model_name.lower():
            if thinking_str in ["OFF", "MINIMAL", "0"]:
                generation_config["thinkingConfig"] = {"thinkingBudget": 0}
            else:
                generation_config["thinkingConfig"] = {"thinkingBudget": -1}
        else:
            if thinking_str in ["OFF", "0"]:
                thinking_str = "MINIMAL"
            generation_config["thinkingConfig"] = {
                "thinkingLevel": thinking_str
            }

    payload = {
        "contents": contents,
        "generationConfig": generation_config
    }

    if endpoint_override:
        if "key=" in endpoint_override:
            endpoints = [endpoint_override]
        elif "?" in endpoint_override:
            endpoints = [endpoint_override + f"&key={api_key}"]
        else:
            endpoints = [endpoint_override + f"?key={api_key}"]
    else:
        model_safe = re.sub(r"[^a-z0-9\-\.]", "", model_name.lower().replace(" ", "-"))
        endpoints = [
            f"https://generativelanguage.googleapis.com/v1beta/models/{model_safe}:generateContent?key={api_key}",
            f"https://generativelanguage.googleapis.com/v1/models/{model_safe}:generateContent?key={api_key}",
        ]

    last_resp = None
    last_error_detail = ""
    j = None
    api_latency = 0.0
    
    for attempt in range(1, max_retries + 1):
        for url in endpoints:
            try:
                req_start = time.time()
                timeout_val = int(os.getenv("API_TIMEOUT", "900"))
                resp = requests.post(url, json=payload, timeout=timeout_val)
                req_duration = time.time() - req_start
                last_resp = resp
                
                if resp.status_code != 200:
                    last_error_detail = resp.text
                    
                if resp.status_code == 404:
                    continue
                    
                resp.raise_for_status()
                api_latency = req_duration
                
                try:
                    j = resp.json()
                except ValueError:
                    j = None
                break
            except requests.RequestException as e:
                last_error_detail = f"Erro de conexão/requisição: {e}"
                continue

        if j is not None:
            break
            
        # Se falhou e ainda tem tentativas, aguarda antes de tentar de novo
        if attempt < max_retries:
            wait_time = attempt * 5
            print(f"  [!] Falha na tentativa {attempt}/{max_retries}. Aguardando {wait_time}s para tentar novamente...")
            time.sleep(wait_time)

    if j is None:
        error_msg = f"Failed to get a valid response from the API.\nÚltimo status: {getattr(last_resp, 'status_code', 'N/A')}\nDetalhes do Erro da API: {last_error_detail}"
        raise RuntimeError(error_msg)

    # Extração de tokens do usageMetadata
    usage = j.get("usageMetadata", {}) if isinstance(j, dict) else {}
    prompt_tokens = usage.get("promptTokenCount", 0)
    candidates_tokens = usage.get("candidatesTokenCount", 0)
    thoughts_tokens = usage.get("thoughtsTokenCount", 0)
    total_tokens = usage.get("totalTokenCount", prompt_tokens + candidates_tokens + thoughts_tokens)

    tokens_info = {
        "prompt": prompt_tokens,
        "candidates": candidates_tokens,
        "thoughts": thoughts_tokens,
        "total": total_tokens
    }

    # Extração do texto
    out = None
    if isinstance(j, dict):
        candidates = j.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            text_parts = []
            thought_parts = []
            for p in parts:
                if isinstance(p, dict):
                    if p.get("thought", False):
                        thought_parts.append(p.get("text", ""))
                    elif "text" in p:
                        text_parts.append(p.get("text", ""))
            
            if text_parts:
                out = "".join(text_parts).strip()
            elif thought_parts:
                out = "".join(thought_parts).strip()
                
    if out is None:
        out = json.dumps(j)

    # Rate limiting delay (executado após registrar a latência pura da requisição)
    if rate_limit_delay > 0:
        try:
            time.sleep(rate_limit_delay)
        except Exception:
            pass

    return {
        "text": out,
        "tokens": tokens_info,
        "latency": api_latency,
        "raw": j
    }