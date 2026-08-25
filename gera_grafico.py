import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Criação do DataFrame com os Tempos por Task (segundos) - 10 Tasks exatas
dados_tasks = {
    "Task": [
        "3aa6fb7a", "44d8ac46", "44f52bb0", "0a938d79", "0b148d64", 
        "00576224", "0a1d4ef5", "0b17323b", "0bb8deee", "0becf7df"
    ],
    "gemma-4-31b-it": [
        244.16, 315.47, 186.48, 380.39, 232.58, 
        194.39, 266.02, 170.22, 249.02, 327.94
    ],
    "gemma-4-26b-a4b-it": [
        378.67, 377.28, 235.71, 377.40, 376.91, 
        224.67, 396.81, 377.80, 376.84, 269.03
    ],
    "gemini-3.5-flash-lite": [
        35.70, 35.18, 36.14, 37.53, 35.30, 
        34.83, 36.28, 49.83, 35.25, 37.65
    ],
    "gemini-flash-lite (metade)": [
        35.57, 34.31, 56.07, 36.08, 35.98, 
        51.77, 35.36, 58.95, 34.19, 36.97
    ]
}
df_tasks = pd.DataFrame(dados_tasks)

# 2. Criação do DataFrame para o Tempo Total (segundos)
dados_totais = {
    "Modelo": [
        "gemma-4-31b-it", 
        "gemma-4-26b-a4b-it", 
        "gemini-3.5-flash-lite", 
        "gemini-flash-lite (metade)"
    ],
    "Tempo Total": [2567.28, 3392.92, 374.31, 415.76]
}
df_total = pd.DataFrame(dados_totais)

# 3. Configuração da Figura
fig, axes = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={'width_ratios': [3, 1]})

# --- Subplot 1: Tempos Individuais (Barras Agrupadas) ---
df_tasks.set_index("Task").plot(kind="bar", ax=axes[0], width=0.8, colormap="viridis")
axes[0].set_title("Comparativo de Tempo por Task", fontsize=14, fontweight='bold', pad=15)
axes[0].set_ylabel("Tempo (segundos)", fontsize=12)
axes[0].set_xlabel("Nome da Task", fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', linestyle='--', alpha=0.7)
axes[0].legend(title="Modelos")

# --- Subplot 2: Tempo Total do Batch (Barras Individuais) ---
cores = plt.cm.viridis([0, 0.33, 0.66, 0.99])
axes[1].bar(df_total["Modelo"], df_total["Tempo Total"], color=cores)
axes[1].set_title("Tempo Total do Batch", fontsize=14, fontweight='bold', pad=15)
axes[1].set_ylabel("Tempo Total (segundos)", fontsize=12)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

# 4. Ajustes Finais e Renderização
plt.tight_layout()
os.makedirs("Results", exist_ok=True)
plt.savefig("Results/benchmark_modelos_arc.png", dpi=300)
plt.show()