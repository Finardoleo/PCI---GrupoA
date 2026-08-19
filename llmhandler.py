import os
from dotenv import load_dotenv
import requests
import json
import time
import re

load_dotenv()

# Alterado de generate_text para generate_chat
def generate_chat(contents: list, model: str = None, api_key: str = None, max_tokens: int = 4096, temperature: float = 0.6) -> str:
    api_key = api_key or os.getenv("GEMMA_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = model or os.getenv("GEMMA_MODEL", "gemma-2-27b-it")
    
    if not api_key:
        raise RuntimeError("API KEY environment variable is not set no .env")
    
    endpoint_override = os.getenv("GEMMA_ENDPOINT")

    if str(model).startswith("models/"):
        model_name = str(model).split("/", 1)[1]
    else:
        model_name = str(model)

    # Agora passamos o array 'contents' diretamente para o payload
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "candidateCount": 1,
            "maxOutputTokens": max_tokens
        }
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
    j = None
    
    for url in endpoints:
        try:
            resp = requests.post(url, json=payload, timeout=300)
            last_resp = resp
            if resp.status_code == 404:
                continue
            resp.raise_for_status()
            
            try:
                j = resp.json()
            except ValueError:
                j = None
            break
        except requests.RequestException as e:
            continue

    if j is None:
        raise RuntimeError("Failed to get a valid response from the API.")

    out = None
    if isinstance(j, dict):
        candidates = j.get("candidates", [])
        if candidates:
            try:
                out = candidates[0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                pass
                
    if out is None:
        out = json.dumps(j)

    try:
        # Delay de 15 segundos mantido para evitar Rate Limit da API do Google
        time.sleep(15)
    except Exception:
        pass

    return out