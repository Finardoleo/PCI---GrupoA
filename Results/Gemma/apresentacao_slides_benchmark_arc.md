# 📊 Apresentação: A Robustez de LLMs sob Perturbações Espaciais no ARC-AGI

**Investigando Memorização, Viés Geométrico e Degradação de Raciocínio em Modelos com Chain of Thought (Gemma 31B)**

* **Instituição:** Universidade Federal do Rio Grande do Sul (UFRGS) - Bacharelado em Ciência da Computação
* **Disciplina:** PCI - Projeto em Ciência e Inovação
* **Alunos:** Gabriel, Leonardo e Luis
* **Professores:** André, Érica, João e Frederico
* **Modelo Avaliado:** `gemma-4-31b-it` com *High Thinking Process*
* **Amostras:** Mais de 1.600 inferências avaliadas

---

## 🎯 Sumário Executivo dos Resultados

```
+-------------------+---------+------------------+----------------+------------------+
| Dataset           | Tasks   | Acurácia (%)     | Média Tokens   | Média Tempo (s)  |
+-------------------+---------+------------------+----------------+------------------+
| Original (Treino) | 400     | 76.00% (304/400) | 12.810,7       | 262,56s          |
| Reflected         | 304     | 70.39% (214/304) | 13.644,6       | 304,00s          |
| Rotated           | 304     | 61.18% (186/304) | 15.420,0       | 320,92s          |
| Merged            | 591     | 44.50% (263/591) | 16.221,9       | 369,76s          |
+-------------------+---------+------------------+----------------+------------------+
```

---

## 📑 Estrutura Completa dos Slides

---

### SLIDE 1: Capa
* **Título Principal:** A Robustez de LLMs sob Perturbações Espaciais no ARC-AGI
* **Subtítulo:** Investigando Memorização, Viés Geométrico e Degradação de Raciocínio em Modelos com Chain of Thought (Gemma 31B)
* **Identificação:**
  * **Alunos:** Gabriel, Leonardo e Luis
  * **Professores:** André, Érica, João e Frederico
  * **Curso:** Bacharelado em Ciência da Computação — UFRGS

---

### SLIDE 2: Metodologia e Pipeline em 2 Etapas
* **Isolamento de Raciocínio (`solver.py`):**
  1. **Etapa 1 (High Thinking / CoT):** Temperatura $T = 0.6$, limite de 16k tokens. O modelo explora hipóteses e deduções espaciais profundas (~200s a 800s).
  2. **Etapa 2 (Extração Numérica - Thinking: MINIMAL):** Temperatura $T = 0.0$ (determinístico/greedy). Apenas formata o grid numérico final no bloco `<prediction>` sem nova carga de raciocínio (~4s).
* **Isolamento Amostral Rigoroso:**
  * Apenas os **304 problemas acertados** pelo Gemma no dataset original foram submetidos às perturbações, garantindo que qualquer erro subsequente seja atribuído à perturbação e não à incapacidade prévia do modelo.
* **Pool Paralelo Multi-Chaves:** 4 chaves API com Circuit Breaker isolando cotas (16K TPM).

---

### SLIDE 3: Mecanismo das Transformações 2D (`task_generator.py`)
* **Como as matrizes foram manipuladas mantendo a lógica solucionável:**

#### 1. Rotação Espacial (90° CW, 180°, 270°)
```
Original:       →   Rotacionado 90° Horário:
1 2 0               0 4 1
4 5 0               0 5 2
0 0 0               0 0 0
```
*Gira todo o espaço 2D preservando a vizinhança topológica relativa.*

#### 2. Reflexão / Espelhamento (Horizontal e Vertical)
```
Original:       →   Espelhado Horizontalmente:
1 2 0               0 2 1
4 0 0               0 0 4
3 3 0               0 3 3
```
*Inverte a ordem das colunas ou linhas, testando a orientação esquerda-direita e cima-baixo.*

#### 3. Permutação Bijetiva de Cores
```
Original:       →   Cores Trocadas [1→7, 2→3]:
1 1 2               7 7 3
0 2 0               0 3 0
2 0 1               3 0 7
```
*Permuta os valores numéricos da paleta, preservando o valor neutro de fundo (0).*

#### 4. Transformações Compostas (Merged)
```
Original:       →   Giro 90° CW + Cores [1→7, 2→4, 3→8]:
1 2 0               0 0 7
0 3 0               0 8 4
0 0 0               0 0 0
```
*Combinação não-linear de 2 famílias de transformação aplicadas deterministicamente em todos os exemplos de treino e teste.*

---

### SLIDE 4: Resultados Globais e Queda de Desempenho
* **Acurácia Base:** 76.00% (304/400 acertos).
* **Impacto das Perturbações (apenas sobre as 304 tasks antes acertadas):**
  * **Reflected:** Queda de 5,61 pontos percentuais $\rightarrow$ **70.39%**
  * **Rotated:** Queda de 14,82 pontos percentuais $\rightarrow$ **61.18%**
  * **Merged (Compostas):** Queda de 31,50 pontos percentuais $\rightarrow$ **44.50%**
* **Insight Chave:** O modelo não possui invariância espacial topológica real; transformações geométricas elementares quebram o raciocínio do LLM.

---

### SLIDE 5: Dashboard Visual 3-em-1
* **Acurácia, Volume de Pensamento (Tokens) e Tempo de Inferência:**
  * Original: `76.00%` | `12.811` tokens méd. | `262,56s`
  * Reflected: `70.39%` | `13.645` tokens méd. | `304,00s`
  * Rotated: `61.18%` | `15.420` tokens méd. | `320,92s`
  * Merged: `44.50%` | `16.222` tokens méd. | `369,76s`
* **Inference-Time Compute Scaling:** Conforme a complexidade da perturbação aumenta, o modelo consome significativamente mais tokens de raciocínio (+26.6%) e tempo (+40.8%) para navegar por árvores de hipóteses conflitantes.

---

### SLIDE 6: Hipótese 1 - Prior Memorization Override (Contaminação de Treino)
* **Teoria:** LLMs são expostos a repositórios do ARC-AGI durante o pré-treinamento. Ao reconhecer o formato de um problema, o modelo recupera a regra memorizada em vez de induzi-la das demonstrações no prompt.
* **Evidência Experimental:** Em tarefas modificadas, o modelo expressa no raciocínio textual a regra da tarefa original e aplica valores antigos, ignorando as novas demonstrações fornecidas no JSON.

---

### SLIDE 7: Estudo de Caso 1 - Merged Task `d965528e.json` (Original `f1cefba8.json`)
* **Texto Gerado pelo LLM Reasoning:**
  > *"Transpose the grid. The inner rectangle of the output takes the color of the input's outer rectangle (A). The outer rectangle of the output takes a transformed color of the input's inner rectangle (B), **following the cycle 2 -> 3 -> 8 -> 2** (and 4 -> 4)."*
* **O Erro Fatal:** O ciclo `2 -> 3 -> 8 -> 2` era a regra da **task original**! Na nova task gerada, as cores foram permutadas e o ciclo não existia mais. O modelo memorizou a regra canônica e a aplicou cegamente, errando o resultado final.
* **Erros Tipográficos Adicionais:** O modelo "comeu" números na parede esquerda (`0 0 0 2 1 1...` em vez de `0 0 0 2 2 1...`), quebrando a continuidade da forma.

---

### SLIDE 8: Hipótese 2 - Viés de Fechamento Geométrico (Gestalt Prior)
* **Teoria:** LLMs treinados em matrizes sofrem de viés indutivo de fechamento topológico: assumem que pontos esparsos devem formar figuras fechadas (caixas/retângulos).
* **Estudo de Caso na Task Rotacionada:**
  * **Regra Real:** Conectar pontos colineares da mesma cor.
  * **Coordenadas de Entrada:** `(3,6)`, `(15,6)` e `(15,21)`.
  * **Forma Geométrica Correta:** Um formato exato de **"L"**.
  * **Alucinação do Modelo:** O modelo inventou conexões na linha 3 e na coluna 21, desenhando um **retângulo fechado inteiro** onde não havia colinearidade.

---

### SLIDE 9: Hipótese 3 - Discretização e Erros de Coordenadas sob Reflexão
* **Estudo de Caso na Task Refletida `0ac8ac11.json`:**
  * **Regra Textual Deduzida:** Perfeita (*"Identificar colunas com a cor 5, ordenar por altura decrescente e substituir por 1, 2, 3 e 4"*).
  * **Falha de Execução no Grid:**
    1. **Posições Incorretas:** Desenhou colunas nas posições `0, 2, 4 e 7` (as reais eram `1, 3, 5 e 7`).
    2. **Erro de Altura (+1 pixel):** Desenhou alturas `9, 8, 6 e 4` (as reais eram `8, 7, 5 e 3`).
    3. **Inversão de Ranking:** Confundiu o ranking da coluna espelhada.
* **Insight:** LLMs conseguem expressar raciocínio abstrato em linguagem natural, mas falham na discretização espacial fina e indexação matricial.

---

### SLIDE 10: Conclusões e Próximos Passos
1. **Ausência de Invariância Espacial:** O desempenho em ARC-AGI é fortemente dependente da orientação canônica dos dados de treino (queda de até **31,5 pontos percentuais**).
2. **Contaminação de Treino como Muleta:** A acurácia original de 76% é inflada pela memorização prévia dos benchmarks.
3. **Próximos Passos:** Executar o mesmo pipeline experimental e de transformações para o modelo **Gemini 2.5/3.5 Flash Lite**, permitindo comparar diretamente o grau de dependência de memorização vs. capacidade de raciocínio espacial entre modelos de arquiteturas e portes distintos.
