# Benchmark ARC-AGI: Raciocínio Genuíno ou Memorização de Dados Públicos?
**Estudo Comparativo entre Gemma 4 (31B-IT) e Gemini 3.5 Flash Lite sob Perturbações Espaciais Equivariantes e Assimétricas**

* **Discentes:** Gabriel, Leonardo, Luis
* **Docentes & Avaliadores:** Prof. André, Profa. Érica, Prof. Frederico, Prof. João
* **Instituição:** Universidade Federal do Rio Grande do Sul (UFRGS) • Instituto de Informática • Projeto em Ciência e Inovação (PCI)

---

## 📌 Links dos Slides Interativos em HTML
* 📖 **[Versão Completa com Roteiro do Orador](file:///c:/Users/Gabriel/Desktop/Escola_Trabalho/Faculdade/UFRGS/5%C2%B0_semestre/PCI/Projeto%201/PCI-GrupoA/Results/apresentacao_slides_benchmark_arc_completa.html)**
* ⚡ **[Versão Enxuta / Apresentação Pública](file:///c:/Users/Gabriel/Desktop/Escola_Trabalho/Faculdade/UFRGS/5%C2%B0_semestre/PCI/Projeto%201/PCI-GrupoA/Results/apresentacao_slides_benchmark_arc_resumida.html)**

> **Nota sobre Portabilidade:** As duas apresentações HTML possuem todas as imagens e gráficos convertidos e embutidos diretamente em Base64, tornando cada arquivo 100% autônomo e executável em qualquer computador sem necessidade de copiar pastas de imagens anexas.

---

## 📊 Tabela Comparativa de Desempenho Oficial (Tasks Corretas)

| Dataset Avaliado | Tasks Gemma | Acurácia Gemma (31B) | Tasks Gemini | Acurácia Gemini (Flash Lite) | Diferença (p.p.) | Tokens Médios (Corretas) | Tempo Médio por Task (Corretas) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Original (Treino ARC)** | 400 | **76.00%** (304/400) | 400 | **67.50%** (270/400) | **+8.50 pp** | 10.670 vs 9.755 | 224,9s vs 28,3s |
| **Rotated ($T_{\text{in}} = T_{\text{out}}$)** | 304 | **87.17%** (265/304) | 270 | **85.56%** (231/270) | **+1.62 pp** | 10.225 vs 8.983 | 231,7s vs 31,9s |
| **Reflected ($T_{\text{in}} = T_{\text{out}}$)** | 304 | **87.50%** (266/304) | 270 | **87.04%** (235/270) | **+0.46 pp** | 10.216 vs 9.177 | 227,5s vs 29,6s |
| **Coloration ($T_{\text{in}} = T_{\text{out}}$)** | 304 | **89.14%** (271/304) | 270 | **84.44%** (228/270) | **+4.70 pp** | 10.464 vs 9.162 | 238,3s vs 28,7s |
| **Merged (Composto & Livre)** | 591 | **44.50%** (263/591) | 540 | **35.93%** (194/540) | **+8.57 pp** | 11.672 vs 10.494 | 288,2s vs 32,3s |

---

## 📈 Estatísticas de Dispersão e Extremos (Tasks Corretas)

### Gemma 4 (31B-IT)
* **Original:** Tokens (Mín: 2.510, Máx: 36.473, Média: 10.669,8 ± 4.183,6) | Tempo (Mín: 47,6s, Máx: 499,2s, Média: 224,9s ± 83,8s)
* **Rotated:** Tokens (Mín: 2.064, Máx: 39.623, Média: 10.224,7 ± 3.993,3) | Tempo (Mín: 34,5s, Máx: 868,6s, Média: 231,7s ± 107,8s)
* **Reflected:** Tokens (Mín: 2.148, Máx: 27.759, Média: 10.215,5 ± 3.965,5) | Tempo (Mín: 38,4s, Máx: 572,3s, Média: 227,5s ± 94,4s)
* **Coloration:** Tokens (Mín: 2.538, Máx: 30.981, Média: 10.463,6 ± 3.915,7) | Tempo (Mín: 51,7s, Máx: 705,2s, Média: 238,3s ± 101,6s)
* **Merged:** Tokens (Mín: 3.310, Máx: 22.710, Média: 11.672,3 ± 3.820,2) | Tempo (Mín: 67,8s, Máx: 805,3s, Média: 288,2s ± 132,2s)

### Gemini 3.5 Flash Lite
* **Original:** Tokens (Mín: 1.920, Máx: 23.493, Média: 9.754,9 ± 4.983,2) | Tempo (Mín: 4,9s, Máx: 173,7s, Média: 28,3s ± 19,7s)
* **Rotated:** Tokens (Mín: 1.910, Máx: 23.979, Média: 8.983,3 ± 4.494,4) | Tempo (Mín: 4,2s, Máx: 116,1s, Média: 31,9s ± 23,2s)
* **Reflected:** Tokens (Mín: 1.826, Máx: 22.480, Média: 9.176,7 ± 4.542,1) | Tempo (Mín: 4,5s, Máx: 198,8s, Média: 29,6s ± 26,8s)
* **Coloration:** Tokens (Mín: 1.759, Máx: 23.611, Média: 9.161,9 ± 4.429,5) | Tempo (Mín: 4,2s, Máx: 113,8s, Média: 28,7s ± 21,3s)
* **Merged:** Tokens (Mín: 1.816, Máx: 22.401, Média: 10.493,9 ± 4.726,3) | Tempo (Mín: 4,7s, Máx: 266,0s, Média: 32,3s ± 27,7s)

---

## 📑 Estrutura da Apresentação (17 Slides)

1. **Slide 1 — Capa Oficial:** Autoria (Gabriel, Leonardo, Luis), Professores (André, Érica, Frederico, João) e afiliação com a UFRGS.
2. **Slide 2 — O Desafio do ARC-AGI:** François Chollet (2019) e o risco de contaminação prévia decorrente da disponibilidade pública das 400 tarefas de treino na internet.
3. **Slide 3 — A Hipótese da Invariância Isomórfica (Resultados Esperados):**
   * *Caso 1: Raciocínio Genuíno (AGI)* — Regra lógica invariante a rotação, reflexão e cor.
   * *Caso 2: Memorização Canônica (Overfitting)* — Queda de acurácia ou alucinações sob perturbações.
4. **Slide 4 — Metodologia Experimental em 2 Etapas:**
   * *Etapa 1 (High Thinking, $T=0.6$):* Cadeia de pensamento livre explorando hipóteses espaciais.
   * *Etapa 2 (Formatação Determinística, $T=0.0$, Minimal):* Extração estrita do grid numérico.
   * *A Matemática do Tempo:* Prova de que $>99.9\%$ do tempo medido corresponde ao esforço de inferência das TPUs.
5. **Slide 5 — As 4 Famílias de Transformação 2D (com Grids Visuais):**
   * *Rotação:* 90° CW, 180°, 90° CCW ($T_{\text{in}} = T_{\text{out}}$).
   * *Reflexão:* Espelhamento horizontal e vertical ($T_{\text{in}} = T_{\text{out}}$).
   * *Coloração:* Permutação 1:1 incluindo a cor de fundo 0 ($T_{\text{in}} = T_{\text{out}}$).
   * *Merged:* Rotação 90° CW + Reflexão Vertical + Permutação de cores (Composição Livre).
6. **Slide 6 — Tabela Comparativa de Acurácia:** Dados consolidados com indicação de que o Gemma aparenta ter maior recall bruto no dataset público.
7. **Slide 7 — Explorador Interativo de Gráficos:** Abas interativas para alternar entre *Visão 3-em-1*, *Taxa de Acurácia*, *Tokens de Pensamento* e *Tempo de Execução*.
8. **Slide 8 — Quem Acerta Mais vs. Quem é Mais Consistente:**
   * *Volume Bruto:* Gemma 31B lidera em todos os datasets (+8.5 pp original, +8.6 pp merged).
   * *Consistência Simétrica:* Empate técnico em Rotação e Reflexão (diferença menor que 1,6 pp).
   * *Ponto de Ruptura:* Ambos sofrem colapso de 43 a 50 pontos percentuais no Merged.
9. **Slide 9 — Estatísticas de Dispersão e Extremos (Tasks Corretas):** Tabela com filtros múltiplos para alternar entre Modelo (*Gemma*, *Gemini*, *Gemma vs. Gemini*) e Métrica (*Completo*, *Tokens*, *Tempo*).
10. **Slide 10 — Análise de Tokens de Pensamento por Modelo:**
    * *Gemma 31B:* 10.464 tokens (corretas) vs. 16.221 tokens (incorretas) [Pico de 39.623].
    * *Gemini 3.5 Flash Lite:* 9.162 tokens (corretas) vs. 15.586 tokens (incorretas) [Pico de 33.643].
    * *Insight:* Salto de +70% no consumo, possivelmente por entrar em loops de busca em hipóteses inválidas.
11. **Slide 11 — Tempo e Throughput:**
    * Gemini 3.5 Flash Lite opera 7x a 8x mais rápido (~28s a 32s vs ~225s a 288s por tarefa correta).
12. **Slide 12 — Estudo de Caso 1: A "Regra Fantasma":**
    * *Modelo:* Gemma 4 (31B-IT) na *Task f1cefba8* (Merged).
    * Reproduziu a regra antiga do dataset público no texto de raciocínio (*"cycle 2 -> 3 -> 8 -> 2"*), mesmo após essa regra ter sido removida no JSON transformado.
13. **Slide 13 — Estudo de Caso 2: Falhas Espaciais e Viés Canônico:**
    * *Task 0ac8ac11 (Gemma 31B):* Inversão de índices de colunas e alturas em reflexão.
    * *Task f7cb8069 (Gemini Flash):* Desvio métrico na segunda reta vertical (coluna 7 em vez de 5).
    * *Task 04e656f5 (Gemini Flash):* Falha dimensional severa (quadrado 5x5 em vez de retângulo 10x4).
14. **Slide 14 — Discussão e Hipóteses Explicativas (Cautela Epistêmica):**
    * *Operadores Parciais:* Modelos podem ter desenvolvido representações heurísticas para simetrias regulares.
    * *Viés Canônico:* A estrutura sequencial pode induzir preferências por leitura Top-to-Bottom e Left-to-Right.
    * *Limite Composicional:* A combinação livre de operadores pode sobrecarregar a busca dedutiva.
15. **Slide 15 — Cuidados Metodológicos e Rigor Científico:**
    * Postura cautelosa tratando as conclusões como indícios comportamentais observáveis.
16. **Slide 16 — Conclusões Finais:**
    * O sucesso atual no ARC reflete um regime híbrido entre heurísticas geométricas elementares e memorização de configurações canônicas.
17. **Slide 17 — Próximos Passos e Extensões da Pesquisa:**
    * 1. Redação e Finalização do Artigo Científico em LaTeX no Overleaf.
    * 2. Apresentação e Defesa Formal perante a Banca na UFRGS.
    * 3. Possíveis Extensões Futuras da Pesquisa (análise cruzada de falhas em tasks idênticas, taxonomia estruturada de erros e avaliação com modelos maiores).
