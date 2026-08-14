import requests
import os
from dotenv import load_dotenv

# Carrega a chave do seu .env
load_dotenv()
api_key = os.getenv("GEMMA_API_KEY")

# Bate no endpoint de listagem de modelos
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get("models", [])
    print("Modelos disponíveis para esta chave que suportam generateContent:\n")
    for m in models:
        # Filtra apenas os modelos que funcionam para o nosso baseline
        if "generateContent" in m.get("supportedGenerationMethods", []):
            print(f"- {m['name'].replace('models/', '')}")
else:
    print(f"Erro ao buscar modelos: {response.status_code}\n{response.text}")