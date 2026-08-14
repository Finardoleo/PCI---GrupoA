import argparse
from pathlib import Path
from solver import solve_task_file


def main():
    parser = argparse.ArgumentParser(description="ARC Gemma Solver CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task", help="Path to single ARC JSON task file")
    group.add_argument("--batch", help="Path to .txt file listing task filenames (one per line)")
    parser.add_argument("--data-dir", default="data", help="Data folder containing tasks")
    parser.add_argument("--out", help="Optional output folder to save results")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    tasks = []
    if args.task:
        tasks = [Path(args.task)]
    else:
        batch_path = Path(args.batch)
        with batch_path.open() as f:
            for line in f:
                name = line.strip()
                if not name:
                    continue
                tasks.append(data_dir / name)

    for task_path in tasks:
        print(f"\n=== Solving {task_path} ===")
        try:
            res = solve_task_file(task_path)
        except Exception as e:
            print(f"Error solving {task_path}: {e}")
            continue

        print("Reasoning:\n", res.get("reasoning", "(no reasoning)"))
        print("Prediction grid:")
        for row in res.get("prediction", []):
            print(''.join(str(x) for x in row))
        correct = res.get("correct")
        if correct is None:
            print("Correct: (no expected output to check)")
        else:
            print("Correct:", correct)
        if args.out:
            outp = Path(args.out)
            outp.mkdir(parents=True, exist_ok=True)
            out_file = outp / (task_path.stem + "_result.txt")
            with out_file.open("w", encoding="utf-8") as f:
                f.write("Reasoning:\n" + res.get("reasoning", "") + "\n\n")
                f.write("Prediction:\n")
                for r in res.get("prediction", []):
                    f.write(''.join(str(x) for x in r) + "\n")
            print("Saved result to", out_file)


if __name__ == "__main__":
    main()
