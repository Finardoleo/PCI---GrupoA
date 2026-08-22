# PCI---Baseline
Para olhar o diário/logbook do projeto, entre na "Wiki" no próprio repositório do Github.

Para checar quais outros modelos existem para colocar no .env, é só rodar o programa check_models.py com "python check_models.py".

Para gerar um gráfico dos dados obtidos na planilha, é só rodar o programa gera_grafico.py com "python gera_grafico.py".

# ARC-AGI Solver (Gemma & Gemini API)

This project is an automated solver for ARC-AGI-1 problems. It utilizes the `gemma-4-31b-it` model via the Google Gemini API to analyze ARC task grids and predict the correct output. 

## Prerequisites
* Python 3.9 or higher
* A Google Gemini API Key

## Setup Instructions

**1. Set up a virtual environment**
It's highly recommended to use a virtual environment to manage dependencies, but not strictly needed. Open your terminal and run:

```bash
python -m venv venv
venv\Scripts\activate 
```

**2. Install requirements**
With your virtual environment active, install the necessary Python packages:

```bash
pip install -r requirements.txt
```

**3. Configure your environment variables**
This project requires a .env file to securely load your API keys. 
- Copy the provided template file:
```bash
  copy .env.example .env
```
- Open the new .env file in your text editor.
- Replace your_api_key_here with your actual Google Gemini API key.

**4. Add your data**
Ensure your ARC-AGI JSON task files (like 00dbd492.json) are placed within the data/ directory.

## Usage

The application features a 15-second delay between API requests to prevent rate-limiting from the Google API. You can run the solver in two modes:

### Single Task Mode
To evaluate a single JSON file, run:
```bash
python main.py --mode single --input data/training/00dbd492.json --output results.csv
```

### Batch Mode (List from file)
To evaluate multiple tasks listed in a `.txt` file sequentially:
```bash
python main.py --mode batch --input tasks.txt --output batch_results.csv
```

### All Dataset Mode (Run all problems in `data/`)
To automatically discover and evaluate all ARC tasks in the `data/` directory (with immediate persistence after every task):
```bash
# Run all 800 tasks (training + evaluation)
python main.py --mode all --output all_results.csv

# Or run only training tasks (400 tasks)
python main.py --mode all --split training --output train_results.csv

# Or run only evaluation tasks (400 tasks)
python main.py --mode all --split evaluation --output eval_results.csv
```

### Retry Modes (Re-run Failed Tasks)
To re-run only tasks that failed in an existing spreadsheet:
```bash
# 1. Re-run ALL incorrect/failed tasks from the spreadsheet
python main.py --output batch_results.csv --retry incorrect

# 2. Re-run ONLY tasks that failed with 'Insufficient data' in reasoning
python main.py --output batch_results.csv --retry insufficient
```

### Additional Flags
* `--new`: Overwrite existing CSV spreadsheets and restart from scratch.
* `--retry {incorrect, insufficient}`: Filter and re-execute only failed tasks.

## Output
The script automatically evaluates and corrects each task against the ARC-AGI ground-truth test grid and generates **5 dedicated CSV spreadsheets inside the `Results/` folder**:
1. `Results/<output>_accuracy.csv`: Contains whether the model got the problem right (`CORRECT` / `INCORRECT`) and the final batch accuracy (`Batch Accuracy: XX.XX% (Y/Z)`).
2. `Results/<output>_tokens.csv`: Contains the tokens breakdown per task (`Total: X (Prompt: Y, Resposta: Z, Pensamento: W)`) and the cumulative batch sum (`Tokens do Batch`).
3. `Results/<output>_reasoning.csv`: Contains only the summary of the reasoning behind the answer.
4. `Results/<output>_grids.csv`: Contains only the predicted matrices/grids.
5. `Results/<output>_times.csv`: Contains only the timers (`Total: XX.XXs (Raciocínio: YY.YYs, Formatação: ZZ.ZZs)`) and the cumulative batch sum (`Tempo do Batch`).

## Additional Codes
### task_generator.py (ARC Task Generator & 2D Transformer)
Generates new ARC tasks by applying 2D transformations (Rotations, Reflections, Colorations, Merged) to original tasks from `data/`:
```bash
# Generate 10 random transformed tasks
python task_generator.py --num-tasks 10

# Generate 20 tasks with Rotation on input and Reflection on output
python task_generator.py --input-transform rotation --output-transform reflection --num-tasks 20

# Generate tasks for all 800 problems in data/ with coloration
python task_generator.py --transform coloration --num-tasks all

# Generate merged transformations (combinations of 2 distinct transforms)
python task_generator.py --transform merged --num-tasks 15
```
Tasks are automatically saved in categorized folders:
* `New Tasks/Rotation/`: Rotation-only transforms
* `New Tasks/Reflexion/`: Reflection-only transforms
* `New Tasks/Coloration/`: Color permutation transforms
* `New Tasks/Merged/`: Composite or mixed transforms

All transformations are tracked and deduplicated in `New Tasks/transformed_tasks.csv`.

### check_models.py
* You can use this code to check out all possible models available for the API, and its formal names.

### gera_grafico.py
* You can use this code to create a bar graph for the data obtained in the spreadsheet.