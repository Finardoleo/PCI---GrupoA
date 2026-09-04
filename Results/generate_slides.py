import os
import base64

# Carrega imagens e converte para Base64
with open('Results/benchmark_comparativo_gemma_vs_gemini.png', 'rb') as f:
    b64_geral = base64.b64encode(f.read()).decode('utf-8')
with open('Results/comparativo_acuracia.png', 'rb') as f:
    b64_acuracia = base64.b64encode(f.read()).decode('utf-8')
with open('Results/comparativo_tokens.png', 'rb') as f:
    b64_tokens = base64.b64encode(f.read()).decode('utf-8')
with open('Results/comparativo_tempo.png', 'rb') as f:
    b64_tempo = base64.b64encode(f.read()).decode('utf-8')

print('Images loaded to Base64 successfully.')

def get_shared_head(title):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-body: #F5F1EA;
      --bg-deck: #FFFFFF;
      --bg-cream: #FAF7F2;
      --bg-cream-dark: #F0EAE1;
      --border-cream: #E4DCD0;
      --border-dark: #C8BCAC;
      
      --brown-deep: #2A1F17;
      --brown-espresso: #443224;
      --brown-cognac: #B86728;
      --brown-caramel: #D48B47;
      --brown-terracotta: #A64426;
      --brown-sand: #EADBC8;
      
      --text-main: #231B15;
      --text-muted: #574A3E;
      --text-light: #8C7C6F;

      --badge-gemma-bg: #F5EAE0;
      --badge-gemma-txt: #5C3214;
      --badge-gemini-bg: #E8F0F5;
      --badge-gemini-txt: #1A4663;
      --badge-success-bg: #EAF3EC;
      --badge-success-txt: #1B582E;
      --badge-danger-bg: #FBECE9;
      --badge-danger-txt: #8B2519;
      
      --shadow-deck: 0 16px 44px -8px rgba(42, 31, 23, 0.1), 0 4px 14px -2px rgba(42, 31, 23, 0.04);
      --shadow-card: 0 3px 8px rgba(42, 31, 23, 0.04), 0 1px 3px rgba(42, 31, 23, 0.02);
      --radius-deck: 22px;
      --radius-card: 14px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-body);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 16px;
      overflow-x: hidden;
    }}

    .deck-container {{
      width: 100%;
      max-width: 1480px;
      background: var(--bg-deck);
      border-radius: var(--radius-deck);
      border: 1px solid var(--border-cream);
      box-shadow: var(--shadow-deck);
      display: flex;
      flex-direction: column;
      min-height: 870px;
      overflow: hidden;
    }}

    .top-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 40px;
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-cream);
    }}
    
    .topic-pill {{
      font-size: 0.82rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 5px 16px;
      border-radius: 20px;
      background: #F3ECE2;
      color: var(--brown-espresso);
      border: 1px solid #DFD2C2;
    }}

    .slide-counter {{
      font-family: 'Outfit', sans-serif;
      font-size: 1rem;
      font-weight: 800;
      color: var(--brown-espresso);
    }}

    .progress-track {{ width: 100%; height: 5px; background: #EDE6DC; }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--brown-espresso), var(--brown-cognac), var(--brown-caramel));
      transition: width 0.3s ease;
    }}

    .slide-viewport {{
      flex: 1;
      padding: 34px 54px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      background: var(--bg-cream);
    }}

    .slide {{
      display: none;
      opacity: 0;
      transform: translateY(10px);
      transition: opacity 0.28s ease, transform 0.28s ease;
      width: 100%;
    }}
    .slide.active {{
      display: flex;
      flex-direction: column;
      opacity: 1;
      transform: translateY(0);
    }}

    h1, h2, h3, h4 {{ font-family: 'Outfit', sans-serif; color: var(--brown-deep); }}
    .slide-title {{ font-size: 2.3rem; font-weight: 800; line-height: 1.18; margin-bottom: 8px; }}
    .slide-subtitle {{ font-size: 1.08rem; color: var(--text-muted); margin-bottom: 22px; font-weight: 500; }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 14px;
      border-radius: 6px;
      font-size: 0.85rem;
      font-weight: 800;
      font-family: 'Outfit', sans-serif;
    }}
    .badge-gemma {{ background: var(--badge-gemma-bg); color: var(--badge-gemma-txt); border: 1px solid #E5D5C5; }}
    .badge-gemini {{ background: var(--badge-gemini-bg); color: var(--badge-gemini-txt); border: 1px solid #CADBE7; }}
    .badge-success {{ background: var(--badge-success-bg); color: var(--badge-success-txt); border: 1px solid #C4DFC8; }}
    .badge-danger {{ background: var(--badge-danger-bg); color: var(--badge-danger-txt); border: 1px solid #F3C9C3; }}

    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}

    .card {{
      background: #FFFFFF;
      border-radius: var(--radius-card);
      padding: 20px 22px;
      border: 1px solid var(--border-cream);
      box-shadow: var(--shadow-card);
    }}
    .card-brown {{ border-left: 5px solid var(--brown-espresso); }}
    .card-cognac {{ border-left: 5px solid var(--brown-cognac); }}
    .card-terracotta {{ border-left: 5px solid var(--brown-terracotta); }}
    .card-success {{ border-left: 5px solid #2D6A4F; background: #FCFDFB; }}
    .card-danger {{ border-left: 5px solid #8B2519; background: #FFFDFD; }}

    .card-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.08rem;
      font-weight: 700;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .card-body {{
      font-size: 0.94rem;
      line-height: 1.55;
      color: var(--text-main);
    }}
    .card-body ul {{
      padding-left: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .table-wrapper {{
      background: #FFFFFF;
      border-radius: var(--radius-card);
      border: 1px solid var(--border-cream);
      box-shadow: var(--shadow-card);
      overflow: hidden;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.90rem;
    }}
    .data-table th {{
      background: #F5EFE6;
      color: var(--brown-deep);
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      padding: 12px 16px;
      border-bottom: 2px solid var(--border-cream);
    }}
    .data-table td {{
      padding: 11px 16px;
      border-bottom: 1px solid var(--border-cream);
      color: var(--text-main);
    }}
    .data-table tr:last-child td {{ border-bottom: none; }}
    .data-table tr:hover td {{ background: #FAF6F0; }}
    .data-table tr.highlight td {{ background: #FDF4F2; font-weight: 600; }}

    .speaker-script {{
      background: #FFFFFF;
      border-left: 4px solid var(--brown-cognac);
      border-radius: 8px;
      padding: 12px 16px;
      margin-top: 16px;
      font-size: 0.88rem;
      line-height: 1.5;
      color: var(--brown-espresso);
      border-top: 1px solid var(--border-cream);
      border-right: 1px solid var(--border-cream);
      border-bottom: 1px solid var(--border-cream);
    }}
    .speaker-script strong {{ color: var(--brown-deep); }}

    .matrix-box {{
      display: inline-grid;
      gap: 2px;
      background: #E8DDD0;
      padding: 3px;
      border-radius: 4px;
      border: 1px solid #D5C7B7;
    }}
    .m-cell {{ width: 16px; height: 16px; border-radius: 2px; }}
    .c0 {{ background: #000000; }}
    .c1 {{ background: #3B82F6; }}
    .c2 {{ background: #EF4444; }}
    .c3 {{ background: #10B981; }}
    .c4 {{ background: #F59E0B; }}
    .c8 {{ background: #06B6D4; }}

    .chart-tabs {{
      display: flex;
      gap: 10px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }}
    .chart-tab-btn {{
      padding: 8px 18px;
      border-radius: 8px;
      font-family: 'Outfit', sans-serif;
      font-size: 0.92rem;
      font-weight: 700;
      border: 1px solid var(--border-cream);
      background: #FFFFFF;
      color: var(--brown-espresso);
      cursor: pointer;
      transition: all 0.2s;
    }}
    .chart-tab-btn:hover {{ background: #F5ECE0; }}
    .chart-tab-btn.active {{
      background: var(--brown-espresso);
      color: #FAF7F2;
      border-color: var(--brown-espresso);
    }}

    .chart-display-frame {{
      background: #FFFFFF;
      border-radius: var(--radius-card);
      border: 1px solid var(--border-cream);
      padding: 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 470px;
      box-shadow: var(--shadow-card);
    }}

    /* Controles da Tabela de Estatísticas */
    .filter-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .filter-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .filter-btn {{
      padding: 6px 14px;
      border-radius: 6px;
      font-family: 'Outfit', sans-serif;
      font-size: 0.88rem;
      font-weight: 700;
      border: 1px solid var(--border-cream);
      background: #FFFFFF;
      color: var(--brown-espresso);
      cursor: pointer;
      transition: all 0.2s;
    }}
    .filter-btn:hover {{ background: #F5ECE0; }}
    .filter-btn.active {{
      background: var(--brown-espresso);
      color: #FAF7F2;
      border-color: var(--brown-espresso);
    }}

    .stat-card {{
      background: #FAF7F2;
      border-radius: 8px;
      padding: 10px 14px;
      border: 1px solid var(--border-cream);
      text-align: center;
    }}
    .stat-number {{
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      font-size: 1.8rem;
      color: var(--brown-deep);
    }}
    .stat-label {{
      font-size: 0.80rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .bottom-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 40px;
      background: #FFFFFF;
      border-top: 1px solid var(--border-cream);
    }}
    
    .nav-btn {{
      padding: 9px 22px;
      border-radius: 8px;
      font-family: 'Outfit', sans-serif;
      font-size: 0.94rem;
      font-weight: 800;
      cursor: pointer;
      border: 1px solid var(--border-cream);
      background: #FFFFFF;
      color: var(--brown-deep);
      transition: all 0.2s;
    }}
    .nav-btn:hover:not(:disabled) {{ background: #F5EFE6; transform: translateY(-1px); }}
    .nav-btn.btn-primary {{ background: var(--brown-espresso); color: #FAF7F2; border-color: var(--brown-espresso); }}
    .nav-btn.btn-primary:hover:not(:disabled) {{ background: var(--brown-deep); }}
    .nav-btn:disabled {{ opacity: 0.35; cursor: not-allowed; }}

    .switch-link {{
      font-size: 0.84rem;
      font-weight: 800;
      color: var(--brown-cognac);
      text-decoration: none;
      padding: 5px 14px;
      border-radius: 6px;
      background: #F6ECE0;
      border: 1px solid #E8D3BF;
      transition: background 0.2s;
    }}
    .switch-link:hover {{ background: #EEDCCE; }}

    kbd {{
      background: #F0EAE1;
      border: 1px solid #D5C8B8;
      border-radius: 4px;
      padding: 2px 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
    }}
  </style>
</head>
<body>
"""

def get_shared_js():
    return f"""
  <script>
    const CHART_IMAGES = {{
      'geral': 'data:image/png;base64,{b64_geral}',
      'acuracia': 'data:image/png;base64,{b64_acuracia}',
      'tokens': 'data:image/png;base64,{b64_tokens}',
      'tempo': 'data:image/png;base64,{b64_tempo}'
    }};

    let currentIdx = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    const progressFill = document.getElementById('progressFill');
    const slideCounter = document.getElementById('slideCounter');
    const slideTopic = document.getElementById('slideTopic');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    function renderSlide() {{
      slides.forEach((s, idx) => {{
        s.classList.toggle('active', idx === currentIdx);
      }});

      const activeElem = slides[currentIdx];
      const topic = activeElem.getAttribute('data-topic') || 'Apresentação';
      slideTopic.innerText = topic;

      slideCounter.innerText = `Slide ${{currentIdx + 1}} de ${{totalSlides}}`;
      progressFill.style.width = `${{((currentIdx + 1) / totalSlides) * 100}}%`;

      prevBtn.disabled = currentIdx === 0;
      nextBtn.disabled = currentIdx === totalSlides - 1;
      nextBtn.innerText = currentIdx === totalSlides - 1 ? 'Concluir' : 'Próximo →';
    }}

    function navSlide(dir) {{
      const target = currentIdx + dir;
      if (target >= 0 && target < totalSlides) {{
        currentIdx = target;
        renderSlide();
      }}
    }}

    function switchChartTab(chartKey, descText, btnElem) {{
      const img = document.getElementById('mainChartImg');
      const desc = document.getElementById('chartDesc');
      if (CHART_IMAGES[chartKey]) {{
        img.src = CHART_IMAGES[chartKey];
        desc.innerText = descText;
      }}

      document.querySelectorAll('.chart-tab-btn').forEach(b => b.classList.remove('active'));
      if (btnElem) btnElem.classList.add('active');
    }}

    // Controle interativo da Tabela de Estatísticas (Modelo x Métrica)
    let curStatModel = 'gemma';
    let curStatMetric = 'both';

    function setStatModel(model, btnElem) {{
      curStatModel = model;
      document.querySelectorAll('.btn-stat-model').forEach(b => b.classList.remove('active'));
      if (btnElem) btnElem.classList.add('active');
      renderStatsView();
    }}

    function setStatMetric(metric, btnElem) {{
      curStatMetric = metric;
      document.querySelectorAll('.btn-stat-metric').forEach(b => b.classList.remove('active'));
      if (btnElem) btnElem.classList.add('active');
      renderStatsView();
    }}

    function renderStatsView() {{
      const allTables = document.querySelectorAll('.stats-view-table');
      allTables.forEach(t => t.style.display = 'none');

      const targetId = `stats_${{curStatModel}}_${{curStatMetric}}`;
      const targetElem = document.getElementById(targetId);
      if (targetElem) {{
        targetElem.style.display = 'block';
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ') {{
        navSlide(1);
      }} else if (e.key === 'ArrowLeft') {{
        navSlide(-1);
      }}
    }});

    renderSlide();
  </script>
</body>
</html>
"""

# Bloco HTML reutilizável das tabelas interativas de dispersão (com cores para Gemma e Gemini e sem variância)
def get_dispersion_tables_html():
    return """
        <!-- Barra de Filtros Dupla (Modelo e Métrica) -->
        <div class="filter-bar">
          <div class="filter-group">
            <span style="font-size: 0.88rem; font-weight: 700; color: var(--brown-espresso);">Modelo:</span>
            <button class="filter-btn btn-stat-model active" onclick="setStatModel('gemma', this)">🤖 Gemma 4 (31B)</button>
            <button class="filter-btn btn-stat-model" onclick="setStatModel('gemini', this)">⚡ Gemini 3.5 Flash Lite</button>
            <button class="filter-btn btn-stat-model" onclick="setStatModel('compare', this)">⚔️ Gemma vs. Gemini</button>
          </div>
          <div class="filter-group">
            <span style="font-size: 0.88rem; font-weight: 700; color: var(--brown-espresso);">Métrica:</span>
            <button class="filter-btn btn-stat-metric active" onclick="setStatMetric('both', this)">📊 Completo</button>
            <button class="filter-btn btn-stat-metric" onclick="setStatMetric('tokens', this)">🧠 Apenas Tokens</button>
            <button class="filter-btn btn-stat-metric" onclick="setStatMetric('time', this)">⏱️ Apenas Tempo (s)</button>
          </div>
        </div>

        <!-- 1. GEMMA - COMPLETO -->
        <div class="table-wrapper stats-view-table" id="stats_gemma_both">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Tasks Corretas</th>
                <th>Tokens (Mín)</th>
                <th>Tokens (Máx)</th>
                <th>Tokens (Média ± σ)</th>
                <th>Tempo (Mín)</th>
                <th>Tempo (Máx)</th>
                <th>Tempo (Média ± σ)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td><span class="badge badge-gemma">304 / 400 (76.0%)</span></td>
                <td>2.510</td>
                <td>36.473</td>
                <td><strong>10.669,8</strong> ± 4.183,6</td>
                <td>47,6s</td>
                <td>499,2s</td>
                <td><strong>224,9s</strong> ± 83,8s</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td><span class="badge badge-success">265 / 304 (87.2%)</span></td>
                <td>2.064</td>
                <td>39.623</td>
                <td><strong>10.224,7</strong> ± 3.993,3</td>
                <td>34,5s</td>
                <td>868,6s</td>
                <td><strong>231,7s</strong> ± 107,8s</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td><span class="badge badge-success">266 / 304 (87.5%)</span></td>
                <td>2.148</td>
                <td>27.759</td>
                <td><strong>10.215,5</strong> ± 3.965,5</td>
                <td>38,4s</td>
                <td>572,3s</td>
                <td><strong>227,5s</strong> ± 94,4s</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td><span class="badge badge-success">271 / 304 (89.1%)</span></td>
                <td>2.538</td>
                <td>30.981</td>
                <td><strong>10.463,6</strong> ± 3.915,7</td>
                <td>51,7s</td>
                <td>705,2s</td>
                <td><strong>238,3s</strong> ± 101,6s</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged (Composto)</strong></td>
                <td><span class="badge badge-danger">263 / 591 (44.5%)</span></td>
                <td>3.310</td>
                <td>22.710</td>
                <td><strong>11.672,3</strong> ± 3.820,2</td>
                <td>67,8s</td>
                <td>805,3s</td>
                <td><strong>288,2s</strong> ± 132,2s</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 2. GEMMA - APENAS TOKENS (Sem variância) -->
        <div class="table-wrapper stats-view-table" id="stats_gemma_tokens" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Corretas / Total</th>
                <th>Tokens Mínimo</th>
                <th>Tokens Máximo</th>
                <th>Tokens (Média ± Desvio Padrão)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td>304 / 400 (76.0%)</td>
                <td>2.510</td>
                <td>36.473</td>
                <td><strong>10.669,8</strong> ± 4.183,6</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td>265 / 304 (87.2%)</td>
                <td>2.064</td>
                <td>39.623</td>
                <td><strong>10.224,7</strong> ± 3.993,3</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td>266 / 304 (87.5%)</td>
                <td>2.148</td>
                <td>27.759</td>
                <td><strong>10.215,5</strong> ± 3.965,5</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td>271 / 304 (89.1%)</td>
                <td>2.538</td>
                <td>30.981</td>
                <td><strong>10.463,6</strong> ± 3.915,7</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td>263 / 591 (44.5%)</td>
                <td>3.310</td>
                <td>22.710</td>
                <td><strong>11.672,3</strong> ± 3.820,2</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 3. GEMMA - APENAS TEMPO (Sem variância) -->
        <div class="table-wrapper stats-view-table" id="stats_gemma_time" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Corretas / Total</th>
                <th>Tempo Mínimo (s)</th>
                <th>Tempo Máximo (s)</th>
                <th>Tempo (Média ± Desvio Padrão)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td>304 / 400 (76.0%)</td>
                <td>47,6s</td>
                <td>499,2s (8,3 min)</td>
                <td><strong>224,9s</strong> ± 83,8s</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td>265 / 304 (87.2%)</td>
                <td>34,5s</td>
                <td>868,6s (14,5 min)</td>
                <td><strong>231,7s</strong> ± 107,8s</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td>266 / 304 (87.5%)</td>
                <td>38,4s</td>
                <td>572,3s (9,5 min)</td>
                <td><strong>227,5s</strong> ± 94,4s</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td>271 / 304 (89.1%)</td>
                <td>51,7s</td>
                <td>705,2s (11,8 min)</td>
                <td><strong>238,3s</strong> ± 101,6s</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td>263 / 591 (44.5%)</td>
                <td>67,8s</td>
                <td>805,3s (13,4 min)</td>
                <td><strong>288,2s</strong> ± 132,2s</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 4. GEMINI - COMPLETO -->
        <div class="table-wrapper stats-view-table" id="stats_gemini_both" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Tasks Corretas</th>
                <th>Tokens (Mín)</th>
                <th>Tokens (Máx)</th>
                <th>Tokens (Média ± σ)</th>
                <th>Tempo (Mín)</th>
                <th>Tempo (Máx)</th>
                <th>Tempo (Média ± σ)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td><span class="badge badge-gemini">270 / 400 (67.5%)</span></td>
                <td>1.920</td>
                <td>23.493</td>
                <td><strong>9.754,9</strong> ± 4.983,2</td>
                <td>4,9s</td>
                <td>173,7s</td>
                <td><strong>28,3s</strong> ± 19,7s</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td><span class="badge badge-success">231 / 270 (85.6%)</span></td>
                <td>1.910</td>
                <td>23.979</td>
                <td><strong>8.983,3</strong> ± 4.494,4</td>
                <td>4,2s</td>
                <td>116,1s</td>
                <td><strong>31,9s</strong> ± 23,2s</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td><span class="badge badge-success">235 / 270 (87.0%)</span></td>
                <td>1.826</td>
                <td>22.480</td>
                <td><strong>9.176,7</strong> ± 4.542,1</td>
                <td>4,5s</td>
                <td>198,8s</td>
                <td><strong>29,6s</strong> ± 26,8s</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td><span class="badge badge-success">228 / 270 (84.4%)</span></td>
                <td>1.759</td>
                <td>23.611</td>
                <td><strong>9.161,9</strong> ± 4.429,5</td>
                <td>4,2s</td>
                <td>113,8s</td>
                <td><strong>28,7s</strong> ± 21,3s</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged (Composto)</strong></td>
                <td><span class="badge badge-danger">194 / 540 (35.9%)</span></td>
                <td>1.816</td>
                <td>22.401</td>
                <td><strong>10.493,9</strong> ± 4.726,3</td>
                <td>4,7s</td>
                <td>266,0s</td>
                <td><strong>32,3s</strong> ± 27,7s</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 5. GEMINI - APENAS TOKENS (Sem variância) -->
        <div class="table-wrapper stats-view-table" id="stats_gemini_tokens" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Corretas / Total</th>
                <th>Tokens Mínimo</th>
                <th>Tokens Máximo</th>
                <th>Tokens (Média ± Desvio Padrão)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td>270 / 400 (67.5%)</td>
                <td>1.920</td>
                <td>23.493</td>
                <td><strong>9.754,9</strong> ± 4.983,2</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td>231 / 270 (85.6%)</td>
                <td>1.910</td>
                <td>23.979</td>
                <td><strong>8.983,3</strong> ± 4.494,4</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td>235 / 270 (87.0%)</td>
                <td>1.826</td>
                <td>22.480</td>
                <td><strong>9.176,7</strong> ± 4.542,1</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td>228 / 270 (84.4%)</td>
                <td>1.759</td>
                <td>23.611</td>
                <td><strong>9.161,9</strong> ± 4.429,5</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td>194 / 540 (35.9%)</td>
                <td>1.816</td>
                <td>22.401</td>
                <td><strong>10.493,9</strong> ± 4.726,3</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 6. GEMINI - APENAS TEMPO (Sem variância) -->
        <div class="table-wrapper stats-view-table" id="stats_gemini_time" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Corretas / Total</th>
                <th>Tempo Mínimo (s)</th>
                <th>Tempo Máximo (s)</th>
                <th>Tempo (Média ± Desvio Padrão)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td>270 / 400 (67.5%)</td>
                <td>4,9s</td>
                <td>173,7s</td>
                <td><strong>28,3s</strong> ± 19,7s</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td>231 / 270 (85.6%)</td>
                <td>4,2s</td>
                <td>116,1s</td>
                <td><strong>31,9s</strong> ± 23,2s</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td>235 / 270 (87.0%)</td>
                <td>4,5s</td>
                <td>198,8s</td>
                <td><strong>29,6s</strong> ± 26,8s</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td>228 / 270 (84.4%)</td>
                <td>4,2s</td>
                <td>113,8s</td>
                <td><strong>28,7s</strong> ± 21,3s</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td>194 / 540 (35.9%)</td>
                <td>4,7s</td>
                <td>266,0s</td>
                <td><strong>32,3s</strong> ± 27,7s</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 7. COMPARATIVO - TOKENS (COM CORES PARA GEMMA E GEMINI) -->
        <div class="table-wrapper stats-view-table" id="stats_compare_tokens" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th style="background: #F5EAE0; color: #5C3214; border-bottom: 2px solid #E5D5C5;">Gemma (Média ± σ)</th>
                <th style="background: #F5EAE0; color: #5C3214; border-bottom: 2px solid #E5D5C5;">Gemma (Mín - Máx)</th>
                <th style="background: #E8F0F5; color: #1A4663; border-bottom: 2px solid #CADBE7;">Gemini (Média ± σ)</th>
                <th style="background: #E8F0F5; color: #1A4663; border-bottom: 2px solid #CADBE7;">Gemini (Mín - Máx)</th>
                <th>Diferença (Gemma − Gemini)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">10.669,8 ± 4.183,6</td>
                <td style="background: #FAF4EE; color: #443224;">2.510 - 36.473</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">9.754,9 ± 4.983,2</td>
                <td style="background: #F3F7FA; color: #1A4663;">1.920 - 23.493</td>
                <td style="font-weight: 700;">+914,9 tokens</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">10.224,7 ± 3.993,3</td>
                <td style="background: #FAF4EE; color: #443224;">2.064 - 39.623</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">8.983,3 ± 4.494,4</td>
                <td style="background: #F3F7FA; color: #1A4663;">1.910 - 23.979</td>
                <td style="font-weight: 700;">+1.241,4 tokens</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">10.215,5 ± 3.965,5</td>
                <td style="background: #FAF4EE; color: #443224;">2.148 - 27.759</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">9.176,7 ± 4.542,1</td>
                <td style="background: #F3F7FA; color: #1A4663;">1.826 - 22.480</td>
                <td style="font-weight: 700;">+1.038,8 tokens</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">10.463,6 ± 3.915,7</td>
                <td style="background: #FAF4EE; color: #443224;">2.538 - 30.981</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">9.161,9 ± 4.429,5</td>
                <td style="background: #F3F7FA; color: #1A4663;">1.759 - 23.611</td>
                <td style="font-weight: 700;">+1.301,7 tokens</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">11.672,3 ± 3.820,2</td>
                <td style="background: #FAF4EE; color: #443224;">3.310 - 22.710</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">10.493,9 ± 4.726,3</td>
                <td style="background: #F3F7FA; color: #1A4663;">1.816 - 22.401</td>
                <td style="font-weight: 700;">+1.178,4 tokens</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 8. COMPARATIVO - TEMPO (COM CORES PARA GEMMA E GEMINI E REFERÊNCIA CLARA) -->
        <div class="table-wrapper stats-view-table" id="stats_compare_time" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th style="background: #F5EAE0; color: #5C3214; border-bottom: 2px solid #E5D5C5;">Gemma (Média ± σ)</th>
                <th style="background: #F5EAE0; color: #5C3214; border-bottom: 2px solid #E5D5C5;">Gemma (Mín - Máx)</th>
                <th style="background: #E8F0F5; color: #1A4663; border-bottom: 2px solid #CADBE7;">Gemini (Média ± σ)</th>
                <th style="background: #E8F0F5; color: #1A4663; border-bottom: 2px solid #CADBE7;">Gemini (Mín - Máx)</th>
                <th>Aceleração do Gemini (em relação ao Gemma)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">224,9s ± 83,8s</td>
                <td style="background: #FAF4EE; color: #443224;">47,6s - 499,2s</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">28,3s ± 19,7s</td>
                <td style="background: #F3F7FA; color: #1A4663;">4,9s - 173,7s</td>
                <td style="font-weight: 700; color: #1B582E;">⚡ 7.9x mais rápido que o Gemma</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">231,7s ± 107,8s</td>
                <td style="background: #FAF4EE; color: #443224;">34,5s - 868,6s</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">31,9s ± 23,2s</td>
                <td style="background: #F3F7FA; color: #1A4663;">4,2s - 116,1s</td>
                <td style="font-weight: 700; color: #1B582E;">⚡ 7.3x mais rápido que o Gemma</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">227,5s ± 94,4s</td>
                <td style="background: #FAF4EE; color: #443224;">38,4s - 572,3s</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">29,6s ± 26,8s</td>
                <td style="background: #F3F7FA; color: #1A4663;">4,5s - 198,8s</td>
                <td style="font-weight: 700; color: #1B582E;">⚡ 7.7x mais rápido que o Gemma</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">238,3s ± 101,6s</td>
                <td style="background: #FAF4EE; color: #443224;">51,7s - 705,2s</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">28,7s ± 21,3s</td>
                <td style="background: #F3F7FA; color: #1A4663;">4,2s - 113,8s</td>
                <td style="font-weight: 700; color: #1B582E;">⚡ 8.3x mais rápido que o Gemma</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td style="background: #FAF4EE; color: #443224; font-weight: 600;">288,2s ± 132,2s</td>
                <td style="background: #FAF4EE; color: #443224;">67,8s - 805,3s</td>
                <td style="background: #F3F7FA; color: #1A4663; font-weight: 600;">32,3s ± 27,7s</td>
                <td style="background: #F3F7FA; color: #1A4663;">4,7s - 266,0s</td>
                <td style="font-weight: 700; color: #1B582E;">⚡ 8.9x mais rápido que o Gemma</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 9. COMPARATIVO - COMPLETO (COM CORES PARA GEMMA E GEMINI) -->
        <div class="table-wrapper stats-view-table" id="stats_compare_both" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma Tokens</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini Tokens</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma Tempo</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini Tempo</th>
                <th>Acurácia (Gemma − Gemini)</th>
                <th>Aceleração do Gemini</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td style="background: #FAF4EE; color: #443224;">10.669,8</td>
                <td style="background: #F3F7FA; color: #1A4663;">9.754,9</td>
                <td style="background: #FAF4EE; color: #443224;">224,9s</td>
                <td style="background: #F3F7FA; color: #1A4663;">28,3s</td>
                <td style="font-weight: 700;">+8.50 pp</td>
                <td style="font-weight: 700; color: #1B582E;">7.9x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td style="background: #FAF4EE; color: #443224;">10.224,7</td>
                <td style="background: #F3F7FA; color: #1A4663;">8.983,3</td>
                <td style="background: #FAF4EE; color: #443224;">231,7s</td>
                <td style="background: #F3F7FA; color: #1A4663;">31,9s</td>
                <td style="font-weight: 700;">+1.62 pp</td>
                <td style="font-weight: 700; color: #1B582E;">7.3x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td style="background: #FAF4EE; color: #443224;">10.215,5</td>
                <td style="background: #F3F7FA; color: #1A4663;">9.176,7</td>
                <td style="background: #FAF4EE; color: #443224;">227,5s</td>
                <td style="background: #F3F7FA; color: #1A4663;">29,6s</td>
                <td style="font-weight: 700;">+0.46 pp</td>
                <td style="font-weight: 700; color: #1B582E;">7.7x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td style="background: #FAF4EE; color: #443224;">10.463,6</td>
                <td style="background: #F3F7FA; color: #1A4663;">9.161,9</td>
                <td style="background: #FAF4EE; color: #443224;">238,3s</td>
                <td style="background: #F3F7FA; color: #1A4663;">28,7s</td>
                <td style="font-weight: 700;">+4.70 pp</td>
                <td style="font-weight: 700; color: #1B582E;">8.3x mais rápido</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td style="background: #FAF4EE; color: #443224;">11.672,3</td>
                <td style="background: #F3F7FA; color: #1A4663;">10.493,9</td>
                <td style="background: #FAF4EE; color: #443224;">288,2s</td>
                <td style="background: #F3F7FA; color: #1A4663;">32,3s</td>
                <td style="font-weight: 700;">+8.57 pp</td>
                <td style="font-weight: 700; color: #1B582E;">8.9x mais rápido</td>
              </tr>
            </tbody>
          </table>
        </div>
    """


# ==============================================================================
# GERAÇÃO DA APRESENTAÇÃO RESUMIDA (SUCINTA, SEM LINK, 17 SLIDES)
# ==============================================================================
def generate_resumida():
    head = get_shared_head("Benchmark ARC-AGI: Raciocínio vs Memorização (Versão Apresentação Pública)")
    
    body = f"""
  <div class="deck-container">
    <!-- Top Header (Sem link para versão completa) -->
    <div class="top-header">
      <div style="display: flex; align-items: center; gap: 14px;">
        <span class="topic-pill" id="slideTopic">Apresentação</span>
      </div>
      <div class="slide-counter" id="slideCounter">Slide 1 de 17</div>
    </div>
    
    <div class="progress-track">
      <div class="progress-fill" id="progressFill"></div>
    </div>

    <!-- Viewport -->
    <div class="slide-viewport">

      <!-- SLIDE 1: Capa -->
      <div class="slide active" data-topic="Apresentação">
        <div style="text-align: center; max-width: 1100px; margin: 0 auto;">
          <div style="display: inline-flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <span class="badge badge-gemma" style="font-size: 1rem; padding: 6px 18px;">Gemma 4 (31B-IT)</span>
            <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">VS</span>
            <span class="badge badge-gemini" style="font-size: 1rem; padding: 6px 18px;">Gemini 3.5 Flash Lite</span>
          </div>
          <h1 class="slide-title" style="font-size: 2.85rem; margin-bottom: 14px;">
            ARC-AGI: Raciocínio Genuíno ou Memorização de Dados Públicos?
          </h1>
          <p class="slide-subtitle" style="font-size: 1.2rem; margin-bottom: 30px;">
            Avaliando a invariância de Modelos de Linguagem sob perturbações 2D.
          </p>

          <div class="grid-2" style="max-width: 950px; margin: 0 auto; text-align: left;">
            <div class="card card-brown">
              <div style="font-size: 0.85rem; font-weight: 800; color: var(--brown-espresso);">DISCENTES</div>
              <div style="font-size: 1.15rem; font-weight: 800; margin-top: 4px;">Gabriel • Leonardo • Luis</div>
            </div>
            <div class="card card-cognac">
              <div style="font-size: 0.85rem; font-weight: 800; color: var(--brown-cognac);">DOCENTES & AVALIADORES</div>
              <div style="font-size: 1.15rem; font-weight: 800; margin-top: 4px;">Prof. André • Profa. Érica • Prof. João • Prof. Frederico</div>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 2: O Desafio do ARC-AGI -->
      <div class="slide" data-topic="O Problema Científico">
        <h2 class="slide-title">O Desafio do ARC-AGI</h2>
        <p class="slide-subtitle">Por que pontuações elevadas geram desconfiança na comunidade?</p>

        <div class="grid-2">
          <div class="card card-brown">
            <div class="card-title">🧩 O Teste de Inteligência Geral</div>
            <div class="card-body">
              <ul>
                <li>Proposto por Chollet (2019) para medir <strong>aquisição rápida de novas regras</strong>.</li>
                <li>Matrizes 2D com indução lógica puramente visual em Few-Shot.</li>
                <li>Baseado em Core Knowledge: simetria, conectividade, contagem e geometria.</li>
              </ul>
            </div>
          </div>

          <div class="card card-terracotta">
            <div class="card-title">⚠️ O Fator da Contaminação</div>
            <div class="card-body">
              <ul>
                <li>As 400 tarefas de treino estão <strong>públicas na web desde 2019</strong>.</li>
                <li>LLMs modernos tiveram contato massivo com esses dados no pré-treinamento.</li>
                <li><strong>Questão Central:</strong> Indução lógica real ou recuperação de gabarito?</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 3: Hipótese Invariante (COM CASO 1 E CASO 2) -->
      <div class="slide" data-topic="Hipótese Epistêmica">
        <h2 class="slide-title">O Teste da Invariância Isomórfica</h2>
        <p class="slide-subtitle">A lógica abstrata deve ser preservada sob perturbações espaciais. Resultados esperados:</p>

        <div class="grid-2">
          <div class="card card-success">
            <div class="card-title">🧠 Caso 1: Raciocínio Genuíno (AGI)</div>
            <div class="card-body">
              <ul>
                <li>Compreensão conceitual invariante a eixos ou paletas de cores.</li>
                <li>A acurácia se mantém estável mesmo se a matriz for girada ou espelhada.</li>
                <li>Capacidade de generalizar regras para configurações não-canônicas.</li>
              </ul>
            </div>
          </div>

          <div class="card card-danger">
            <div class="card-title">📦 Caso 2: Memorização Canônica (Overfitting)</div>
            <div class="card-body">
              <ul>
                <li>Dependência estrita de coordenadas, orientação de leitura ou cores originais.</li>
                <li>Perturbações causam colapso de acurácia ou alucinação de regras antigas.</li>
                <li>Incapacidade de resolver variações compostas não vistas.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 4: Metodologia em 2 Etapas -->
      <div class="slide" data-topic="Arquitetura Experimental">
        <h2 class="slide-title">Pipeline Experimental em 2 Etapas (solver.py)</h2>
        <p class="slide-subtitle">Separação estrita entre indução de hipóteses e geração determinística de matrizes.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">1. High Thinking</div>
            <div class="card-body">
              <ul>
                <li>Temperatura T = 0.6.</li>
                <li>Cadeia de Pensamento livre (CoT).</li>
                <li>Exploração profunda de hipóteses.</li>
              </ul>
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">2. Formatação Mínima</div>
            <div class="card-body">
              <ul>
                <li>Temperatura T = 0.0 (Greedy).</li>
                <li>Modo Thinking: MINIMAL.</li>
                <li>Extração estrita da matriz numérica.</li>
              </ul>
            </div>
          </div>

          <div class="card card-success">
            <div class="card-title">3. Auditoria Multi-Worker</div>
            <div class="card-body">
              <ul>
                <li>Workers paralelos multi-chaves.</li>
                <li>Persistência em 5 planilhas independentes.</li>
                <li>Métricas de inferência isoladas de rede.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 5: As 4 Transformações 2D (COM FIGURA ASSIMÉTRICA NO MERGED) -->
      <div class="slide" data-topic="Geração das Novas Tasks">
        <h2 class="slide-title">As 4 Transformações Aplicadas</h2>
        <p class="slide-subtitle">Derivadas exclusivamente das tarefas acertadas previamente por cada modelo.</p>

        <div class="grid-4">
          <div class="card card-brown" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🔄 Rotação</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c1"></div><div class="m-cell c1"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">90° CW, 180°, 90° CCW<br>Input == Output</p>
          </div>

          <div class="card card-cognac" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🪞 Reflexão</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">Espelhamento Horizontal / Vertical<br>Input == Output</p>
          </div>

          <div class="card card-terracotta" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🎨 Coloração</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
                <div class="m-cell c8"></div><div class="m-cell c3"></div><div class="m-cell c8"></div>
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">Permutação 1:1 com Cor 0 fixa<br>Input == Output</p>
          </div>

          <div class="card card-danger" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🌪️ Merged</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <!-- Input Assimétrico: 1 no topo esquerdo e 1 com 2 no centro -->
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-terracotta); font-size: 1.2rem;">➔</span>
              <!-- Output: Rotação 90° CW + Reflexão Vertical + Cores (1->8, 2->3) -->
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c8"></div><div class="m-cell c8"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">Rotação 90° + Reflexão + Cor (1→8, 2→3)<br>Composição Livre</p>
          </div>
        </div>
      </div>

      <!-- SLIDE 6: Acurácia Comparativa -->
      <div class="slide" data-topic="Resultados • Acurácia">
        <h2 class="slide-title">Taxas de Acurácia: Gemma vs. Gemini</h2>
        <p class="slide-subtitle">Comparação direta dos dados oficiais obtidos em cada dataset.</p>

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Acurácia Gemma (31B)</th>
                <th>Acurácia Gemini (Flash Lite)</th>
                <th>Diferença</th>
                <th>Tendência Observada</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td><span class="badge badge-gemma">76.00%</span> (304/400)</td>
                <td><span class="badge badge-gemini">67.50%</span> (270/400)</td>
                <td><strong>+8.50 pp</strong></td>
                <td>Gemma aparenta ter maior recall no dataset público</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td><span class="badge badge-success">87.17%</span> (265/304)</td>
                <td><span class="badge badge-success">85.56%</span> (231/270)</td>
                <td><strong>+1.62 pp</strong></td>
                <td>Alta invariância rotacional em ambos</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td><span class="badge badge-success">87.50%</span> (266/304)</td>
                <td><span class="badge badge-success">87.04%</span> (235/270)</td>
                <td><strong>+0.46 pp</strong></td>
                <td>Empate técnico em reflexão axial</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td><span class="badge badge-success">89.14%</span> (271/304)</td>
                <td><span class="badge badge-success">84.44%</span> (228/270)</td>
                <td><strong>+4.70 pp</strong></td>
                <td>Gemma ligeiramente mais robusto em cores</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td><span class="badge badge-danger">44.50%</span> (263/591)</td>
                <td><span class="badge badge-danger">35.93%</span> (194/540)</td>
                <td><strong>+8.57 pp</strong></td>
                <td><strong>Queda severa (-43 a -50 pp) em ambos</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- SLIDE 7: GRÁFICOS INTERATIVOS -->
      <div class="slide" data-topic="Resultados • Gráficos Interativos">
        <h2 class="slide-title">Explorador Interativo de Gráficos</h2>
        <p class="slide-subtitle">Selecione uma métrica abaixo para alternar a visualização.</p>

        <div class="chart-tabs">
          <button class="chart-tab-btn active" onclick="switchChartTab('geral', 'Visão Geral Comparativa 3 em 1 (Acurácia, Tokens e Tempo)', this)">📊 Visão Geral 3-em-1</button>
          <button class="chart-tab-btn" onclick="switchChartTab('acuracia', 'Comparativo Detalhado de Acurácia (%) por Dataset', this)">🎯 Taxa de Acurácia (%)</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tokens', 'Tokens Médios de Pensamento em Tarefas Corretas', this)">🧠 Tokens de Pensamento</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tempo', 'Tempo Médio de Execução por Tarefa em Segundos (Tasks Corretas)', this)">⏱️ Latência e Tempo (s)</button>
        </div>

        <div class="chart-display-frame">
          <img id="mainChartImg" src="data:image/png;base64,{b64_geral}" alt="Gráfico Comparativo ARC-AGI" style="max-width: 100%; max-height: 480px; object-fit: contain; border-radius: 8px;">
          <p id="chartDesc" style="margin-top: 10px; font-size: 0.92rem; font-weight: 700; color: var(--brown-espresso);">
            Visão Geral Comparativa 3 em 1 (Acurácia, Tokens e Tempo)
          </p>
        </div>
      </div>

      <!-- SLIDE 8: QUEM ACERTA MAIS VS QUEM É MAIS CONSISTENTE (AGORA SLIDE 8) -->
      <div class="slide" data-topic="Análise Comparativa">
        <h2 class="slide-title">Quem Acerta Mais vs. Quem é Mais Consistente?</h2>
        <p class="slide-subtitle">Distinguindo volume absoluto de estabilidade perante transformações.</p>

        <div class="grid-2">
          <div class="card card-brown">
            <div class="card-title">🏆 Maior Acurácia Absoluta: Gemma 31B</div>
            <div class="card-body">
              <ul>
                <li>Lidera no Treino Original: <strong>76.0%</strong> (+8.5 pp).</li>
                <li>Lidera no Merged: <strong>44.5%</strong> (+8.6 pp).</li>
                <li>Maior capacidade paramétrica para reter raciocínios longos.</li>
              </ul>
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">⚖️ Simetrias Atômicas: Empate Técnico</div>
            <div class="card-body">
              <ul>
                <li>Reflexão: diferença de apenas <strong>0.46 pp</strong> (87.5% vs 87.0%).</li>
                <li>Rotação: diferença de apenas <strong>1.62 pp</strong> (87.2% vs 85.6%).</li>
                <li>Ambos possuem operadores funcionais para simetrias isoladas.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="card card-danger" style="margin-top: 14px;">
          <div class="card-title" style="color: var(--brown-terracotta);">💥 A Ruptura Comum no Merged</div>
          <div class="card-body">
            Ambos sofrem queda severa para <strong>44.5%</strong> (Gemma) e <strong>35.9%</strong> (Gemini), evidenciando a fragilidade perante composições livres.
          </div>
        </div>
      </div>

      <!-- SLIDE 9: ESTATÍSTICAS DE DISPERSÃO E EXTREMOS (AGORA SLIDE 9 COM FILTRO DUPLO) -->
      <div class="slide" data-topic="Estatísticas • Dispersão e Extremos">
        <h2 class="slide-title">Estatísticas de Dispersão e Extremos (Tasks Corretas)</h2>
        <p class="slide-subtitle">Valores calculados exclusivamente sobre as tarefas resolvidas com sucesso.</p>

        {get_dispersion_tables_html()}

        <div class="grid-2" style="margin-top: 14px;">
          <div class="card card-brown" style="padding: 12px 16px;">
            <div style="font-size: 0.90rem; font-weight: 700; color: var(--brown-espresso); margin-bottom: 4px;">Tokens (Esforço Cognitivo)</div>
            <div style="font-size: 0.88rem; color: var(--text-muted);">Mínimos de ~1.7k a 2.5k em tasks simples; picos de até 39.6k no Gemma e 24.0k no Gemini.</div>
          </div>
          <div class="card card-cognac" style="padding: 12px 16px;">
            <div style="font-size: 0.90rem; font-weight: 700; color: var(--brown-cognac); margin-bottom: 4px;">Tempo (Estabilidade)</div>
            <div style="font-size: 0.88rem; color: var(--text-muted);">Gemini mantém latência ultrabaixa (4.2s mín, 28s média). Gemma exige computação densa (225s média, até 868s).</div>
          </div>
        </div>
      </div>

      <!-- SLIDE 10: TOKENS DE PENSAMENTO SEPARADOS POR MODELO -->
      <div class="slide" data-topic="Tokens & Esforço">
        <h2 class="slide-title">Tokens de Pensamento: Gemma vs. Gemini</h2>
        <p class="slide-subtitle">O custo do raciocínio em tarefas resolvidas com sucesso versus falhas.</p>

        <div class="grid-2" style="margin-bottom: 16px;">
          <!-- Card Gemma -->
          <div class="card card-brown">
            <div class="card-title" style="color: var(--badge-gemma-txt);">
              <span>🤖 Gemma 4 (31B-IT)</span>
            </div>
            <div class="grid-3" style="margin: 10px 0 8px;">
              <div class="stat-card">
                <div class="stat-number" style="color: #2D6A4F; font-size: 1.7rem;">10.464</div>
                <div class="stat-label">Corretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-terracotta); font-size: 1.7rem;">16.221</div>
                <div class="stat-label">Incorretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-cognac); font-size: 1.7rem;">39.623</div>
                <div class="stat-label">Pico</div>
              </div>
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              Consumo sobe em <strong>+55%</strong> quando a dedução lógica falha.
            </p>
          </div>

          <!-- Card Gemini -->
          <div class="card card-cognac">
            <div class="card-title" style="color: var(--badge-gemini-txt);">
              <span>⚡ Gemini 3.5 Flash Lite</span>
            </div>
            <div class="grid-3" style="margin: 10px 0 8px;">
              <div class="stat-card">
                <div class="stat-number" style="color: #2D6A4F; font-size: 1.7rem;">9.162</div>
                <div class="stat-label">Corretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-terracotta); font-size: 1.7rem;">15.586</div>
                <div class="stat-label">Incorretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-cognac); font-size: 1.7rem;">33.643</div>
                <div class="stat-label">Pico</div>
              </div>
            </div>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              Consumo salta em <strong>+70%</strong>, possivelmente por entrar em loops de busca em hipóteses inválidas.
            </p>
          </div>
        </div>

        <div class="card card-brown" style="padding: 12px 18px;">
          <div style="font-size: 0.90rem; font-weight: 700; color: var(--brown-espresso);">💡 Insight Transversal</div>
          <div style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px;">
            Ambos os modelos economizam de 35% a 40% de tokens ao identificar a regra correta rapidamente. Em tarefas perturbadas (Merged), longas cadeias de pensamento não impedem a falha.
          </div>
        </div>
      </div>

      <!-- SLIDE 11: Tempo e Throughput -->
      <div class="slide" data-topic="Latência & Throughput">
        <h2 class="slide-title">Tempo de Execução e Throughput</h2>
        <p class="slide-subtitle">Médias calculadas exclusivamente sobre as tarefas corretas.</p>

        <div class="grid-2">
          <div class="card card-cognac">
            <div class="card-title">⚡ Gemini 3.5 Flash Lite</div>
            <div class="card-body">
              <ul>
                <li>Média de <strong>28s a 32s por task</strong>.</li>
                <li>Latência de resposta inicial (TTFT): 1.38s.</li>
                <li>Ideal para experimentação massiva e benchmarks de larga escala.</li>
              </ul>
            </div>
          </div>

          <div class="card card-brown">
            <div class="card-title">🐢 Gemma 4 31B</div>
            <div class="card-body">
              <ul>
                <li>Média de <strong>225s a 288s por task</strong>.</li>
                <li>Geração a 25-50 tokens/s nas TPUs.</li>
                <li>Custo computacional ~8x maior para ganho modesto de acurácia.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 12: Estudo de Caso 1 (COM IDENTIFICAÇÃO CLARA DO MODELO) -->
      <div class="slide" data-topic="Estudo de Caso • Memorização">
        <h2 class="slide-title">Estudo de Caso 1: A "Regra Fantasma"</h2>
        <p class="slide-subtitle">Task f1cefba8 (Merged) — Alucinação direta da regra da base pública.</p>

        <div class="grid-2">
          <div class="card card-danger">
            <div class="card-title">
              <span>❌ O que o Modelo Escreveu</span>
              <span class="badge badge-gemma">Gemma 4 (31B)</span>
            </div>
            <div class="card-body">
              <p style="font-family: 'JetBrains Mono', monospace; font-size: 0.90rem; background: #FBECE9; padding: 12px; border-radius: 6px; color: #8B2519; border: 1px solid #F3C9C3;">
                "...following the cycle 2 -> 3 -> 8 -> 2..."
              </p>
              <p style="margin-top: 10px; font-size: 0.88rem;">
                Essa regra existia no ARC público original, mas <strong>foi removida na nossa task</strong>! O Gemma 31B ignorou a nova demonstração e aplicou a memória antiga.
              </p>
            </div>
          </div>

          <div class="card card-brown">
            <div class="card-title">💡 Diagnóstico Científico</div>
            <div class="card-body">
              <ul>
                <li>Evidência empírica direta de <strong>recuperação de pré-treino pelo Gemma</strong>.</li>
                <li>Diante de sobrecarga composicional, a dedução por contexto é desligada.</li>
                <li>Confirma dependência parcial de representações memorizadas.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 13: Estudo de Caso 2 (COM MODELO IDENTIFICADO EM CADA CARD) -->
      <div class="slide" data-topic="Estudo de Caso • Falhas Espaciais">
        <h2 class="slide-title">Estudo de Caso 2: Falhas Espaciais e de Eixo</h2>
        <p class="slide-subtitle">Dificuldade com eixos invertidos identificada individualmente nos modelos.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">
              <span>1. Task 0ac8ac11</span>
              <span class="badge badge-gemma">Gemma 31B</span>
            </div>
            <div class="card-body">
              Ao espelhar o grid em Reflexão, o Gemma inverteu índices de colunas e alturas, refletindo vício de leitura Left-to-Right.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">
              <span>2. Task f7cb8069</span>
              <span class="badge badge-gemini">Gemini Flash</span>
            </div>
            <div class="card-body">
              O Gemini traçou retas horizontais, mas errou a vertical (coluna 7 em vez da 5), perdendo o alinhamento de cruzamento.
            </div>
          </div>

          <div class="card card-terracotta">
            <div class="card-title">
              <span>3. Task 04e656f5</span>
              <span class="badge badge-gemini">Gemini Flash</span>
            </div>
            <div class="card-body">
              O Gemini falhou na inferência dimensional (gerou um quadrado 5x5 em vez de retângulo 10x4 com padrão de bordas).
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 14: Hipóteses Explicativas -->
      <div class="slide" data-topic="Discussão Teórica">
        <h2 class="slide-title">Hipóteses Explicativas do Comportamento</h2>
        <p class="slide-subtitle">Três hipóteses fundamentadas sobre o comportamento observado.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">1. Heurísticas Parciais</div>
            <div class="card-body">
              Os modelos podem ter desenvolvido operadores internos funcionais para simetrias regulares (~87%), mas não um motor puramente agnóstico a coordenadas.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">2. Viés Canônico</div>
            <div class="card-body">
              O pré-treinamento autoregressivo em texto pode induzir preferências por eixos de leitura padrão (da esquerda para a direita e de cima para baixo).
            </div>
          </div>

          <div class="card card-danger">
            <div class="card-title">3. Limite Composicional</div>
            <div class="card-body">
              No Merged, a combinação livre de operadores sobrecarrega a busca dedutiva, provocando alucinações de regras do pré-treino.
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 15: Rigor Metodológico -->
      <div class="slide" data-topic="Rigor Epistêmico">
        <h2 class="slide-title">Cuidados Metodológicos e Rigor Científico</h2>
        <p class="slide-subtitle">A postura científica necessária ao avaliar modelos caixa-preta.</p>

        <div class="grid-2">
          <div class="card card-brown">
            <div class="card-title">🛡️ O que os Dados Sustentam</div>
            <div class="card-body">
              <ul>
                <li>Alta estabilidade em simetrias atômicas (T_in == T_out).</li>
                <li>Colapso drástico sob perturbações compostas (T_in != T_out).</li>
                <li>Alucinações de regras públicas documentadas em log de reasoning.</li>
              </ul>
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">⚠️ Postura Epistêmica Cautelosa</div>
            <div class="card-body">
              <ul>
                <li>Tratamos as conclusões como <strong>hipóteses e indícios comportamentais</strong>, sem afirmações absolutas sobre pesos neurais.</li>
                <li>Foco no teste estrito de invariância sob perturbações controladas.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 16: Conclusões Finais -->
      <div class="slide" data-topic="Conclusão Geral">
        <h2 class="slide-title">Conclusão: Raciocínio vs. Memorização</h2>
        <p class="slide-subtitle">A resposta consolidada à questão central da pesquisa.</p>

        <div class="grid-2">
          <div class="card card-brown">
            <div class="card-title">🎯 Resposta à Pergunta Central</div>
            <div class="card-body">
              O desempenho dos LLMs reflete um <strong>regime híbrido</strong>: capacidade real de aplicar operadores simétricos básicos, combinada a uma <strong>alta vulnerabilidade quando a forma canônica memorizada é alterada</strong>.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">📊 Resumo do Duelo</div>
            <div class="card-body">
              <ul>
                <li><strong>Gemma 31B:</strong> Maior acurácia absoluta (+8.5 pp treino, +8.6 pp merged).</li>
                <li><strong>Gemini 3.5 Flash Lite:</strong> Maior eficiência operacional (8x mais rápido, empate técnico nas simetrias).</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 17: Próximos Passos (COM EXTENSÕES FUTURAS DETALHADAS) -->
      <div class="slide" data-topic="Próximos Passos">
        <h2 class="slide-title">Próximos Passos e Extensões da Pesquisa</h2>
        <p class="slide-subtitle">Continuidade da pesquisa e potenciais investigações futuras.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">📝 1. Artigo no Overleaf</div>
            <div class="card-body">
              Desenvolvimento e redação final do artigo científico em LaTeX no Overleaf com todas as tabelas e gráficos comparativos consolidados.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">🎓 2. Defesa na UFRGS</div>
            <div class="card-body">
              Apresentação formal dos resultados e entrega do relatório técnico final perante a banca avaliadora da disciplina de PCI.
            </div>
          </div>

          <div class="card card-success">
            <div class="card-title">🔬 3. Possíveis Extensões Futuras</div>
            <div class="card-body" style="font-size: 0.88rem; line-height: 1.45;">
              • <strong>Análise Cruzada de Falhas:</strong> Comparar erros em tarefas idênticas entre Gemma e Gemini para verificar se convergem para a mesma lógica falha.<br>
              • <strong>Taxonomia de Erros:</strong> Classificar individualmente as razões de falha (off-by-one, perda de cor, regra canônica) buscando padrões estruturados.<br>
              • <strong>Modelos Maiores:</strong> Avaliar modelos de maior escala para checar se a invariância composicional emerge.
            </div>
          </div>
        </div>

        <div style="text-align: center; margin-top: 26px; font-size: 0.92rem; font-weight: 800; color: var(--text-light);">
          UFRGS • Instituto de Informática • Projeto em Ciência e Inovação (PCI)
        </div>
      </div>

    </div>

    <!-- Bottom Footer -->
    <div class="bottom-footer">
      <button class="nav-btn" id="prevBtn" onclick="navSlide(-1)">← Anterior</button>
      <div style="font-size: 0.88rem; color: var(--text-muted); font-weight: 700;">
        Use as setas <kbd>←</kbd> <kbd>→</kbd> ou a barra de espaço para navegar
      </div>
      <button class="nav-btn btn-primary" id="nextBtn" onclick="navSlide(1)">Próximo →</button>
    </div>
  </div>
"""
    tail = get_shared_js()
    return head + body + tail


# ==============================================================================
# GERAÇÃO DA APRESENTAÇÃO COMPLETA (COM ROTEIRO DO ORADOR E LINK PARA RESUMIDA)
# ==============================================================================
def generate_completa():
    head = get_shared_head("Benchmark ARC-AGI: Raciocínio vs Memorização (Versão Completa • Roteiro do Apresentador)")
    
    body = f"""
  <div class="deck-container">
    <!-- Top Header (Com link para versão resumida) -->
    <div class="top-header">
      <div style="display: flex; align-items: center; gap: 14px;">
        <span class="topic-pill" id="slideTopic">Abertura</span>
        <a href="apresentacao_slides_benchmark_arc_resumida.html" class="switch-link">⚡ Ir para Versão Enxuta (Apresentação)</a>
      </div>
      <div class="slide-counter" id="slideCounter">Slide 1 de 17</div>
    </div>
    
    <div class="progress-track">
      <div class="progress-fill" id="progressFill"></div>
    </div>

    <!-- Viewport -->
    <div class="slide-viewport">

      <!-- SLIDE 1: Capa -->
      <div class="slide active" data-topic="Abertura & Apresentação">
        <div style="text-align: center; max-width: 1100px; margin: 0 auto;">
          <div style="display: inline-flex; align-items: center; gap: 12px; margin-bottom: 18px;">
            <span class="badge badge-gemma" style="font-size: 1rem; padding: 6px 18px;">Gemma 4 (31B-IT)</span>
            <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">VS</span>
            <span class="badge badge-gemini" style="font-size: 1rem; padding: 6px 18px;">Gemini 3.5 Flash Lite</span>
          </div>
          <h1 class="slide-title" style="font-size: 2.85rem; margin-bottom: 14px;">
            Benchmark ARC-AGI: Raciocínio Genuíno ou Memorização de Dados Públicos?
          </h1>
          <p class="slide-subtitle" style="font-size: 1.2rem; max-width: 950px; margin: 0 auto 30px;">
            Uma análise experimental da invariância geométrica e composicional de Modelos de Linguagem sob perturbações 2D.
          </p>

          <div class="grid-2" style="max-width: 950px; margin: 0 auto; text-align: left;">
            <div class="card card-brown">
              <div class="card-title" style="font-size: 0.92rem; color: var(--brown-espresso);">Discentes Responsáveis</div>
              <div class="card-body" style="font-weight: 800; font-size: 1.15rem; color: var(--brown-deep);">
                Gabriel • Leonardo • Luis
              </div>
            </div>
            <div class="card card-cognac">
              <div class="card-title" style="font-size: 0.92rem; color: var(--brown-cognac);">Corpo Docente & Avaliadores</div>
              <div class="card-body" style="font-weight: 800; font-size: 1.15rem; color: var(--brown-deep);">
                Prof. André • Profa. Érica • Prof. João • Prof. Frederico
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 2: Contexto do ARC-AGI -->
      <div class="slide" data-topic="Contexto & Motivação">
        <h2 class="slide-title">O que é o ARC-AGI e por que ele importa?</h2>
        <p class="slide-subtitle">A fronteira da inteligência artificial geral e a medição de adaptabilidade.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">🧩 Abstração Visual</div>
            <div class="card-body">
              Proposto por François Chollet (2019), o Abstraction and Reasoning Corpus avalia a capacidade de induzir regras lógicas complexas a partir de pouquíssimos exemplos visuais (Few-Shot 2D).
            </div>
          </div>
          <div class="card card-cognac">
            <div class="card-title">📐 Conhecimento A Priori</div>
            <div class="card-body">
              O ARC assume apenas princípios fundamentais de Core Knowledge humano: geometria, noções de conectividade, simetria, gravidade e contagem espacial.
            </div>
          </div>
          <div class="card card-terracotta">
            <div class="card-title">⚠️ O Problema da Web</div>
            <div class="card-body">
              O conjunto de treinamento original de 400 tarefas é público e amplamente discutido em fóruns e repositórios desde 2019, levantando a dúvida sobre contaminação prévia.
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Roteiro do Orador:</strong>
          "O ARC-AGI é considerado o padrão-ouro para avaliar se um modelo realmente pensa como humano ou se apenas interpola dados. Porém, a ampla circulação pública das 400 tasks originais nos força a perguntar: o acerto decorre de inteligência real ou de memorização de dados?"
        </div>
      </div>

      <!-- SLIDE 3: A Pergunta de Pesquisa (COM CASO 1 E CASO 2) -->
      <div class="slide" data-topic="Hipótese Epistêmica">
        <h2 class="slide-title">A Hipótese da Invariância Isomórfica</h2>
        <p class="slide-subtitle">A lógica abstrata deve ser preservada sob perturbações espaciais. Resultados esperados:</p>

        <div class="grid-2">
          <div class="card card-brown">
            <div class="card-title">💡 Caso 1: Raciocínio Genuíno (AGI)</div>
            <div class="card-body">
              Se um modelo de IA realmente compreendeu a regra abstrata intrínseca de uma matriz (por exemplo, conectar pontos da mesma cor), essa regra lógica deve ser invariante a transformações espaciais simples como rotações, reflexões e troca de cores.
            </div>
          </div>
          <div class="card card-danger">
            <div class="card-title">🔍 Caso 2: Memorização Canônica (Overfitting)</div>
            <div class="card-body">
              Se o modelo acertou o ARC porque decorou coordenadas canônicas ou padrões pré-treinados, pequenas perturbações espaciais (ou composições livres) quebrarão os acertos ou farão o modelo alucinar regras antigas do dataset público.
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Critério Experimental:</strong>
          "Nosso teste é simples: selecionamos apenas os problemas que cada modelo provou saber resolver no conjunto original e aplicamos perturbações sistemáticas. Se o modelo despencar, ele dependia da forma canônica memorizada."
        </div>
      </div>

      <!-- SLIDE 4: Metodologia e Pipeline de 2 Etapas -->
      <div class="slide" data-topic="Arquitetura Experimental">
        <h2 class="slide-title">Metodologia: Pipeline em 2 Etapas (solver.py)</h2>
        <p class="slide-subtitle">Isolando o raciocínio matemático da formatação determinística de matrizes.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">1. Raciocínio Profundo</div>
            <div class="card-body">
              <strong>High Thinking Process</strong><br>
              • Temperatura T = 0.6<br>
              • Cadeia de Pensamento livre (Chain-of-Thought)<br>
              • Exploração de hipóteses sem restrição de JSON
            </div>
          </div>
          <div class="card card-cognac">
            <div class="card-title">2. Extração Determinística</div>
            <div class="card-body">
              <strong>Formatação de Matriz</strong><br>
              • Modo Thinking: MINIMAL<br>
              • Temperatura T = 0.0 (Greedy)<br>
              • Extração estrita do grid numérico sem ruído sintático
            </div>
          </div>
          <div class="card card-success">
            <div class="card-title">3. Auditoria & Métricas</div>
            <div class="card-body">
              <strong>Persistência Segura</strong><br>
              • Pool de workers multi-chaves<br>
              • Gravação em 5 planilhas separadas (Acurácia, Grids, Reasoning, Tokens, Tempos)
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>A Prova da Matemática do Tempo:</strong>
          "A Etapa 1 leva centenas de segundos produzindo milhares de tokens de pensamento. A Etapa 2 leva apenas cerca de 5 segundos na mesma conexão HTTPS. Isso comprova cientificamente que mais de 99.9% do tempo medido é esforço de inferência das TPUs, e não atraso de rede."
        </div>
      </div>

      <!-- SLIDE 5: As 4 Famílias de Transformações 2D (COM FIGURA ASSIMÉTRICA NO MERGED) -->
      <div class="slide" data-topic="Geração das Novas Tasks">
        <h2 class="slide-title">As 4 Famílias de Transformações 2D</h2>
        <p class="slide-subtitle">Como as novas tarefas foram construídas matematicamente.</p>

        <div class="grid-4">
          <!-- Card Rotação -->
          <div class="card card-brown" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🔄 Rotação</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c1"></div><div class="m-cell c1"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">90° CW, 180°, 90° CCW<br><strong>Input == Output (Equivariante)</strong></p>
          </div>

          <!-- Card Reflexão -->
          <div class="card card-cognac" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🪞 Reflexão</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">Espelhamento Horizontal / Vertical<br><strong>Input == Output (Equivariante)</strong></p>
          </div>

          <!-- Card Coloração -->
          <div class="card card-terracotta" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🎨 Coloração</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-cognac); font-size: 1.2rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
                <div class="m-cell c8"></div><div class="m-cell c3"></div><div class="m-cell c8"></div>
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">Permutação 1:1 (com Cor 0 fixa)<br><strong>Input == Output (Equivariante)</strong></p>
          </div>

          <!-- Card Merged com figura assimétrica -->
          <div class="card card-danger" style="text-align: center;">
            <div class="card-title" style="justify-content: center;">🌪️ Merged</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 12px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 800; color: var(--brown-terracotta); font-size: 1.2rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 16px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c8"></div><div class="m-cell c8"></div>
              </div>
            </div>
            <p style="font-size: 0.86rem; color: var(--text-muted);">Rotação 90° + Reflexão + Cor (1→8, 2→3)<br><strong>Composição Livre</strong></p>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Diferença Chave:</strong>
          "Nas três primeiras famílias, a transformação é estritamente equivariante (o mesmo operador no input e output). No Merged, combinamos operadores de famílias distintas (como rotação somada à reflexão e troca de cores) preservando a coerência das regras."
        </div>
      </div>

      <!-- SLIDE 6: Tabela Comparativa de Acurácia -->
      <div class="slide" data-topic="Resultados • Acurácia">
        <h2 class="slide-title">Tabela Comparativa Oficial de Acurácia</h2>
        <p class="slide-subtitle">Desempenho comparado em todas as divisões experimentais.</p>

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset Avaliado</th>
                <th>Tasks Gemma</th>
                <th>Acurácia Gemma (31B)</th>
                <th>Tasks Gemini</th>
                <th>Acurácia Gemini (Flash Lite)</th>
                <th>Diferença (Gemma - Gemini)</th>
                <th>Comportamento Observado</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino ARC)</strong></td>
                <td>400</td>
                <td><span class="badge badge-gemma">76.00%</span> (304/400)</td>
                <td>400</td>
                <td><span class="badge badge-gemini">67.50%</span> (270/400)</td>
                <td><strong>+8.50 pp</strong></td>
                <td>Gemma aparenta ter maior recall no dataset público</td>
              </tr>
              <tr>
                <td><strong>Rotated (T_in == T_out)</strong></td>
                <td>304</td>
                <td><span class="badge badge-success">87.17%</span> (265/304)</td>
                <td>270</td>
                <td><span class="badge badge-success">85.56%</span> (231/270)</td>
                <td><strong>+1.62 pp</strong></td>
                <td>Alta invariância rotacional em ambos os modelos</td>
              </tr>
              <tr>
                <td><strong>Reflected (T_in == T_out)</strong></td>
                <td>304</td>
                <td><span class="badge badge-success">87.50%</span> (266/304)</td>
                <td>270</td>
                <td><span class="badge badge-success">87.04%</span> (235/270)</td>
                <td><strong>+0.46 pp</strong></td>
                <td>Empate técnico em reflexão axial</td>
              </tr>
              <tr>
                <td><strong>Coloration (T_in == T_out)</strong></td>
                <td>304</td>
                <td><span class="badge badge-success">89.14%</span> (271/304)</td>
                <td>270</td>
                <td><span class="badge badge-success">84.44%</span> (228/270)</td>
                <td><strong>+4.70 pp</strong></td>
                <td>Gemma ligeiramente superior em abstração de cores</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged (Composto & Assimétrico)</strong></td>
                <td>591</td>
                <td><span class="badge badge-danger">44.50%</span> (263/591)</td>
                <td>540</td>
                <td><span class="badge badge-danger">35.93%</span> (194/540)</td>
                <td><strong>+8.57 pp</strong></td>
                <td><strong>Colapso severo de desempenho em ambos os modelos (-43 a -50 pp)</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- SLIDE 7: INTERFACE INTERATIVA DE GRÁFICOS (BASE64 INTEGRADO) -->
      <div class="slide" data-topic="Resultados • Gráficos Interativos">
        <h2 class="slide-title">Explorador Interativo de Gráficos</h2>
        <p class="slide-subtitle">Selecione uma métrica abaixo para visualizar o gráfico detalhado em alta resolução.</p>

        <div class="chart-tabs">
          <button class="chart-tab-btn active" onclick="switchChartTab('geral', 'Visão Geral Comparativa 3 em 1 (Acurácia, Tokens e Tempo)', this)">📊 Visão Geral 3-em-1</button>
          <button class="chart-tab-btn" onclick="switchChartTab('acuracia', 'Comparativo Detalhado de Acurácia (%) por Dataset', this)">🎯 Taxa de Acurácia (%)</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tokens', 'Tokens Médios de Pensamento em Tarefas Corretas', this)">🧠 Tokens de Pensamento</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tempo', 'Tempo Médio de Execução por Tarefa em Segundos (Tasks Corretas)', this)">⏱️ Latência e Tempo (s)</button>
        </div>

        <div class="chart-display-frame">
          <img id="mainChartImg" src="data:image/png;base64,{b64_geral}" alt="Gráfico Comparativo ARC-AGI" style="max-width: 100%; max-height: 480px; object-fit: contain; border-radius: 8px;">
          <p id="chartDesc" style="margin-top: 10px; font-size: 0.92rem; font-weight: 700; color: var(--brown-espresso);">
            Visão Geral Comparativa 3 em 1 (Acurácia, Tokens e Tempo)
          </p>
        </div>
      </div>

      <!-- SLIDE 8: QUEM ACERTA MAIS VS QUEM É MAIS CONSISTENTE (AGORA SLIDE 8) -->
      <div class="slide" data-topic="Análise Comparativa">
        <h2 class="slide-title">Quem Acerta Mais vs. Quem é Mais Consistente?</h2>
        <p class="slide-subtitle">Avaliando volume bruto de acertos versus estabilidade a perturbações.</p>

        <div class="grid-2">
          <div class="card card-brown">
            <div class="card-title">🏆 Maior Taxa Bruta: Gemma 31B</div>
            <div class="card-body">
              <ul>
                <li>O Gemma 31B lidera em acurácia absoluta em todos os 5 cenários testados (+8.50 pp no original e +8.57 pp no Merged).</li>
                <li>Seus 31 bilhões de parâmetros parecem conferir maior capacidade de armazenar e processar raciocínios longos em contexto.</li>
              </ul>
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">⚖️ Consistência Atômica: Empate Técnico</div>
            <div class="card-body">
              <ul>
                <li>Em Reflexão e Rotação simples, a diferença entre Gemma e Gemini é de apenas 0.46 a 1.62 pontos percentuais.</li>
                <li>Ambos preservam entre 85% e 88% dos seus acertos originais sob perturbações simétricas puras.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="card card-danger" style="margin-top: 16px;">
          <div class="card-title" style="color: var(--brown-terracotta);">💥 A Ruptura Comum no Merged</div>
          <div class="card-body">
            Nenhum dos dois modelos resistiu à combinação livre de operadores: a acurácia cai para 44.5% no Gemma e 35.9% no Gemini, provando que a composição assimétrica de regras é o ponto de maior vulnerabilidade das duas arquiteturas.
          </div>
        </div>
      </div>

      <!-- SLIDE 9: ESTATÍSTICAS DE DISPERSÃO E EXTREMOS (AGORA SLIDE 9 COM FILTRO DUPLO) -->
      <div class="slide" data-topic="Estatísticas • Dispersão e Extremos">
        <h2 class="slide-title">Estatísticas de Dispersão e Extremos (Tasks Corretas)</h2>
        <p class="slide-subtitle">Mínimos, máximos, médias e desvio padrão calculados exclusivamente sobre as tarefas resolvidas com sucesso.</p>

        {get_dispersion_tables_html()}

        <div class="grid-2" style="margin-top: 14px;">
          <div class="card card-brown" style="padding: 14px 18px;">
            <div class="card-title" style="font-size: 0.95rem;">💡 Padrão de Tokens (Esforço Cognitivo)</div>
            <div class="card-body" style="font-size: 0.88rem;">
              O consumo mínimo de tokens fica na faixa de 1.700 a 2.500 em ambos os modelos quando a regra é direta. Já nos casos complexos, o Gemma atinge picos de quase 40.000 tokens e o Gemini alcança 24.000 tokens.
            </div>
          </div>
          <div class="card card-cognac" style="padding: 14px 18px;">
            <div class="card-title" style="font-size: 0.95rem;">⚡ Padrão de Tempo (Estabilidade Temporal)</div>
            <div class="card-body" style="font-size: 0.88rem;">
              O Gemini apresenta baixíssima latência mínima (4.2s a 4.9s) com desvio padrão restrito (~20-27s). O Gemma exige inferência densa prolongada (mínimo de 34s a 51s) com grande variância e tarefas que chegam a 868s (14,5 min).
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 10: TOKENS DE PENSAMENTO SEPARADOS POR MODELO -->
      <div class="slide" data-topic="Esforço Cognitivo • Tokens">
        <h2 class="slide-title">Análise de Tokens de Pensamento por Modelo</h2>
        <p class="slide-subtitle">Comparação do consumo em tarefas resolvidas com sucesso versus falhas.</p>

        <div class="grid-2" style="margin-bottom: 16px;">
          <!-- Card Gemma -->
          <div class="card card-brown">
            <div class="card-title" style="color: var(--badge-gemma-txt);">
              <span>🤖 Gemma 4 (31B-IT)</span>
              <span class="badge badge-gemma">Modelo Denso</span>
            </div>
            <div class="grid-3" style="margin: 12px 0 10px;">
              <div class="stat-card">
                <div class="stat-number" style="color: #2D6A4F; font-size: 1.8rem;">10.464</div>
                <div class="stat-label">Média Corretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-terracotta); font-size: 1.8rem;">16.221</div>
                <div class="stat-label">Média Incorretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-cognac); font-size: 1.8rem;">39.623</div>
                <div class="stat-label">Pico Máximo</div>
              </div>
            </div>
            <p style="font-size: 0.9rem; color: var(--text-muted);">
              O consumo de tokens do Gemma sobe em +55% quando a indução lógica falha.
            </p>
          </div>

          <!-- Card Gemini -->
          <div class="card card-cognac">
            <div class="card-title" style="color: var(--badge-gemini-txt);">
              <span>⚡ Gemini 3.5 Flash Lite</span>
              <span class="badge badge-gemini">Modelo Otimizado</span>
            </div>
            <div class="grid-3" style="margin: 12px 0 10px;">
              <div class="stat-card">
                <div class="stat-number" style="color: #2D6A4F; font-size: 1.8rem;">9.162</div>
                <div class="stat-label">Média Corretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-terracotta); font-size: 1.8rem;">15.586</div>
                <div class="stat-label">Média Incorretas</div>
              </div>
              <div class="stat-card">
                <div class="stat-number" style="color: var(--brown-cognac); font-size: 1.8rem;">33.643</div>
                <div class="stat-label">Pico Máximo</div>
              </div>
            </div>
            <p style="font-size: 0.9rem; color: var(--text-muted);">
              O consumo de tokens do Gemini salta em +70%, possivelmente por entrar em loops de busca em hipóteses inválidas.
            </p>
          </div>
        </div>

        <div class="card card-brown">
          <div class="card-title">💡 Insight Transversal Compartilhado</div>
          <div class="card-body">
            Ambos os modelos economizam de 35% a 40% de tokens quando encontram a hipótese correta rapidamente. Em contrapartida, diante de tarefas difíceis ou alteradas (Merged), os modelos geram longas cadeias de pensamento que acabam falhando.
          </div>
        </div>
      </div>

      <!-- SLIDE 11: Tempo e Throughput -->
      <div class="slide" data-topic="Latência & Throughput">
        <h2 class="slide-title">Tempo de Execução e Throughput</h2>
        <p class="slide-subtitle">A disparidade de velocidade de inferência entre as arquiteturas (médias sobre tarefas corretas).</p>

        <div class="grid-2" style="margin-bottom: 16px;">
          <div class="card card-cognac">
            <div class="card-title">⚡ Gemini 3.5 Flash Lite: Ultrarrápido</div>
            <div class="card-body">
              • Média de 28s a 32s por task nas simetrias e 32.3s no Merged.<br>
              • Resposta inicial em 1.38s.<br>
              • Permite processar lotes completos de centenas de tarefas em menos de 1 hora.
            </div>
          </div>

          <div class="card card-brown">
            <div class="card-title">🐢 Gemma 4 31B: Alto Custo de Latência</div>
            <div class="card-body">
              • Média de 225s a 238s por task nas simetrias e 288.2s no Merged.<br>
              • Operação a 25-50 tokens/s nas TPUs.<br>
              • Cada lote de 300 tasks exigiu mais de 20 horas acumuladas de inferência.
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Conclusão Prática:</strong>
          "O Gemini 3.5 Flash Lite é cerca de 7 a 8 vezes mais rápido com perda modesta de acurácia, tornando-se muito superior em termos de viabilidade de experimentação e custo por resposta."
        </div>
      </div>

      <!-- SLIDE 12: Estudo de Caso 1 (COM IDENTIFICAÇÃO CLARA DO MODELO) -->
      <div class="slide" data-topic="Estudo de Caso • Memorização">
        <h2 class="slide-title">Estudo de Caso 1: A "Regra Fantasma"</h2>
        <p class="slide-subtitle">Task f1cefba8 (Merged) — Evidência qualitativa de recuperação de pré-treino.</p>

        <div class="grid-2">
          <div class="card card-danger">
            <div class="card-title">
              <span>❌ O que o Modelo Escreveu</span>
              <span class="badge badge-gemma">Gemma 4 (31B)</span>
            </div>
            <div class="card-body">
              <p style="font-family: 'JetBrains Mono', monospace; font-size: 0.90rem; background: #FAF0EE; padding: 12px; border-radius: 6px; border: 1px solid #F5C7C1; color: #8B2519;">
                "...applying the cyclical color permutation 2 -> 3 -> 8 -> 2 from the previous examples..."
              </p>
              <p style="margin-top: 10px; font-size: 0.90rem;">
                No problema original, essa regra existia. Na nova task transformada, o ciclo foi quebrado intencionalmente (o 2 virava 2). O Gemma 31B ignorou a nova demonstração e aplicou a memória do dataset público!
              </p>
            </div>
          </div>

          <div class="card card-brown">
            <div class="card-title">🔍 Diagnóstico Científico</div>
            <div class="card-body">
              <ul>
                <li>O modelo reconheceu a silhueta geral da task memorizada no pré-treinamento.</li>
                <li>Ao entrar em sobrecarga de raciocínio no Merged, o Gemma desligou a dedução a partir do contexto e puxou a regra antiga da memória.</li>
                <li>Forte indício empírico de que parte do sucesso no dataset original vem de dados decorados.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 13: Estudo de Caso 2 (COM MODELO IDENTIFICADO EM CADA CARD E EXPLICAÇÃO DO VÍCIO LEFT-RIGHT) -->
      <div class="slide" data-topic="Estudo de Caso • Falhas Espaciais">
        <h2 class="slide-title">Estudo de Caso 2: Falhas de Ancoragem e Leitura</h2>
        <p class="slide-subtitle">Dificuldades com eixos invertidos identificadas individualmente nos modelos.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">
              <span>1. Task 0ac8ac11</span>
              <span class="badge badge-gemma">Gemma 31B</span>
            </div>
            <div class="card-body">
              A regra era classificar colunas por altura. Ao espelhar o grid em Reflexão, o Gemma inverteu índices (desenhou nas colunas 0, 2, 4 em vez de 1, 3, 5, 7) e inverteu a ordem de alturas, demonstrando vício de leitura da esquerda para a direita.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">
              <span>2. Task f7cb8069</span>
              <span class="badge badge-gemini">Gemini Flash</span>
            </div>
            <div class="card-body">
              Exigia traçar linhas a partir de cruzamentos. O Gemini traçou perfeitamente as horizontais e a 1ª vertical (coluna 1), mas errou a 2ª vertical (desenhou na coluna 7 em vez da 5).
            </div>
          </div>

          <div class="card card-terracotta">
            <div class="card-title">
              <span>3. Task 04e656f5</span>
              <span class="badge badge-gemini">Gemini Flash</span>
            </div>
            <div class="card-body">
              O objetivo era recortar um retângulo de 10x4. O Gemini gerou um quadrado 5x5 com diagonal simplificada, falhando tanto na inferência dimensional quanto no conteúdo.
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Por que o Vício Left-to-Right Ocorre? (Roteiro do Orador):</strong>
          "Os LLMs não possuem visão 2D nativa contínua; a matriz é linearizada como texto linha por linha, da esquerda para a direita (Left-to-Right). Durante o pré-treinamento, o modelo aprendeu que a informação à esquerda ancora a informação à direita. Quando um problema é espelhado e a regra passa a fluir da direita para a esquerda, há um conflito direto entre a direção geométrica da regra e a ordem autoregressiva de geração dos tokens, gerando erros sistemáticos de indexação."
        </div>
      </div>

      <!-- SLIDE 14: DISCUSSÃO E HIPÓTESES -->
      <div class="slide" data-topic="Discussão Teórica & Hipóteses">
        <h2 class="slide-title">Discussão e Hipóteses Explicativas</h2>
        <p class="slide-subtitle">Hipóteses fundamentadas sobre a representação interna dos LLMs em tarefas visuais.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">1. Heurísticas Parciais</div>
            <div class="card-body">
              A retenção de cerca de 85% a 89% em simetrias simples sugere a hipótese de que os modelos podem ter desenvolvido operadores internos funcionais para espelhamentos e rotações regulares, refutando a ideia de que sejam puramente memorizadores estáticos.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">2. Viés Canônico de Leitura</div>
            <div class="card-body">
              A arquitetura baseada em tokens pode induzir uma preferência por orientações canônicas. Inverter a direção dos dados parece aumentar a probabilidade de falhas de indexação espacial.
            </div>
          </div>

          <div class="card card-danger">
            <div class="card-title">3. Limite Composicional</div>
            <div class="card-body">
              O colapso no Merged indica que quando múltiplos operadores não-canônicos se combinam, o modelo pode não conseguir manter a coerência dedutiva, tendendo a recorrer a memórias do pré-treino.
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 15: Cuidados Metodológicos e Rigor Científico -->
      <div class="slide" data-topic="Rigor Metodológico">
        <h2 class="slide-title">Cuidados Metodológicos e Rigor Científico</h2>
        <p class="slide-subtitle">A postura científica necessária ao avaliar modelos de caixa-preta.</p>

        <div class="grid-2">
          <div class="card card-brown">
            <div class="card-title">🛡️ O que os Dados Empíricos Sustentam</div>
            <div class="card-body">
              • Os modelos demonstram alta retenção em transformações simétricas simples (T_in == T_out).<br>
              • Há uma degradação severa e replicável de desempenho sob transformações compostas (T_in != T_out).<br>
              • Existem evidências documentadas de recuperação de regras da base pública.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">⚠️ Postura Epistêmica Cautelosa</div>
            <div class="card-body">
              • Evitamos afirmações absolutas sobre os pesos neurais internos.<br>
              • Como não temos acesso aos gradientes durante a inferência, nossas conclusões são hipóteses fundamentadas no comportamento observável dos modelos frente a perturbações controladas.
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Para responder à banca:</strong>
          "Reconhecemos os limites de interpretabilidade das redes neurais profundas. Por isso, nosso estudo foca no teste comportamental rigoroso de invariância, que é um requisito formal para qualquer sistema que alegue generalização genuína."
        </div>
      </div>

      <!-- SLIDE 16: Conclusões Finais -->
      <div class="slide" data-topic="Conclusão Geral">
        <h2 class="slide-title">Conclusão: Raciocínio vs. Memorização</h2>
        <p class="slide-subtitle">A resposta final do estudo à questão central do ARC-AGI.</p>

        <div class="grid-2" style="margin-bottom: 16px;">
          <div class="card card-brown">
            <div class="card-title">🎯 Síntese da Resposta</div>
            <div class="card-body">
              Os dados empíricos indicam que o sucesso atual dos LLMs no ARC-AGI decorre de um sistema híbrido:<br><br>
              1. <strong>Capacidade Real Parcial:</strong> Os modelos possuem operadores equivariantes eficazes para simetrias geométricas regulares.<br>
              2. <strong>Dependência Canônica:</strong> Parte substancial dos acertos no dataset público depende de formas canônicas memorizadas, colapsando quando a simetria é perturbada.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">📊 Resumo do Duelo de Modelos</div>
            <div class="card-body">
              • <strong>Gemma 4 31B:</strong> Vencedor em acurácia absoluta em todos os testes (+8.5 pp treino, +8.6 pp merged).<br>
              • <strong>Gemini 3.5 Flash Lite:</strong> Vencedor absoluto em eficiência (7x a 8x mais rápido, consumo otimizado de tokens e estabilidade atômica idêntica).
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 17: PRÓXIMOS PASSOS (COM EXTENSÕES FUTURAS DETALHADAS) -->
      <div class="slide" data-topic="Próximos Passos">
        <h2 class="slide-title">Próximos Passos e Extensões da Pesquisa</h2>
        <p class="slide-subtitle">Continuidade da pesquisa e potenciais investigações futuras.</p>

        <div class="grid-3">
          <div class="card card-brown">
            <div class="card-title">📝 1. Artigo no Overleaf</div>
            <div class="card-body">
              Desenvolvimento e redação final do artigo científico em LaTeX no Overleaf, incorporando a metodologia, os gráficos comparativos em alta resolução e a discussão teórica.
            </div>
          </div>

          <div class="card card-cognac">
            <div class="card-title">🎓 2. Defesa na UFRGS</div>
            <div class="card-body">
              Consolidação do relatório técnico final e apresentação oral dos resultados para a banca avaliadora da disciplina de PCI.
            </div>
          </div>

          <div class="card card-success">
            <div class="card-title">🔬 3. Possíveis Extensões Futuras</div>
            <div class="card-body" style="font-size: 0.88rem; line-height: 1.45;">
              • <strong>Análise Cruzada de Falhas:</strong> Comparar erros em tarefas idênticas entre Gemma e Gemini para verificar se convergem para a mesma lógica falha.<br>
              • <strong>Taxonomia de Erros:</strong> Classificar individualmente as razões de falha (off-by-one, perda de cor, regra canônica) buscando padrões estruturados.<br>
              • <strong>Modelos Maiores:</strong> Avaliar modelos de maior escala para checar se a invariância composicional emerge.
            </div>
          </div>
        </div>

        <div style="text-align: center; margin-top: 28px; font-size: 0.95rem; font-weight: 800; color: var(--text-light);">
          UFRGS • Instituto de Informática • Projeto em Ciência e Inovação (PCI)
        </div>
      </div>

    </div>

    <!-- Bottom Footer -->
    <div class="bottom-footer">
      <button class="nav-btn" id="prevBtn" onclick="navSlide(-1)">← Anterior</button>
      <div style="font-size: 0.88rem; color: var(--text-muted); font-weight: 700;">
        Navegue com as setas <kbd>←</kbd> <kbd>→</kbd> ou barra de espaço
      </div>
      <button class="nav-btn btn-primary" id="nextBtn" onclick="navSlide(1)">Próximo →</button>
    </div>
  </div>
"""
    tail = get_shared_js()
    return head + body + tail

# Gera versão resumida
resumida_html = generate_resumida()
with open('Results/apresentacao_slides_benchmark_arc_resumida.html', 'w', encoding='utf-8') as f:
    f.write(resumida_html)
print(f'apresentacao_slides_benchmark_arc_resumida.html gerada ({len(resumida_html)} chars)')

# Gera versão completa
completa_html = generate_completa()
with open('Results/apresentacao_slides_benchmark_arc_completa.html', 'w', encoding='utf-8') as f:
    f.write(completa_html)
print(f'apresentacao_slides_benchmark_arc_completa.html gerada ({len(completa_html)} chars)')
