import argparse
import glob
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Paleta de cores moderna e profissional
PALETTE = {
    "Original": "#3B82F6",    # Blue 500
    "Training": "#3B82F6",    # Blue 500
    "Rotated": "#F59E0B",     # Amber 500
    "Reflected": "#10B981",   # Emerald 500
    "Coloration": "#8B5CF6",  # Purple 500
    "Merged": "#EF4444",      # Red 500
    "Default": "#6366F1",     # Indigo 500
}

DATASET_ORDER = [
    ("Training Data Set", "Original (Treino)", "Training"),
    ("Rotated Training Data Set", "Rotated", "Rotated"),
    ("Reflected Training Data Set", "Reflected", "Reflected"),
    ("Coloration Training Data Set", "Coloration", "Coloration"),
    ("Merged Training Data Set", "Merged", "Merged"),
]

def load_metadata_mapping(csv_path: str = "New Tasks/transformed_tasks.csv") -> Dict[str, str]:
    """
    Carrega o arquivo New Tasks/transformed_tasks.csv e cria um dicionário
    mapeando New_Task_ID (com e sem .json) para Original_Task.
    """
    mapping = {}
    if not os.path.exists(csv_path):
        return mapping
        
    try:
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            tid = str(row.get("New_Task_ID", "")).strip().replace(".json", "")
            orig = str(row.get("Original_Task", "")).strip()
            if tid and orig:
                mapping[tid] = orig
                mapping[f"{tid}.json"] = orig
    except Exception as e:
        print(f"[!] Aviso ao carregar transformed_tasks.csv: {e}")
        
    return mapping

def parse_token_string(s: Any) -> int:
    """Extrai o número total de tokens da string de saída."""
    if pd.isna(s):
        return 0
    m = re.search(r"Total:\s*(\d+)", str(s))
    if m:
        return int(m.group(1))
    try:
        return int(float(str(s).strip()))
    except (ValueError, TypeError):
        return 0

def parse_time_string(s: Any) -> float:
    """Extrai o tempo total em segundos da string de saída."""
    if pd.isna(s):
        return 0.0
    m = re.search(r"Total:\s*([\d\.]+)s?", str(s))
    if m:
        return float(m.group(1))
    try:
        return float(str(s).replace("s", "").strip())
    except (ValueError, TypeError):
        return 0.0

def discover_model_datasets(model_dir: str) -> List[Tuple[str, str, str]]:
    """
    Identifica as pastas de datasets presentes no diretório do modelo.
    Retorna lista de tuplas: (caminho_pasta, label_exibicao, chave_cor).
    """
    discovered = []
    base_path = Path(model_dir)
    if not base_path.exists():
        return discovered

    # 1. Verifica pastas padrão conhecidas
    for folder_name, display_label, color_key in DATASET_ORDER:
        folder_path = base_path / folder_name
        if folder_path.is_dir() and glob.glob(str(folder_path / "*_accuracy.csv")):
            discovered.append((str(folder_path), display_label, color_key))

    # 2. Se houver outras pastas com CSVs que não foram pegas acima
    for sub in sorted(base_path.iterdir()):
        if sub.is_dir() and str(sub) not in [d[0] for d in discovered]:
            csvs = glob.glob(str(sub / "*_accuracy.csv"))
            if csvs:
                discovered.append((str(sub), sub.name, "Default"))

    return discovered

def extract_dataset_metrics(
    folder_path: str,
    meta_map: Dict[str, str]
) -> Optional[Dict[str, Any]]:
    """
    Lê as planilhas _accuracy.csv, _tokens.csv e _times.csv da pasta e extrai
    todas as estatísticas requeridas.
    """
    acc_files = glob.glob(f"{folder_path}/*_accuracy.csv")
    tok_files = glob.glob(f"{folder_path}/*_tokens.csv")
    tim_files = glob.glob(f"{folder_path}/*_times.csv")

    if not acc_files or not tok_files or not tim_files:
        print(f"[!] Planilhas incompletas em '{folder_path}' (necessário _accuracy, _tokens e _times).")
        return None

    try:
        acc_df = pd.read_csv(acc_files[0])
        tok_df = pd.read_csv(tok_files[0])
        tim_df = pd.read_csv(tim_files[0])
    except Exception as e:
        print(f"[!] Erro ao ler CSVs de '{folder_path}': {e}")
        return None

    # Filtra linhas de sumário
    summary_tasks = {"Batch Accuracy", "Tempo do Batch", "Tokens do Batch", "Total", "Accuracy"}
    acc_clean = acc_df[~acc_df["Task"].astype(str).str.strip().isin(summary_tasks)].copy()
    tok_clean = tok_df[~tok_df["Task"].astype(str).str.strip().isin(summary_tasks)].copy()
    tim_clean = tim_df[~tim_df["Task"].astype(str).str.strip().isin(summary_tasks)].copy()

    if acc_clean.empty:
        return None

    model_col = acc_clean.columns[1]

    # Merge das três planilhas por Task
    merged = pd.merge(acc_clean[["Task", model_col]], tok_clean[["Task", model_col]], on="Task", suffixes=("_acc", "_tok"))
    merged = pd.merge(merged, tim_clean[["Task", model_col]], on="Task")
    merged.rename(
        columns={
            f"{model_col}_acc": "status",
            f"{model_col}_tok": "tok_str",
            model_col: "time_str"
        },
        inplace=True
    )

    merged["tokens"] = merged["tok_str"].apply(parse_token_string)
    merged["time_s"] = merged["time_str"].apply(parse_time_string)
    merged["is_correct"] = merged["status"].astype(str).str.strip() == "CORRECT"
    
    def resolve_orig(t_name: str) -> str:
        clean = str(t_name).strip().replace(".json", "")
        return meta_map.get(clean, meta_map.get(str(t_name).strip(), str(t_name).strip()))

    merged["orig_task"] = merged["Task"].apply(resolve_orig)

    total_tasks = len(merged)
    correct_count = int(merged["is_correct"].sum())
    incorrect_count = total_tasks - correct_count
    accuracy_pct = (correct_count / total_tasks * 100.0) if total_tasks > 0 else 0.0

    avg_tokens = float(merged["tokens"].mean()) if total_tasks > 0 else 0.0
    avg_time = float(merged["time_s"].mean()) if total_tasks > 0 else 0.0

    corr_df = merged[merged["is_correct"]]
    incorr_df = merged[~merged["is_correct"]]

    def make_record(row: Optional[pd.Series], val_col: str) -> Optional[Dict[str, Any]]:
        if row is None or row.empty:
            return None
        return {
            "task_id": str(row["Task"]),
            "original_task": str(row["orig_task"]),
            "value": row[val_col],
            "status": str(row["status"])
        }

    max_tok_corr = make_record(corr_df.loc[corr_df["tokens"].idxmax()] if not corr_df.empty else None, "tokens")
    min_tok_corr = make_record(corr_df.loc[corr_df["tokens"].idxmin()] if not corr_df.empty else None, "tokens")
    max_tok_incorr = make_record(incorr_df.loc[incorr_df["tokens"].idxmax()] if not incorr_df.empty else None, "tokens")

    max_tim_corr = make_record(corr_df.loc[corr_df["time_s"].idxmax()] if not corr_df.empty else None, "time_s")
    min_tim_corr = make_record(corr_df.loc[corr_df["time_s"].idxmin()] if not corr_df.empty else None, "time_s")
    max_tim_incorr = make_record(incorr_df.loc[incorr_df["time_s"].idxmax()] if not incorr_df.empty else None, "time_s")

    return {
        "folder": folder_path,
        "total_tasks": total_tasks,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "accuracy_pct": accuracy_pct,
        "avg_tokens": avg_tokens,
        "avg_time": avg_time,
        "max_tok_corr": max_tok_corr,
        "min_tok_corr": min_tok_corr,
        "max_tok_incorr": max_tok_incorr,
        "max_tim_corr": max_tim_corr,
        "min_tim_corr": min_tim_corr,
        "max_tim_incorr": max_tim_incorr,
    }

def print_summary_table(model_name: str, datasets_data: List[Tuple[str, str, Dict[str, Any]]]):
    """Imprime um sumário executivo detalhado no terminal."""
    print("\n" + "="*95)
    print(f"   RELATÓRIO COMPARATIVO DE BENCHMARK ARC-AGI - MODELO: {model_name.upper()}")
    print("="*95)
    
    header = f"{'Dataset':<20} | {'Tasks':<7} | {'Acurácia (%)':<15} | {'Média Tokens':<14} | {'Média Tempo (s)':<15}"
    print(header)
    print("-" * 95)
    
    for label, _, data in datasets_data:
        acc_str = f"{data['accuracy_pct']:.2f}% ({data['correct_count']}/{data['total_tasks']})"
        tok_str = f"{data['avg_tokens']:,.1f}"
        tim_str = f"{data['avg_time']:.2f}s"
        print(f"{label:<20} | {data['total_tasks']:<7} | {acc_str:<15} | {tok_str:<14} | {tim_str:<15}")
        
    print("-" * 95)
    print("\n" + "="*95)
    print("   EXTREMOS DE TOKENS E TEMPO (MIN / MAX COM TASKS ORIGINAIS)")
    print("="*95)
    
    for label, _, data in datasets_data:
        print(f"\n[{label.upper()}]")
        print("  * TOKENS:")
        if data["max_tok_corr"]:
            r = data["max_tok_corr"]
            print(f"    - Máx [CORRECT]  : {r['value']:,} tokens | Task: {r['task_id']} (Orig: {r['original_task']})")
        if data["min_tok_corr"]:
            r = data["min_tok_corr"]
            print(f"    - Mín [CORRECT]  : {r['value']:,} tokens | Task: {r['task_id']} (Orig: {r['original_task']})")
        if data["max_tok_incorr"]:
            r = data["max_tok_incorr"]
            print(f"    - Máx [INCORRECT]: {r['value']:,} tokens | Task: {r['task_id']} (Orig: {r['original_task']})")

        print("  * TEMPO DE EXECUÇÃO:")
        if data["max_tim_corr"]:
            r = data["max_tim_corr"]
            print(f"    - Máx [CORRECT]  : {r['value']:.2f}s | Task: {r['task_id']} (Orig: {r['original_task']})")
        if data["min_tim_corr"]:
            r = data["min_tim_corr"]
            print(f"    - Mín [CORRECT]  : {r['value']:.2f}s | Task: {r['task_id']} (Orig: {r['original_task']})")
        if data["max_tim_incorr"]:
            r = data["max_tim_incorr"]
            print(f"    - Máx [INCORRECT]: {r['value']:.2f}s | Task: {r['task_id']} (Orig: {r['original_task']})")

    print("\n" + "="*95)

def plot_accuracy_chart(
    model_name: str,
    datasets_data: List[Tuple[str, str, Dict[str, Any]]],
    output_path: str
):
    """Gera o gráfico de barras comparativo de Acurácia (%)."""
    labels = [d[0] for d in datasets_data]
    colors = [PALETTE.get(d[1], PALETTE["Default"]) for d in datasets_data]
    accuracies = [d[2]["accuracy_pct"] for d in datasets_data]
    counts = [(d[2]["correct_count"], d[2]["total_tasks"]) for d in datasets_data]

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    x = np.arange(len(labels))
    width = 0.55

    bars = ax.bar(x, accuracies, width=width, color=colors, edgecolor="#1E293B", linewidth=1.2, zorder=3)

    # Rótulos sobre as barras com badge
    for bar, acc, (corr, tot) in zip(bars, accuracies, counts):
        y_val = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            y_val + 2.5,
            f"{acc:.2f}%\n({corr}/{tot})",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#0F172A",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", alpha=0.9, edgecolor="#E2E8F0", linewidth=0.8),
            zorder=4
        )

    ax.set_title(f"Taxa de Acurácia ARC-AGI por Dataset - Modelo: {model_name}", fontsize=15, fontweight="bold", pad=20)
    ax.set_ylabel("Acurácia (%)", fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11, fontweight="bold")
    ax.set_ylim(0, max(accuracies) + 22 if accuracies else 100)
    ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

    mean_acc = np.mean(accuracies) if accuracies else 0
    ax.axhline(mean_acc, color="#64748B", linestyle=":", linewidth=1.5, label=f"Média Geral: {mean_acc:.2f}%", zorder=2)
    ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", framealpha=0.9)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Gráfico de Acurácia salvo em: {output_path}")

def plot_tokens_chart(
    model_name: str,
    datasets_data: List[Tuple[str, str, Dict[str, Any]]],
    output_path: str
):
    """Gera o gráfico de barras comparativo de Tokens Médios por Task."""
    labels = [d[0] for d in datasets_data]
    colors = [PALETTE.get(d[1], PALETTE["Default"]) for d in datasets_data]
    avg_tokens = [d[2]["avg_tokens"] for d in datasets_data]

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    x = np.arange(len(labels))
    width = 0.55

    bars = ax.bar(x, avg_tokens, width=width, color=colors, edgecolor="#1E293B", linewidth=1.2, zorder=3)

    for bar, tok in zip(bars, avg_tokens):
        y_val = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            y_val + max(avg_tokens) * 0.03,
            f"{tok:,.0f}\ntokens",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#0F172A",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", alpha=0.9, edgecolor="#E2E8F0", linewidth=0.8),
            zorder=4
        )

    ax.set_title(f"Consumo Médio de Tokens por Task - Modelo: {model_name}", fontsize=15, fontweight="bold", pad=20)
    ax.set_ylabel("Média de Tokens por Task", fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11, fontweight="bold")
    ax.set_ylim(0, max(avg_tokens) * 1.30 if avg_tokens else 1000)
    ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

    mean_tok = np.mean(avg_tokens) if avg_tokens else 0
    ax.axhline(mean_tok, color="#64748B", linestyle=":", linewidth=1.5, label=f"Média Geral: {mean_tok:,.0f}", zorder=2)
    ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", framealpha=0.9)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Gráfico de Tokens salvo em: {output_path}")

def plot_time_chart(
    model_name: str,
    datasets_data: List[Tuple[str, str, Dict[str, Any]]],
    output_path: str
):
    """Gera o gráfico de barras comparativo de Tempo Médio (s) por Task."""
    labels = [d[0] for d in datasets_data]
    colors = [PALETTE.get(d[1], PALETTE["Default"]) for d in datasets_data]
    avg_times = [d[2]["avg_time"] for d in datasets_data]

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

    x = np.arange(len(labels))
    width = 0.55

    bars = ax.bar(x, avg_times, width=width, color=colors, edgecolor="#1E293B", linewidth=1.2, zorder=3)

    for bar, tim in zip(bars, avg_times):
        y_val = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            y_val + max(avg_times) * 0.03,
            f"{tim:.2f}s",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#0F172A",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", alpha=0.9, edgecolor="#E2E8F0", linewidth=0.8),
            zorder=4
        )

    ax.set_title(f"Tempo Médio de Execução por Task - Modelo: {model_name}", fontsize=15, fontweight="bold", pad=20)
    ax.set_ylabel("Tempo Médio (segundos)", fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11, fontweight="bold")
    ax.set_ylim(0, max(avg_times) * 1.30 if avg_times else 10)
    ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

    mean_tim = np.mean(avg_times) if avg_times else 0
    ax.axhline(mean_tim, color="#64748B", linestyle=":", linewidth=1.5, label=f"Média Geral: {mean_tim:.2f}s", zorder=2)
    ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF", framealpha=0.9)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Gráfico de Tempo salvo em: {output_path}")

def plot_dashboard_all(
    model_name: str,
    datasets_data: List[Tuple[str, str, Dict[str, Any]]],
    output_path: str
):
    """
    Gera o Dashboard mestre 3-em-1 combinando Acurácia, Tokens e Tempo,
    além de tabela visual com os extremos (Mín/Máx) e mapeamento original.
    """
    labels = [d[0] for d in datasets_data]
    colors = [PALETTE.get(d[1], PALETTE["Default"]) for d in datasets_data]
    
    accuracies = [d[2]["accuracy_pct"] for d in datasets_data]
    counts = [(d[2]["correct_count"], d[2]["total_tasks"]) for d in datasets_data]
    avg_tokens = [d[2]["avg_tokens"] for d in datasets_data]
    avg_times = [d[2]["avg_time"] for d in datasets_data]

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig = plt.figure(figsize=(18, 12), dpi=300)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 0.9], hspace=0.35, wspace=0.25)

    ax_acc = fig.add_subplot(gs[0, 0])
    ax_tok = fig.add_subplot(gs[0, 1])
    ax_tim = fig.add_subplot(gs[0, 2])
    ax_tab = fig.add_subplot(gs[1, :])

    x = np.arange(len(labels))
    width = 0.55

    # 1. Gráfico de Acurácia
    bars_acc = ax_acc.bar(x, accuracies, width=width, color=colors, edgecolor="#1E293B", linewidth=1.1, zorder=3)
    for bar, acc, (corr, tot) in zip(bars_acc, accuracies, counts):
        ax_acc.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + 1.8,
            f"{acc:.1f}%\n({corr}/{tot})",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold"
        )
    ax_acc.set_title("Taxa de Acurácia (%)", fontsize=13, fontweight="bold", pad=12)
    ax_acc.set_ylabel("Acurácia (%)", fontsize=11, fontweight="semibold")
    ax_acc.set_xticks(x)
    ax_acc.set_xticklabels(labels, fontsize=10, fontweight="semibold", rotation=15)
    ax_acc.set_ylim(0, max(accuracies) + 18 if accuracies else 100)
    ax_acc.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

    # 2. Gráfico de Tokens
    bars_tok = ax_tok.bar(x, avg_tokens, width=width, color=colors, edgecolor="#1E293B", linewidth=1.1, zorder=3)
    for bar, tok in zip(bars_tok, avg_tokens):
        ax_tok.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + max(avg_tokens) * 0.02,
            f"{tok:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold"
        )
    ax_tok.set_title("Média de Tokens / Task", fontsize=13, fontweight="bold", pad=12)
    ax_tok.set_ylabel("Tokens", fontsize=11, fontweight="semibold")
    ax_tok.set_xticks(x)
    ax_tok.set_xticklabels(labels, fontsize=10, fontweight="semibold", rotation=15)
    ax_tok.set_ylim(0, max(avg_tokens) * 1.25 if avg_tokens else 1000)
    ax_tok.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

    # 3. Gráfico de Tempo
    bars_tim = ax_tim.bar(x, avg_times, width=width, color=colors, edgecolor="#1E293B", linewidth=1.1, zorder=3)
    for bar, tim in zip(bars_tim, avg_times):
        ax_tim.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + max(avg_times) * 0.02,
            f"{tim:.1f}s",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold"
        )
    ax_tim.set_title("Tempo Médio / Task (s)", fontsize=13, fontweight="bold", pad=12)
    ax_tim.set_ylabel("Segundos", fontsize=11, fontweight="semibold")
    ax_tim.set_xticks(x)
    ax_tim.set_xticklabels(labels, fontsize=10, fontweight="semibold", rotation=15)
    ax_tim.set_ylim(0, max(avg_times) * 1.25 if avg_times else 10)
    ax_tim.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

    # 4. Tabela de Detalhes dos Extremos (Min / Max com Task Original)
    ax_tab.axis("off")
    table_headers = [
        "Dataset",
        "Máx Tokens [CORRECT]\n(Task -> Orig)",
        "Mín Tokens [CORRECT]\n(Task -> Orig)",
        "Máx Tokens [INCORRECT]\n(Task -> Orig)",
        "Máx Tempo [CORRECT]\n(Task -> Orig)",
        "Mín Tempo [CORRECT]\n(Task -> Orig)",
        "Máx Tempo [INCORRECT]\n(Task -> Orig)"
    ]

    table_rows = []
    for label, _, data in datasets_data:
        def fmt_rec(r, is_time=False):
            if not r:
                return "N/A"
            v = f"{r['value']:.2f}s" if is_time else f"{r['value']:,}"
            tid = r['task_id'].replace('.json', '')
            orig = r['original_task'].replace('.json', '')
            return f"{v}\n({tid} -> {orig})"

        row = [
            label,
            fmt_rec(data["max_tok_corr"], False),
            fmt_rec(data["min_tok_corr"], False),
            fmt_rec(data["max_tok_incorr"], False),
            fmt_rec(data["max_tim_corr"], True),
            fmt_rec(data["min_tim_corr"], True),
            fmt_rec(data["max_tim_incorr"], True),
        ]
        table_rows.append(row)

    table = ax_tab.table(
        cellText=table_rows,
        colLabels=table_headers,
        cellLoc="center",
        loc="center",
        bbox=[0.0, 0.0, 1.0, 0.95]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    
    # Estilização das células da tabela
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor("#CBD5E1")
        if i == 0:
            cell.set_facecolor("#1E293B")
            cell.set_text_props(color="#FFFFFF", weight="bold")
            cell.set_height(0.22)
        else:
            cell.set_facecolor("#F8FAFC" if i % 2 == 0 else "#FFFFFF")
            cell.set_text_props(color="#0F172A")
            cell.set_height(0.18)

    fig.suptitle(
        f"ARC-AGI Benchmark Comparativo de Transformações - Modelo: {model_name}",
        fontsize=17,
        fontweight="bold",
        y=0.98,
        color="#0F172A"
    )

    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Dashboard Geral 3-em-1 salvo em: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Plotador de Benchmarks ARC-AGI (Acurácia, Tokens e Tempo)")
    parser.add_argument(
        "--model", "-m", default="Gemma",
        help="Nome do modelo ou subpasta em Results/ (ex: 'Gemma', 'Results/Gemma')"
    )
    parser.add_argument(
        "--metric", choices=["accuracy", "acerto", "tokens", "time", "tempo", "all"], default="all",
        help="Métrica para plotar: 'accuracy' (acertos), 'tokens', 'time' (tempo) ou 'all' (todos)"
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Diretório onde os gráficos serão salvos (padrão: Results/<model>/)"
    )
    
    args = parser.parse_args()

    # Normaliza caminho do modelo
    model_str = args.model.strip()
    if os.path.exists(model_str) and os.path.isdir(model_str):
        model_dir = model_str
        model_name = Path(model_dir).name
    else:
        model_dir = os.path.join("Results", model_str)
        model_name = model_str

    if not os.path.exists(model_dir):
        print(f"[!] Erro: Diretório do modelo '{model_dir}' não encontrado.")
        return

    out_dir = args.output_dir if args.output_dir else model_dir
    os.makedirs(out_dir, exist_ok=True)

    print(f"[+] Carregando mapeamento de tasks originais...")
    meta_map = load_metadata_mapping("New Tasks/transformed_tasks.csv")

    print(f"[+] Descobrindo datasets em '{model_dir}'...")
    dataset_dirs = discover_model_datasets(model_dir)

    if not dataset_dirs:
        print(f"[!] Nenhum dataset com planilhas de resultados encontrado em '{model_dir}'.")
        return

    print(f"[+] Extraindo métricas de {len(dataset_dirs)} pastas de datasets...")
    datasets_data = []
    for fpath, label, color_key in dataset_dirs:
        m = extract_dataset_metrics(fpath, meta_map)
        if m:
            datasets_data.append((label, color_key, m))

    if not datasets_data:
        print("[!] Nenhuma métrica válida pôde ser extraída.")
        return

    # Exibe resumo no terminal
    print_summary_table(model_name, datasets_data)

    metric = args.metric.lower()
    clean_model_name = model_name.lower().replace(" ", "_")

    # Geração dos gráficos solicitados
    if metric in ["accuracy", "acerto"]:
        plot_accuracy_chart(model_name, datasets_data, os.path.join(out_dir, f"benchmark_{clean_model_name}_accuracy.png"))
    elif metric in ["tokens"]:
        plot_tokens_chart(model_name, datasets_data, os.path.join(out_dir, f"benchmark_{clean_model_name}_tokens.png"))
    elif metric in ["time", "tempo"]:
        plot_time_chart(model_name, datasets_data, os.path.join(out_dir, f"benchmark_{clean_model_name}_times.png"))
    elif metric == "all":
        dash_path = os.path.join(out_dir, f"benchmark_{clean_model_name}_dashboard.png")
        plot_dashboard_all(model_name, datasets_data, dash_path)
        plot_accuracy_chart(model_name, datasets_data, os.path.join(out_dir, f"benchmark_{clean_model_name}_accuracy.png"))
        plot_tokens_chart(model_name, datasets_data, os.path.join(out_dir, f"benchmark_{clean_model_name}_tokens.png"))
        plot_time_chart(model_name, datasets_data, os.path.join(out_dir, f"benchmark_{clean_model_name}_times.png"))

    print("\n[+] Processamento concluído com sucesso!")

if __name__ == "__main__":
    main()
