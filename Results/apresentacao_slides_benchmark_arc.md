# Benchmark ARC-AGI: Raciocínio Genuíno ou Memorização de Dados Públicos?
**Estudo Comparativo entre Gemma 4 (31B-IT) e Gemini 3.5 Flash Lite sob Perturbações Espaciais Equivariantes e Assimétricas**

* **Discentes:** Gabriel, Leonardo, Luis
* **Docentes & Avaliadores:** Prof. André, Profa. Érica, Prof. Frederico, Prof. João
* **Instituição:** Universidade Federal do Rio Grande do Sul (UFRGS) • Instituto de Informática • Projeto em Ciência e Inovação (PCI)

---

## 📌 Links dos Slides Interativos em HTML
* 📖 **[Versão Completa com Roteiro do Orador](file:///c:/Users/Gabriel/Desktop/Escola_Trabalho/Faculdade/UFRGS/5%C2%B0_semestre/PCI/Projeto%201/PCI-GrupoA/Results/apresentacao_slides_benchmark_arc_completa.html)**
* ⚡ **[Versão Enxuta / Apresentação Pública (Light Mode)](file:///c:/Users/Gabriel/Desktop/Escola_Trabalho/Faculdade/UFRGS/5%C2%B0_semestre/PCI/Projeto%201/PCI-GrupoA/Results/apresentacao_slides_benchmark_arc_resumida.html)**

---

## 📊 Tabela Comparativa de Desempenho Oficial

| Dataset Avaliado | Tasks Gemma | Acurácia Gemma (31B) | Tasks Gemini | Acurácia Gemini (Flash Lite) | Diferença (p.p.) | Tokens Médios (Tasks Corretas) | Tempo Médio por Task |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Original (Treino ARC)** | 400 | **76.00%** (304/400) | 400 | **67.50%** (270/400) | **+8.50 pp** | 10.670 vs 9.755 | 262,6s vs 35,5s |
| **Rotated ($T_{\text{in}} = T_{\text{out}}$)** | 304 | **87.17%** (265/304) | 270 | **85.56%** (231/270) | **+1.62 pp** | 10.225 vs 8.983 | 255,3s vs 35,6s |
| **Reflected ($T_{\text{in}} = T_{\text{out}}$)** | 304 | **87.50%** (266/304) | 270 | **87.04%** (235/270) | **+0.46 pp** | 10.216 vs 9.177 | 246,7s vs 32,1s |
| **Coloration ($T_{\text{in}} = T_{\text{out}}$)** | 304 | **89.14%** (271/304) | 270 | **84.44%** (228/270) | **+4.70 pp** | 10.464 vs 9.162 | 253,3s vs 31,8s |
| **Merged (Composto & Livre)** | 591 | **44.50%** (263/591) | 540 | **35.93%** (194/540) | **+8.57 pp** | 11.672 vs 10.494 | 369,8s vs 46,9s |

---

## 📑 Resumo da Estrutura dos 16 Slides

1. **Slide 1 — Capa Oficial:** Autoria (Gabriel, Leonardo, Luis), Professores (André, Érica, Frederico, João) e afiliação com a UFRGS.
2. **Slide 2 — O Desafio do ARC-AGI:** François Chollet (2019) e o risco de contaminação prévia decorrente da disponibilidade pública das 400 tarefas de treino na internet.
3. **Slide 3 — A Pergunta Central de Pesquisa:** Indução lógica pura vs. memorização contextual e dependência de canonicidade.
4. **Slide 4 — Metodologia Experimental em 2 Etapas:**
   * *Etapa 1 (High Thinking, $T=0.6$):* Cadeia de pensamento livre explorando hipóteses espaciais.
   * *Etapa 2 (Formatação Determinística, $T=0.0$, Minimal):* Extração estrita do grid numérico.
   * *A Matemática do Tempo:* Prova de que $>99.9\%$ do tempo medido corresponde ao esforço de inferência das TPUs (RTT de ~150ms vs ~250s de computação).
5. **Slide 5 — As 4 Famílias de Transformação 2D (com Grids Visuais):**
   * *Rotação:* 90° CW, 180°, 90° CCW ($T_{\text{in}} = T_{\text{out}}$).
   * *Reflexão:* Espelhamento horizontal e vertical ($T_{\text{in}} = T_{\text{out}}$).
   * *Coloração:* Permutação 1:1 incluindo a cor de fundo 0 ($T_{\text{in}} = T_{\text{out}}$).
   * *Merged:* Rotação 90° CW + Coloração de paleta mantendo coerência geométrica.
6. **Slide 6 — Tabela Comparativa de Acurácia:** Dados consolidados com deltas e tendências observadas.
7. **Slide 7 — Explorador Interativo de Gráficos:** Abas interativas para alternar entre *Visão 3-em-1*, *Taxa de Acurácia*, *Tokens de Pensamento*, *Tempo de Execução*, *Dashboard Gemma* e *Dashboard Gemini*.
8. **Slide 8 — Quem Acerta Mais vs. Quem é Mais Consistente:**
   * *Volume Bruto:* Gemma 31B lidera em todos os datasets (+8.5 pp original, +8.6 pp merged).
   * *Consistência Simétrica:* Empate técnico em Rotação e Reflexão (diferença menor que 1,6 pp).
   * *Ponto de Ruptura:* Ambos sofrem colapso de 43 a 50 pontos percentuais no Merged.
9. **Slide 9 — Análise de Tokens de Pensamento por Modelo:**
   * *Gemma 31B:* 10.464 tokens (corretas) vs. 16.221 tokens (incorretas) [Pico de 39.623].
   * *Gemini 3.5 Flash Lite:* 9.162 tokens (corretas) vs. 15.586 tokens (incorretas) [Pico de 33.643].
   * *Insight:* Economia de 35% a 40% de tokens ao acertar; loops exaustivos ao falhar.
10. **Slide 10 — Tempo e Throughput:**
    * Gemini 3.5 Flash Lite opera 7x a 8x mais rápido (~32s vs ~255s por tarefa).
11. **Slide 11 — Estudo de Caso 1 (A "Regra Fantasma"):**
    * Na *Task f1cefba8*, o modelo reproduziu a regra antiga do dataset público no texto de raciocínio (*"cycle 2 -> 3 -> 8 -> 2"*), mesmo após essa regra ter sido removida no JSON transformado.
12. **Slide 12 — Estudo de Caso 2 (Falhas Espaciais e Viés Canônico):**
    * *Task 0ac8ac11:* Inversão de índices de colunas e alturas em reflexão.
    * *Task f7cb8069:* Desvio métrico na segunda reta vertical (coluna 7 em vez de 5).
    * *Task 04e656f5:* Falha dimensional severa (quadrado 5x5 em vez de retângulo 10x4).
13. **Slide 13 — Discussão e Hipóteses Explicativas (Cautela Epistêmica):**
    * *Operadores Parciais:* Modelos podem ter desenvolvido representações heurísticas para simetrias regulares.
    * *Viés Canônico:* A estrutura sequencial pode induzir preferências por leitura Top-to-Bottom e Left-to-Right.
    * *Limite Composicional:* A combinação livre de operadores pode sobrecarregar a busca dedutiva.
14. **Slide 14 — Cuidados Metodológicos e Rigor Científico:**
    * Postura cautelosa tratando as conclusões como indícios comportamentais observáveis.
15. **Slide 15 — Conclusões Finais:**
    * O sucesso atual no ARC reflete um regime híbrido entre heurísticas geométricas elementares e memorização de configurações canônicas.
16. **Slide 16 — Próximos Passos:**
    * **1. Redação do Artigo Final no Overleaf.**
    * **2. Implementação de Mecanismos de Auto-Verificação em Tempo de Inferência.**
    * **3. Apresentação e Defesa na Disciplina de PCI (UFRGS).**
