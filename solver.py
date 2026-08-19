import json
from llmhandler import generate_chat

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def grid_to_text(grid):
    return "\n".join(" ".join(str(x) for x in row) for row in grid)

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

    s += "What is the logical rule, and what is the exact final grid for the TEST INPUT?"
    return s

def solve_task(path):
    task = load_json(path)
    reasoning_prompt = build_reasoning_prompt(task)
    
    print(f"Processando task (2-Step Prompting)...")
    
    try:
        # ETAPA 1: Chamada Isolada 1 (Liberdade total de tokens)
        chat_1 = [{"role": "user", "parts": [{"text": reasoning_prompt}]}]
        
        print(f"  Etapa 1: Pensando...")
        raw_thought = generate_chat(chat_1, temperature=0.6, max_tokens=8192)
        
        print("\n--- LLM REASONING ---")
        print(raw_thought)
        print("---------------------\n")
        
        # ETAPA 2: Chamada Isolada 2 (Novo escopo absoluto)
        # Em vez de continuar a conversa, iniciamos uma requisição do zero,
        # injetando o texto da Etapa 1 como se fosse um documento a ser lido.
        formatting_prompt = f"""You are a strict data parser. Your ONLY job is to extract the final predicted grid or scalar value from the reasoning text provided below.
CRITICAL: Do NOT write any explanations, summaries, or conversational text. Output NOTHING but the <prediction> tags containing the numbers.

[REASONING TEXT BEGIN]
{raw_thought}
[REASONING TEXT END]

Example format for a grid:
<prediction>
1 2
3 4
</prediction>

Example format for a single number:
<prediction>
7
</prediction>"""
        
        # Inicia um chat zerado apenas com a regra de extração
        chat_2 = [{"role": "user", "parts": [{"text": formatting_prompt}]}]
        
        print(f"  Etapa 2: Formatando a saída...")
        raw_prediction = generate_chat(chat_2, temperature=0.1, max_tokens=8192)
        
        print("\n--- LLM FINAL EXTRACTION ---")
        print(raw_prediction)
        print("----------------------------\n")
        
        return raw_prediction
                
    except Exception as e:
        print(f"Erro na execução: {e}")
        return f"ERRO: {e}"