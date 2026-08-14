import json
from pathlib import Path


def load_json(path: Path or str):
    path = Path(path)
    with path.open(encoding="utf-8") as f:
        return json.load(f)
