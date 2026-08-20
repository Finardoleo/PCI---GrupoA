import json
import time
from llmhandler import generate_chat

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def grid_to_text(grid):
    return "\n".join(" ".join(str(x) for x in row) for row in grid)

def parse_prediction(raw_text):
    """Extract grid from <prediction>...</prediction> tags or from raw grid text"""
    try:
        # First try to find <prediction> tags
        start = raw_text.find("<prediction>")
        end = raw_text.find("</prediction>")
        if start != -1 and end != -1:
            grid_text = raw_text[start + len("<prediction>"):end].strip()
            grid = []
            for line in grid_text.split("\n"):
                line = line.strip()
                if line:
                    row = [int(x) for x in line.split()]
                    grid.append(row)
            return grid if grid else None
        
        # If no tags, look for "Row N:" patterns
        lines = raw_text.split("\n")
        grid = []
        for line in lines:
            line = line.strip()
            # Look for lines starting with "Row" and containing numbers
            if line.startswith("Row") and ":" in line:
                # Extract numbers after the colon
                parts = line.split(":", 1)
                if len(parts) > 1:
                    num_part = parts[1].strip()
                    try:
                        row = [int(x) for x in num_part.split()]
                        if row:
                            grid.append(row)
                    except:
                        pass
        
        if grid:
            return grid
        
        # Fallback: look for the largest grid pattern (most columns)
        all_grids = []
        current_grid = []
        for line in lines:
            line = line.strip()
            # Check if line looks like a grid row (numbers separated by spaces)
            if line and all(part.isdigit() or part == '' for part in line.split()):
                numbers = [int(x) for x in line.split() if x]
                if numbers:
                    current_grid.append(numbers)
            elif current_grid:
                all_grids.append(current_grid)
                current_grid = []
        if current_grid:
            all_grids.append(current_grid)
        
        # Return the largest grid (most columns)
        if all_grids:
            return max(all_grids, key=lambda g: len(g[0]) if g else 0)
        
        return None
    except:
        return None

def grids_equal(grid1, grid2):
    """Compare two grids for equality"""
    if grid1 is None or grid2 is None:
        return False
    if len(grid1) != len(grid2):
        return False
    for r1, r2 in zip(grid1, grid2):
        if r1 != r2:
            return False
    return True

def calculate_accuracy(task: dict, raw_prediction: str):
    """Calculate accuracy comparing predicted output with ground truth"""
    if not task.get("test"):
        return None
    
    predicted_grid = parse_prediction(raw_prediction)
    test_cases = task.get("test", [])
    
    if predicted_grid is None:
        return 0.0
    
    correct = 0
    for test_case in test_cases:
        expected_grid = test_case.get("output")
        if grids_equal(predicted_grid, expected_grid):
            correct += 1
    
    accuracy = (correct / len(test_cases)) * 100 if test_cases else 0.0
    return accuracy

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
    
    start_total = time.time()
    
    try:
        # ETAPA 1: Chamada Isolada 1 (Liberdade total de tokens)
        chat_1 = [{"role": "user", "parts": [{"text": reasoning_prompt}]}]
        
        print(f"  Etapa 1: Pensando...")
        start_1 = time.time()
        raw_thought = generate_chat(chat_1, temperature=0.6, max_tokens=8192)
        time_1 = time.time() - start_1
        
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
        start_2 = time.time()
        raw_prediction = generate_chat(chat_2, temperature=0.1, max_tokens=8192)
        time_2 = time.time() - start_2
        
        print("\n--- LLM FINAL EXTRACTION ---")
        print(raw_prediction)
        print("----------------------------\n")
        
        total_time = time.time() - start_total
        print(f"TIMING: Stage 1: {time_1:.2f}s | Stage 2: {time_2:.2f}s | Total: {total_time:.2f}s\n")
        
        accuracy = calculate_accuracy(task, raw_prediction)
        if accuracy is not None:
            print(f"ACCURACY: {accuracy:.1f}%\n")
        
        return raw_prediction
                
    except Exception as e:
        print(f"Erro na execução: {e}")
        return f"ERRO: {e}"