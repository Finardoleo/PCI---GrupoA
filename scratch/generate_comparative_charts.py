import os
import matplotlib.pyplot as plt
import numpy as np

# Palette: Creme & Marrom (Tema do projeto)
COLOR_GEMMA = '#443224'     # Deep Espresso Brown
COLOR_GEMINI = '#B86728'    # Warm Cognac / Caramel
EDGE_COLOR = '#261B14'      # Dark Border
BG_COLOR = '#FAF6F0'        # Soft Cream
GRID_COLOR = '#E5DCD1'      # Subtle Cream Border
TEXT_DARK = '#261B14'       # Deep Brown Text
TEXT_MUTED = '#5A4C40'      # Muted Brown Text

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

datasets = ['Original (Treino)', 'Rotated', 'Reflected', 'Coloration', 'Merged']

# 1. ACURÁCIA (ORIGINAL - TOTAL DE TASKS AVALIADAS EM CADA MODELO)
acc_gemma_orig = [76.00, 87.17, 87.50, 89.14, 44.50]
acc_gemini_orig = [67.50, 85.56, 87.04, 84.44, 35.93]
counts_gemma_orig = [(304, 400), (265, 304), (266, 304), (271, 304), (263, 591)]
counts_gemini_orig = [(270, 400), (231, 270), (235, 270), (228, 270), (194, 540)]

# 2. TOKENS (INTERSECÇÃO DE TASKS COMPARTILHADAS N=252)
tok_gemma_inter = [9856.1, 9851.3, 9732.0, 9923.4, 11537.0]
tok_gemini_inter = [9462.6, 8944.5, 8918.5, 8991.8, 10504.4]

# 3. TEMPO (INTERSECÇÃO DE TASKS COMPARTILHADAS N=252)
time_gemma_inter = [208.1, 222.4, 218.9, 227.9, 285.1]
time_gemini_inter = [27.5, 31.3, 28.7, 28.0, 32.5]
speedups_inter = [f"{g/m:.1f}×" for g, m in zip(time_gemma_inter, time_gemini_inter)]

out_dir = 'Results'
os.makedirs(out_dir, exist_ok=True)

def style_axis(ax):
    ax.set_facecolor('#FFFFFF')
    ax.grid(axis='y', linestyle='--', alpha=0.6, color=GRID_COLOR, zorder=0)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.tick_params(colors=TEXT_DARK)

# -----------------------------------------------------------------------------
# 1. COMPARATIVO DE ACURÁCIA (ORIGINAL - GERAL)
# -----------------------------------------------------------------------------
def plot_comparativo_acuracia():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300, facecolor=BG_COLOR)
    style_axis(ax)
    x = np.arange(len(datasets))
    w = 0.36

    r1 = ax.bar(x - w/2, acc_gemma_orig, w, label='Gemma 4 (31B-IT)', color=COLOR_GEMMA, edgecolor=EDGE_COLOR, linewidth=1.1, zorder=3)
    r2 = ax.bar(x + w/2, acc_gemini_orig, w, label='Gemini 3.5 Flash Lite', color=COLOR_GEMINI, edgecolor=EDGE_COLOR, linewidth=1.1, zorder=3)

    for i, (b1, b2) in enumerate(zip(r1, r2)):
        ax.text(b1.get_x() + b1.get_width()/2, b1.get_height() + 1.8, f"{acc_gemma_orig[i]:.2f}%",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=TEXT_DARK)
        ax.text(b2.get_x() + b2.get_width()/2, b2.get_height() + 1.8, f"{acc_gemini_orig[i]:.2f}%",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_GEMINI)

    ax.set_title('Taxa de Acurácia ARC-AGI (%) por Dataset', fontsize=14, fontweight='bold', pad=18, color=TEXT_DARK)
    ax.set_ylabel('Acurácia (%)', fontsize=12, fontweight='bold', color=TEXT_MUTED)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 108)
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor=GRID_COLOR, framealpha=0.95, fontsize=10.5)

    plt.tight_layout()
    path = os.path.join(out_dir, 'comparativo_acuracia.png')
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"[+] Salvo: {path}")

# -----------------------------------------------------------------------------
# 2. COMPARATIVO DE TOKENS (INTERSECÇÃO N=252)
# -----------------------------------------------------------------------------
def plot_comparativo_tokens():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300, facecolor=BG_COLOR)
    style_axis(ax)
    x = np.arange(len(datasets))
    w = 0.36

    r1 = ax.bar(x - w/2, tok_gemma_inter, w, label='Gemma 4 (31B-IT)', color=COLOR_GEMMA, edgecolor=EDGE_COLOR, linewidth=1.1, zorder=3)
    r2 = ax.bar(x + w/2, tok_gemini_inter, w, label='Gemini 3.5 Flash Lite', color=COLOR_GEMINI, edgecolor=EDGE_COLOR, linewidth=1.1, zorder=3)

    for i, (b1, b2) in enumerate(zip(r1, r2)):
        ax.text(b1.get_x() + b1.get_width()/2, b1.get_height() + 200, f"{tok_gemma_inter[i]:,.0f}",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=TEXT_DARK)
        ax.text(b2.get_x() + b2.get_width()/2, b2.get_height() + 200, f"{tok_gemini_inter[i]:,.0f}",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_GEMINI)

    ax.set_title('Consumo Médio de Tokens de Pensamento — Intersecção de Tasks Compartilhadas (N=252)', fontsize=13, fontweight='bold', pad=18, color=TEXT_DARK)
    ax.set_ylabel('Média de Tokens por Task', fontsize=12, fontweight='bold', color=TEXT_MUTED)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=11, fontweight='bold')
    ax.set_ylim(0, max(tok_gemma_inter) * 1.25)
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor=GRID_COLOR, framealpha=0.95, fontsize=10.5)

    plt.tight_layout()
    path = os.path.join(out_dir, 'comparativo_tokens.png')
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"[+] Salvo: {path}")

# -----------------------------------------------------------------------------
# 3. COMPARATIVO DE TEMPO (INTERSECÇÃO N=252)
# -----------------------------------------------------------------------------
def plot_comparativo_tempo():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300, facecolor=BG_COLOR)
    style_axis(ax)
    x = np.arange(len(datasets))
    w = 0.36

    r1 = ax.bar(x - w/2, time_gemma_inter, w, label='Gemma 4 (31B-IT)', color=COLOR_GEMMA, edgecolor=EDGE_COLOR, linewidth=1.1, zorder=3)
    r2 = ax.bar(x + w/2, time_gemini_inter, w, label='Gemini 3.5 Flash Lite', color=COLOR_GEMINI, edgecolor=EDGE_COLOR, linewidth=1.1, zorder=3)

    for i, (b1, b2) in enumerate(zip(r1, r2)):
        ax.text(b1.get_x() + b1.get_width()/2, b1.get_height() + 4, f"{time_gemma_inter[i]:.1f}s",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=TEXT_DARK)
        ax.text(b2.get_x() + b2.get_width()/2, b2.get_height() + 4, f"{time_gemini_inter[i]:.1f}s\n({speedups_inter[i]})",
                ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_GEMINI)

    ax.set_title('Tempo Médio de Inferência Pura (s) — Intersecção de Tasks Compartilhadas (N=252)', fontsize=13, fontweight='bold', pad=18, color=TEXT_DARK)
    ax.set_ylabel('Tempo Médio (segundos)', fontsize=12, fontweight='bold', color=TEXT_MUTED)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=11, fontweight='bold')
    ax.set_ylim(0, max(time_gemma_inter) * 1.25)
    ax.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor=GRID_COLOR, framealpha=0.95, fontsize=10.5)

    plt.tight_layout()
    path = os.path.join(out_dir, 'comparativo_tempo.png')
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"[+] Salvo: {path}")

# -----------------------------------------------------------------------------
# 4. DASHBOARD 3-EM-1 (ACURÁCIA GERAL + TOKENS/TEMPO INTERSECÇÃO)
# -----------------------------------------------------------------------------
def plot_dashboard_completo():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.8), dpi=300, facecolor=BG_COLOR)
    x = np.arange(len(datasets))
    w = 0.38

    # Subplot 1: Acurácia Geral
    style_axis(ax1)
    r1_acc = ax1.bar(x - w/2, acc_gemma_orig, w, label='Gemma 4 (31B-IT)', color=COLOR_GEMMA, edgecolor=EDGE_COLOR, linewidth=1.0, zorder=3)
    r2_acc = ax1.bar(x + w/2, acc_gemini_orig, w, label='Gemini 3.5 Flash Lite', color=COLOR_GEMINI, edgecolor=EDGE_COLOR, linewidth=1.0, zorder=3)
    for i, (b1, b2) in enumerate(zip(r1_acc, r2_acc)):
        ax1.text(b1.get_x() + b1.get_width()/2, b1.get_height() + 1.5, f"{acc_gemma_orig[i]:.1f}%",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=TEXT_DARK)
        ax1.text(b2.get_x() + b2.get_width()/2, b2.get_height() + 1.5, f"{acc_gemini_orig[i]:.1f}%",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=COLOR_GEMINI)
    ax1.set_title('Taxa de Acurácia (%)', fontsize=13, fontweight='bold', pad=14, color=TEXT_DARK)
    ax1.set_ylabel('Acurácia (%)', fontsize=11, fontweight='bold', color=TEXT_MUTED)
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets, fontsize=9.5, fontweight='bold', rotation=15)
    ax1.set_ylim(0, 108)
    ax1.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor=GRID_COLOR, framealpha=0.9, fontsize=9.5)

    # Subplot 2: Tokens (Intersecção)
    style_axis(ax2)
    r1_tok = ax2.bar(x - w/2, tok_gemma_inter, w, label='Gemma 4 (31B-IT)', color=COLOR_GEMMA, edgecolor=EDGE_COLOR, linewidth=1.0, zorder=3)
    r2_tok = ax2.bar(x + w/2, tok_gemini_inter, w, label='Gemini 3.5 Flash Lite', color=COLOR_GEMINI, edgecolor=EDGE_COLOR, linewidth=1.0, zorder=3)
    for i, (b1, b2) in enumerate(zip(r1_tok, r2_tok)):
        ax2.text(b1.get_x() + b1.get_width()/2, b1.get_height() + 180, f"{tok_gemma_inter[i]:,.0f}",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=TEXT_DARK)
        ax2.text(b2.get_x() + b2.get_width()/2, b2.get_height() + 180, f"{tok_gemini_inter[i]:,.0f}",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=COLOR_GEMINI)
    ax2.set_title('Média Tokens (Intersecção N=252)', fontsize=13, fontweight='bold', pad=14, color=TEXT_DARK)
    ax2.set_ylabel('Tokens de Pensamento', fontsize=11, fontweight='bold', color=TEXT_MUTED)
    ax2.set_xticks(x)
    ax2.set_xticklabels(datasets, fontsize=9.5, fontweight='bold', rotation=15)
    ax2.set_ylim(0, max(tok_gemma_inter) * 1.25)
    ax2.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor=GRID_COLOR, framealpha=0.9, fontsize=9.5)

    # Subplot 3: Tempo (Intersecção)
    style_axis(ax3)
    r1_tim = ax3.bar(x - w/2, time_gemma_inter, w, label='Gemma 4 (31B-IT)', color=COLOR_GEMMA, edgecolor=EDGE_COLOR, linewidth=1.0, zorder=3)
    r2_tim = ax3.bar(x + w/2, time_gemini_inter, w, label='Gemini 3.5 Flash Lite', color=COLOR_GEMINI, edgecolor=EDGE_COLOR, linewidth=1.0, zorder=3)
    for i, (b1, b2) in enumerate(zip(r1_tim, r2_tim)):
        ax3.text(b1.get_x() + b1.get_width()/2, b1.get_height() + 3.5, f"{time_gemma_inter[i]:.1f}s",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=TEXT_DARK)
        ax3.text(b2.get_x() + b2.get_width()/2, b2.get_height() + 3.5, f"{time_gemini_inter[i]:.1f}s\n({speedups_inter[i]})",
                 ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=COLOR_GEMINI)
    ax3.set_title('Tempo Médio (s) (Intersecção N=252)', fontsize=13, fontweight='bold', pad=14, color=TEXT_DARK)
    ax3.set_ylabel('Segundos', fontsize=11, fontweight='bold', color=TEXT_MUTED)
    ax3.set_xticks(x)
    ax3.set_xticklabels(datasets, fontsize=9.5, fontweight='bold', rotation=15)
    ax3.set_ylim(0, max(time_gemma_inter) * 1.25)
    ax3.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor=GRID_COLOR, framealpha=0.9, fontsize=9.5)

    fig.suptitle('ARC-AGI Benchmark Comparativo — Gemma 4 (31B) vs Gemini 3.5 Flash Lite',
                 fontsize=15, fontweight='bold', y=0.98, color=TEXT_DARK)

    plt.tight_layout()
    path = os.path.join(out_dir, 'benchmark_comparativo_gemma_vs_gemini.png')
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"[+] Salvo: {path}")

if __name__ == '__main__':
    plot_comparativo_acuracia()
    plot_comparativo_tokens()
    plot_comparativo_tempo()
    plot_dashboard_completo()
