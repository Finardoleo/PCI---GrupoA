# Benchmark ARC-AGI: Raciocínio Genuíno ou Memorização de Dados Públicos?
**Estudo Comparativo entre Gemma 4 (31B-IT) e Gemini 3.5 Flash Lite sob Perturbações Espaciais Equivariantes e Assimétricas**

* **Discentes:** Gabriel, Leonardo, Luis
* **Docentes & Avaliadores:** Prof. André, Profa. Érica, Prof. João, Prof. Frederico
* **Instituição:** Universidade Federal do Rio Grande do Sul (UFRGS) • Instituto de Informática • PCI

---

## 📌 Arquivos de Slides Criados
1. 📖 **[Versão Completa (Roteiro do Orador)](file:///c:/Users/Gabriel/Desktop/Escola_Trabalho/Faculdade/UFRGS/5%C2%B0_semestre/PCI/Projeto%201/PCI-GrupoA/Results/apresentacao_slides_benchmark_arc_completa.html)** — Com explicações aprofundadas, notas de fala para a banca, tabelas completas e detalhamento metodológico.
2. ⚡ **[Versão Enxuta (Apresentação Pública)](file:///c:/Users/Gabriel/Desktop/Escola_Trabalho/Faculdade/UFRGS/5%C2%B0_semestre/PCI/Projeto%201/PCI-GrupoA/Results/apresentacao_slides_benchmark_arc_resumida.html)** — Formato widescreen em tema Creme e Marrom, cartões visuais limpos, grids de matrizes, gráficos comparativos integrados e tópicos objetivos para projeção.

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

## 📑 Estrutura Lógica dos 16 Slides

1. **Slide 1 — Capa Oficial:** Apresentação do projeto, autores, professores e vínculo com a UFRGS.
2. **Slide 2 — O Desafio do ARC-AGI:** O benchmark de Chollet (2019) e o problema da ampla exposição pública das tarefas na internet.
3. **Slide 3 — A Pergunta Central de Pesquisa:** Raciocínio genuíno por operadores abstratos vs. memorização contextual e dependência canônica.
4. **Slide 4 — Metodologia Experimental em 2 Etapas:**
   * *Etapa 1 (High Thinking, $T=0.6$):* Cadeia de pensamento aberta e exploração dedutiva.
   * *Etapa 2 (Formatação Determinística, $T=0.0$, Minimal):* Extração estrita da matriz sem ruído sintático.
   * *A Matemática do Tempo:* Prova de que 99,9% do tempo medido corresponde à geração de tokens nas TPUs (150ms de RTT vs 250s de inferência).
5. **Slide 5 — As 4 Famílias de Transformação 2D (com Grids Visuais):**
   * *Rotação:* 90° CW, 180°, 90° CCW ($T_{\text{in}} = T_{\text{out}}$).
   * *Reflexão:* Espelhamento horizontal e vertical ($T_{\text{in}} = T_{\text{out}}$).
   * *Coloração:* Permutação bijetiva da paleta de cores, incluindo a cor de fundo 0 ($T_{\text{in}} = T_{\text{out}}$).
   * *Merged:* Combinação de 2 famílias distintas com transformações livres de entrada e saída ($T_{\text{in}} \neq T_{\text{out}}$).
6. **Slide 6 — Tabela Comparativa de Acurácia:** Dados numéricos lado a lado com deltas e tendências observadas.
7. **Slide 7 — Dashboard Visual Integrado:** Exibição da figura `benchmark_comparativo_gemma_vs_gemini.png` com os três gráficos de barras agrupadas.
8. **Slide 8 — Quem Acerta Mais vs. Quem é Mais Consistente:**
   * *Volume Bruto:* Gemma 31B vence em todos os cenários (+8.5 pp original, +8.6 pp merged).
   * *Consistência Simétrica:* Empate técnico em Rotação e Reflexão (diferença menor que 1,6 pp).
   * *Ponto de Ruptura:* Ambos sofrem colapso de 43 a 50 pontos percentuais no Merged.
9. **Slide 9 — Análise de Tokens de Raciocínio:**
   * Tasks corretas consomem ~9.700 a 10.600 tokens (convergência rápida da hipótese).
   * Tasks incorretas consomem ~15.500 a 16.200 tokens (loops exaustivos no espaço de busca).
10. **Slide 10 — Tempo e Throughput:**
    * Gemini 3.5 Flash Lite é 7x a 8x mais rápido (~32s vs ~255s por tarefa).
11. **Slide 11 — Estudo de Caso 1 (A "Regra Fantasma"):**
    * Na *Task f1cefba8*, o modelo escreveu textualmente no raciocínio a regra cíclica da base pública original (*"2 -> 3 -> 8 -> 2"*), mesmo após essa regra ter sido removida no JSON transformado, evidenciando recuperação direta de pré-treino.
12. **Slide 12 — Estudo de Caso 2 (Falhas Espaciais e Viés Canônico):**
    * *Task 0ac8ac11:* Inversão de índices de colunas e erro de alturas em reflexão.
    * *Task f7cb8069:* Desvio na coordenada da 2ª reta vertical (coluna 7 em vez de 5).
    * *Task 04e656f5:* Erro dimensional severo (quadrado 5x5 em vez de retângulo 10x4).
13. **Slide 13 — Discussão e Hipóteses Explicativas:**
    * *Operadores Parciais:* Heurísticas funcionais para simetrias regulares.
    * *Viés Canônico:* Tendência de leitura linear *Left-to-Right* e *Top-to-Bottom*.
    * *Limite Composicional:* Explosão combinatória quando regras livres são compostas.
14. **Slide 14 — Cuidados Metodológicos e Rigor Epistêmico:**
    * Postura científica cautelosa (tratar os achados como indícios e hipóteses comportamentais).
15. **Slide 15 — Conclusão Geral:**
    * O sucesso no ARC-AGI público superestima a capacidade de raciocínio livre de contexto.
16. **Slide 16 — Próximos Passos:**
    * **Desenvolvimento do Artigo Final no Overleaf.**
    * Avaliação de modelos de maior escala (Gemini 2.5 / 3.1 Pro).
    * Mecanismos de auto-verificação em tempo de inferência (*Test-Time Scaling*).
