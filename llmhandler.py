import os
from dotenv import load_dotenv
import requests
import json
import time
import re

# Load .env into the environment if present
load_dotenv()

def generate_text(prompt: str, model: str = None, api_key: str = None, max_tokens: int = 1024, temperature: float = 0.2) -> str:
    api_key = api_key or os.getenv("GEMMA_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    model = model or os.getenv("GEMMA_MODEL", "gemma-4-31b")
    
    if not api_key:
        raise RuntimeError("GEMMA_API_KEY (or GOOGLE_API_KEY) environment variable is not set")
    
    endpoint_override = os.getenv("GEMMA_ENDPOINT")

    if str(model).startswith("models/"):
        model_name = str(model).split("/", 1)[1]
    else:
        model_name = str(model)

    # Payload atualizado com trava rigorosa para JSON
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": temperature,
            "candidateCount": 1,
            "maxOutputTokens": max_tokens,
            "responseMimeType": "application/json" # Impede qualquer texto fora do JSON
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
        # URL atualizada para v1beta e :generateContent, com regex corrigida para permitir pontos
        model_safe = re.sub(r"[^a-z0-9\-\.]", "", model_name.lower().replace(" ", "-"))
        endpoints = [
            f"https://generativelanguage.googleapis.com/v1beta/models/{model_safe}:generateContent?key={api_key}",
            f"https://generativelanguage.googleapis.com/v1/models/{model_safe}:generateContent?key={api_key}",
        ]

    last_resp = None
    last_exc = None
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
            last_exc = e
            continue

    if last_resp is not None and last_resp.status_code == 404:
        detail = last_resp.text
        raise RuntimeError(
            f"Model not found (404). Tried endpoints for model '{model_name}'. "
            "Ensure the model name is correct and the Generative Language API is enabled. "
            f"Tried URLs: {', '.join(endpoints)}\nAPI response: {detail}"
        )

    if j is None:
        status = getattr(last_resp, "status_code", None) if last_resp else None
        text = getattr(last_resp, "text", None) if last_resp else None
        err_parts = [f"Tried endpoints: {', '.join(endpoints)}"]
        if status is not None: err_parts.append(f"Last status: {status}")
        if text: err_parts.append(f"Last response body: {text}")
        if last_exc: err_parts.append(f"Last exception: {repr(last_exc)}")
        raise RuntimeError("Failed to get a valid response from the Generative Language API. " + " | ".join(err_parts))

    # Parse da resposta para extrair o texto JSON retornado
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
        time.sleep(15)
    except Exception:
        pass

    return out