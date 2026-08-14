ARC Gemma Solver

Usage
- Put your Gemma/Google Generative API key in a `.env` file as `GEMMA_API_KEY`.
- Install dependencies: `pip install -r requirements.txt`
- Run a single task:

```bash
python main.py --task data/evaluation/00576224.json
```

- Run a batch (text file with one filename per line, relative to `data/`):

```bash
python main.py --batch tasks.txt --data-dir data --out results
```

The solver will print reasoning and the predicted grid and will check correctness if expected outputs are present.
# PCI---Baseline

Para checar quais outros modelos existem para colocar no .env, é só rodar o programa check_models.py com "python check_models.py".