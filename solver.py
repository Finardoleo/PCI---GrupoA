import json
import re
from typing import Optional
from llmhandler import generate_text
from utils import load_json


def grid_to_text(grid):
    return "\n".join("".join(str(x) for x in row) for row in grid)


def build_prompt(task: dict) -> str:
    train = task.get("train", [])
    test = task.get("test", [])
    s = (
        "You are solving an ARC task. Provide a concise reasoning summary (max 2 sentences) that explains how you solved the test input — do NOT print all intermediate grids."
        " After that, output ONLY a single JSON object on its own line (no surrounding text) containing exactly two keys: `prediction` (a 2D array of numbers for the TEST INPUT) and `reasoning_summary` (the same short summary)."
        " The JSON must be parseable by a standard JSON parser. Use only integers in the prediction array.\n\n"
    )

    if train:
        s += "Training examples:\n"
        for ex in train:
            s += "Input:\n" + grid_to_text(ex["input"]) + "\n"
            s += "Output:\n" + grid_to_text(ex["output"]) + "\n---\n"

    if test:
        s += "Test input:\n" + grid_to_text(test[0]["input"]) + "\n\n"

    s += "Answer format example:\n{" + '"prediction": [[1,2],[3,4]], "reasoning_summary": "Short summary here"}' + "\n\nNow solve the test input."
    return s


def extract_json_from_text(text: str) -> Optional[dict]:
    # Try to locate a JSON object that contains the prediction key
    m = re.search(r"\{[\s\S]*?\}\s*$", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass

    # Try to find any JSON object with prediction inside
    m = re.search(r"\{[\s\S]*?\"prediction\"[\s\S]*?\}", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass

    # Try to find a bare array
    m = re.search(r"\[\s*\[.*?\]\s*\]", text, re.S)
    if m:
        try:
            arr = json.loads(m.group(0))
            return {"prediction": arr}
        except Exception:
            pass

    return None


def solve_task_file(path):
    task = load_json(path)
    prompt = build_prompt(task)
    raw = generate_text(prompt)
    parsed = extract_json_from_text(raw)
    prediction = None
    reasoning = None
    if parsed:
        prediction = parsed.get("prediction")
        # prefer explicit reasoning_summary if provided
        reasoning = parsed.get("reasoning_summary") or parsed.get("reasoning")

    # Fallbacks when model didn't return proper JSON
    if not reasoning:
        # derive a short summary: remove pure-grid lines and take the first sentence-like chunk
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        non_grid_lines = [l for l in lines if re.search(r"[A-Za-z]", l)]
        if non_grid_lines:
            # join and cut to first 2 sentences
            joined = " ".join(non_grid_lines)
            parts = re.split(r"(?<=[\.\?!])\s+", joined)
            reasoning = " ".join(parts[:2]).strip()
        else:
            reasoning = "(no concise reasoning provided)"

    if prediction is None:
        prediction = []
    else:
        # Ensure prediction is a 2D list; if it's a flat string, try to parse it
        if isinstance(prediction, str):
            # try parse lines of digits
            rows = [list(map(int, list(r.strip()))) for r in prediction.splitlines() if r.strip()]
            prediction = rows

    # If prediction still empty, try to extract rows from the raw reasoning text.
    if not prediction:
        # Look for backtick-enclosed rows like `3 2 3 2 3 2` which often appear in model reasoning
        backtick_rows = re.findall(r'`([0-9 \t]+)`', raw)
        if backtick_rows:
            try:
                rows = [list(map(int, re.split(r"\s+", r.strip()))) for r in backtick_rows]
                if rows:
                    prediction = rows
            except Exception:
                pass

    # As a last resort, look for plain lines that look like rows (only digits and spaces)
    if not prediction:
        candidate_rows = []
        for line in raw.splitlines():
            line = line.strip()
            if re.match(r"^[0-9](?:[ 0-9])*$", line):
                try:
                    candidate_rows.append(list(map(int, line.split())))
                except Exception:
                    pass
        if candidate_rows:
            prediction = candidate_rows

    correct = None
    test = task.get("test", [])

    def normalize_grid(g):
        # convert nested lists or strings into list[list[int]]
        if g is None:
            return []
        # If it's a string, try to parse rows
        if isinstance(g, str):
            try:
                rows = [list(map(int, re.split(r"\s+", r.strip()))) for r in g.splitlines() if r.strip()]
                return rows
            except Exception:
                return []
        # If it's a list, ensure nested ints
        if isinstance(g, list):
            out = []
            for row in g:
                if isinstance(row, list):
                    newrow = []
                    for v in row:
                        try:
                            newrow.append(int(v))
                        except Exception:
                            # single-character strings like '86' -> split
                            if isinstance(v, str) and len(v) > 1 and v.isdigit():
                                newrow.extend([int(c) for c in v])
                    out.append(newrow)
                elif isinstance(row, str):
                    # space separated or concatenated digits
                    if re.match(r"^[0-9 ]+$", row):
                        out.append([int(x) for x in row.split()])
                    elif row.isdigit():
                        out.append([int(c) for c in row])
            return out
        return []

    if test and "output" in test[0]:
        expected = normalize_grid(test[0]["output"])
        pred_norm = normalize_grid(prediction)
        correct = pred_norm == expected
        # keep prediction normalized for return
        prediction = pred_norm

    return {"prediction": prediction, "reasoning": reasoning, "correct": correct}
