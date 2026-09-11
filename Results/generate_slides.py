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

# Carrega logo oficial da UFRGS em Base64
b64_logo_ufrgs = ""
if os.path.exists('Imagens/logo ufrgs.png'):
    with open('Imagens/logo ufrgs.png', 'rb') as f:
        b64_logo_ufrgs = base64.b64encode(f.read()).decode('utf-8')

print('Images & UFRGS Logo loaded to Base64 successfully.')

def get_shared_head(title):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-body: #F4EFE6;
      --bg-deck: #FFFFFF;
      --bg-cream: #FAF6F0;
      --bg-cream-card: #FFFFFF;
      --border-cream: #E5DCD1;
      --border-dark: #CBBDB0;
      
      --brown-deep: #261B14;
      --brown-espresso: #443224;
      --brown-cognac: #B86728;
      --brown-caramel: #D48B47;
      --brown-terracotta: #A64426;
      --brown-sand: #EADBC8;
      
      --text-main: #231B15;
      --text-muted: #5A4C40;
      --text-light: #8C7C6F;

      --badge-gemma-bg: #F5EAE0;
      --badge-gemma-txt: #5C3214;
      --badge-gemini-bg: #E8F0F5;
      --badge-gemini-txt: #1A4663;
      --badge-success-bg: #EAF4EC;
      --badge-success-txt: #1E6B37;
      --badge-danger-bg: #FDEEEB;
      --badge-danger-txt: #9C2617;
      
      --shadow-deck: 0 20px 50px -10px rgba(38, 27, 20, 0.12), 0 4px 18px -2px rgba(38, 27, 20, 0.05);
      --shadow-card: 0 4px 14px rgba(38, 27, 20, 0.04), 0 1px 3px rgba(38, 27, 20, 0.02);
      --radius-deck: 24px;
      --radius-card: 16px;
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
      max-width: 1580px;
      background: var(--bg-deck);
      border-radius: var(--radius-deck);
      border: 1px solid var(--border-cream);
      box-shadow: var(--shadow-deck);
      display: flex;
      flex-direction: column;
      min-height: 920px;
      overflow: hidden;
      position: relative;
    }}

    /* Barra Superior com Logo UFRGS e Pipeline */
    .top-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 48px;
      background: #FFFFFF;
      border-bottom: 1px solid var(--border-cream);
    }}

    .ufrgs-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .ufrgs-logo-img {{
      height: 52px;
      object-fit: contain;
    }}

    /* Pipeline de Seções */
    .nav-pipeline {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: #F4EFE6;
      padding: 6px 10px;
      border-radius: 9999px;
      border: 1px solid var(--border-cream);
    }}
    .nav-pill {{
      padding: 8px 20px;
      border-radius: 9999px;
      font-family: 'Outfit', sans-serif;
      font-size: 0.90rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      background: transparent;
      border: none;
      cursor: pointer;
      transition: all 0.2s ease;
      text-decoration: none;
    }}
    .nav-pill:hover {{
      color: var(--brown-deep);
      background: rgba(255, 255, 255, 0.7);
    }}
    .nav-pill.active {{
      background: var(--brown-deep);
      color: #FAF6F0;
      box-shadow: 0 2px 8px rgba(38, 27, 20, 0.2);
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .slide-counter {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.08rem;
      font-weight: 800;
      color: var(--brown-espresso);
    }}
    .hamburger-icon {{
      font-size: 1.4rem;
      color: var(--brown-deep);
      cursor: pointer;
      padding: 6px 10px;
      border-radius: 8px;
      background: #FAF6F0;
      border: 1px solid var(--border-cream);
    }}

    .progress-track {{ width: 100%; height: 5px; background: #EADBC8; }}
    .progress-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--brown-espresso), var(--brown-cognac), var(--brown-terracotta));
      transition: width 0.3s ease;
    }}

    /* Viewport de Slides */
    .slide-viewport {{
      flex: 1;
      padding: 44px 58px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      background: var(--bg-cream);
      position: relative;
    }}

    .slide {{
      display: none;
      opacity: 0;
      transform: translateY(10px);
      transition: opacity 0.25s ease, transform 0.25s ease;
      width: 100%;
    }}
    .slide.active {{
      display: flex;
      flex-direction: column;
      opacity: 1;
      transform: translateY(0);
    }}

    /* Tipografia de Alto Impacto e Escala Ampliada */
    h1, h2, h3, h4 {{ font-family: 'Outfit', sans-serif; color: var(--brown-deep); }}
    .slide-pretitle {{
      font-size: 2.3rem;
      font-weight: 800;
      color: var(--brown-cognac);
      margin-bottom: 8px;
      letter-spacing: -0.01em;
    }}
    .slide-title {{
      font-size: 4.4rem;
      font-weight: 900;
      line-height: 1.08;
      margin-bottom: 16px;
      letter-spacing: -0.02em;
    }}
    .slide-subtitle {{
      font-size: 1.7rem;
      color: var(--text-muted);
      margin-bottom: 28px;
      font-weight: 500;
      line-height: 1.45;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 1.05rem;
      font-weight: 800;
      font-family: 'Outfit', sans-serif;
    }}
    .badge-gemma {{ background: var(--badge-gemma-bg); color: var(--badge-gemma-txt); border: 1px solid #E5D5C5; }}
    .badge-gemini {{ background: var(--badge-gemini-bg); color: var(--badge-gemini-txt); border: 1px solid #CADBE7; }}
    .badge-success {{ background: var(--badge-success-bg); color: var(--badge-success-txt); border: 1px solid #C4DFC8; }}
    .badge-danger {{ background: var(--badge-danger-bg); color: var(--badge-danger-txt); border: 1px solid #F3C9C3; }}

    /* Grid & Cards Modernos */
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
    .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}

    .card {{
      background: var(--bg-cream-card);
      border-radius: var(--radius-card);
      padding: 30px 36px;
      border: 1px solid var(--border-cream);
      box-shadow: var(--shadow-card);
    }}
    .card-brown {{ border-left: 6px solid var(--brown-espresso); }}
    .card-cognac {{ border-left: 6px solid var(--brown-cognac); }}
    .card-terracotta {{ border-left: 6px solid var(--brown-terracotta); }}
    .card-success {{ border-left: 6px solid #1E6B37; background: #FCFDFB; }}
    .card-danger {{ border-left: 6px solid #9C2617; background: #FFFDFD; }}

    .card-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 1.75rem;
      font-weight: 800;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .card-body {{
      font-size: 1.4rem;
      line-height: 1.65;
      color: var(--text-main);
    }}
    .card-body ul {{
      padding-left: 26px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    /* Estilo de Citações e Hipótese */
    .quote-hero {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 700;
      color: var(--brown-deep);
      background: #FFFFFF;
      border-radius: 20px;
      border: 1px solid var(--border-cream);
      box-shadow: var(--shadow-card);
      position: relative;
    }}

    .hypo-box {{
      display: flex;
      align-items: flex-start;
      background: #FFFFFF;
      border-radius: 18px;
      border: 1px solid var(--border-cream);
      box-shadow: var(--shadow-card);
    }}

    /* Observação Box */
    .obs-box {{
      background: #F5EDE4;
      border: 1px solid var(--border-cream);
      border-radius: 14px;
      padding: 16px 22px;
      font-size: 1.15rem;
      line-height: 1.55;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    /* Tabelas */
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
      font-size: 1.15rem;
    }}
    .data-table th {{
      background: #F5EFE6;
      color: var(--brown-deep);
      font-family: 'Outfit', sans-serif;
      font-weight: 800;
      padding: 16px 20px;
      border-bottom: 2px solid var(--border-cream);
    }}
    .data-table td {{
      padding: 15px 20px;
      border-bottom: 1px solid var(--border-cream);
      color: var(--text-main);
    }}
    .data-table tr:last-child td {{ border-bottom: none; }}
    .data-table tr:hover td {{ background: #FAF6F0; }}
    .data-table tr.highlight td {{ background: #FDF4F2; font-weight: 700; }}

    /* Gráficos Interativos */
    .chart-tabs {{
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}
    .chart-tab-btn {{
      padding: 10px 22px;
      border-radius: 10px;
      font-family: 'Outfit', sans-serif;
      font-size: 1.08rem;
      font-weight: 800;
      border: 1px solid var(--border-cream);
      background: #FFFFFF;
      color: var(--brown-espresso);
      cursor: pointer;
      transition: all 0.2s;
    }}
    .chart-tab-btn:hover {{ background: #F5ECE0; }}
    .chart-tab-btn.active {{
      background: var(--brown-deep);
      color: #FAF6F0;
      border-color: var(--brown-deep);
      box-shadow: 0 3px 8px rgba(38, 27, 20, 0.2);
    }}

    .chart-display-frame {{
      background: #FFFFFF;
      border-radius: var(--radius-card);
      border: 1px solid var(--border-cream);
      padding: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 490px;
      box-shadow: var(--shadow-card);
    }}

    /* Filtros da Tabela */
    .filter-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .filter-group {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .filter-btn {{
      padding: 8px 18px;
      border-radius: 8px;
      font-family: 'Outfit', sans-serif;
      font-size: 1rem;
      font-weight: 700;
      border: 1px solid var(--border-cream);
      background: #FFFFFF;
      color: var(--brown-espresso);
      cursor: pointer;
      transition: all 0.2s;
    }}
    .filter-btn:hover {{ background: #F5ECE0; }}
    .filter-btn.active {{
      background: var(--brown-deep);
      color: #FAF6F0;
      border-color: var(--brown-deep);
    }}

    /* Matrizes 2D */
    .matrix-box {{
      display: inline-grid;
      gap: 2px;
      background: #E8DDD0;
      padding: 4px;
      border-radius: 6px;
      border: 1px solid #D5C7B7;
    }}
    .m-cell {{ width: 20px; height: 20px; border-radius: 3px; }}
    .c0 {{ background: #000000; }}
    .c1 {{ background: #3B82F6; }}
    .c2 {{ background: #EF4444; }}
    .c3 {{ background: #10B981; }}
    .c4 {{ background: #F59E0B; }}
    .c8 {{ background: #06B6D4; }}

    /* Roteiro do Orador (Completa) */
    .speaker-script {{
      background: #FFFFFF;
      border-left: 6px solid var(--brown-cognac);
      border-radius: 12px;
      padding: 16px 24px;
      margin-top: 20px;
      font-size: 1.08rem;
      line-height: 1.6;
      color: var(--brown-espresso);
      border-top: 1px solid var(--border-cream);
      border-right: 1px solid var(--border-cream);
      border-bottom: 1px solid var(--border-cream);
    }}
    .speaker-script strong {{ color: var(--brown-deep); }}

    /* Rodapé com Navegação */
    .bottom-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 48px;
      background: #FFFFFF;
      border-top: 1px solid var(--border-cream);
    }}
    
    .nav-btn {{
      padding: 12px 28px;
      border-radius: 12px;
      font-family: 'Outfit', sans-serif;
      font-size: 1.08rem;
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
    .nav-btn.btn-primary:disabled {{ opacity: 0.3; cursor: not-allowed; }}

    .switch-link {{
      font-size: 0.94rem;
      font-weight: 800;
      color: var(--brown-cognac);
      text-decoration: none;
      padding: 8px 18px;
      border-radius: 10px;
      background: #F6ECE0;
      border: 1px solid #E8D3BF;
      transition: all 0.2s;
    }}
    .switch-link:hover {{ background: #EEDCCE; }}

    kbd {{
      background: #F0EAE1;
      border: 1px solid #D5C8B8;
      border-radius: 4px;
      padding: 2px 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
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
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const navPills = document.querySelectorAll('.nav-pill');

    function renderSlide() {{
      slides.forEach((s, idx) => {{
        s.classList.toggle('active', idx === currentIdx);
      }});

      const activeElem = slides[currentIdx];
      const section = activeElem.getAttribute('data-section') || 'INTRODUÇÃO';

      // Atualiza o pill ativo
      navPills.forEach(p => {{
        if (p.getAttribute('data-sec') === section) {{
          p.classList.add('active');
        }} else {{
          p.classList.remove('active');
        }}
      }});

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

    function goToSection(sectionName) {{
      for (let i = 0; i < slides.length; i++) {{
        if (slides[i].getAttribute('data-section') === sectionName) {{
          currentIdx = i;
          renderSlide();
          break;
        }}
      }}
    }}

    function switchChartTab(chartKey, descText, btnElem) {{
      const img = document.getElementById('mainChartImg');
      const desc = document.getElementById('chartDesc');
      if (img && CHART_IMAGES[chartKey]) {{
        img.src = CHART_IMAGES[chartKey];
      }}
      if (desc) desc.innerText = descText;

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

# Bloco HTML das tabelas de dispersão estatística
def get_dispersion_tables_html():
    return """
        <!-- Barra de Filtros Dupla (Modelo e Métrica) -->
        <div class="filter-bar">
          <div class="filter-group">
            <span style="font-size: 1.05rem; font-weight: 800; color: var(--brown-espresso);">Modelo:</span>
            <button class="filter-btn btn-stat-model active" onclick="setStatModel('gemma', this)">Gemma 4 (31B)</button>
            <button class="filter-btn btn-stat-model" onclick="setStatModel('gemini', this)">Gemini 3.5 Flash Lite</button>
            <button class="filter-btn btn-stat-model" onclick="setStatModel('compare', this)">Gemma vs. Gemini</button>
          </div>
          <div class="filter-group">
            <span style="font-size: 1.05rem; font-weight: 800; color: var(--brown-espresso);">Métrica:</span>
            <button class="filter-btn btn-stat-metric active" onclick="setStatMetric('both', this)">Visão Completa</button>
            <button class="filter-btn btn-stat-metric" onclick="setStatMetric('tokens', this)">Apenas Tokens</button>
            <button class="filter-btn btn-stat-metric" onclick="setStatMetric('time', this)">Apenas Tempo (s)</button>
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

        <!-- 2. GEMMA - TOKENS -->
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

        <!-- 3. GEMMA - TEMPO -->
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

        <!-- 5. GEMINI - TOKENS -->
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

        <!-- 6. GEMINI - TEMPO -->
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

        <!-- 7. COMPARATIVO - TOKENS -->
        <div class="table-wrapper stats-view-table" id="stats_compare_tokens" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma (Média ± σ)</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma (Mín - Máx)</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini (Média ± σ)</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini (Mín - Máx)</th>
                <th>Diferença (Gemma − Gemini)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">9.856,1 ± 3.411,4</td>
                <td style="background: #FAF4EE;">2.510 - 20.646</td>
                <td style="background: #F3F7FA; font-weight: 700;">9.462,6 ± 4.906,4</td>
                <td style="background: #F3F7FA;">1.920 - 23.493</td>
                <td style="font-weight: 800;">+393,4 tokens</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">9.851,3 ± 3.921,2</td>
                <td style="background: #FAF4EE;">2.064 - 39.623</td>
                <td style="background: #F3F7FA; font-weight: 700;">8.944,5 ± 4.562,3</td>
                <td style="background: #F3F7FA;">1.910 - 23.979</td>
                <td style="font-weight: 800;">+906,8 tokens</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">9.732,0 ± 3.694,2</td>
                <td style="background: #FAF4EE;">2.148 - 19.993</td>
                <td style="background: #F3F7FA; font-weight: 700;">8.918,5 ± 4.411,4</td>
                <td style="background: #F3F7FA;">1.826 - 22.480</td>
                <td style="font-weight: 800;">+813,5 tokens</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">9.923,4 ± 3.393,4</td>
                <td style="background: #FAF4EE;">2.538 - 20.492</td>
                <td style="background: #F3F7FA; font-weight: 700;">8.991,8 ± 4.402,8</td>
                <td style="background: #F3F7FA;">1.759 - 23.611</td>
                <td style="font-weight: 800;">+931,7 tokens</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">11.537,0 ± 3.790,9</td>
                <td style="background: #FAF4EE;">3.310 - 20.561</td>
                <td style="background: #F3F7FA; font-weight: 700;">10.504,4 ± 4.773,9</td>
                <td style="background: #F3F7FA;">1.816 - 22.401</td>
                <td style="font-weight: 800;">+1.032,5 tokens</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 8. COMPARATIVO - TEMPO -->
        <div class="table-wrapper stats-view-table" id="stats_compare_time" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma (Média ± σ)</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma (Mín - Máx)</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini (Média ± σ)</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini (Mín - Máx)</th>
                <th>Aceleração do Gemini</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">208,1s ± 73,2s</td>
                <td style="background: #FAF4EE;">47,6s - 435,1s</td>
                <td style="background: #F3F7FA; font-weight: 700;">27,5s ± 19,4s</td>
                <td style="background: #F3F7FA;">4,9s - 173,7s</td>
                <td style="font-weight: 800; color: #1E6B37;">7.6x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">222,4s ± 105,1s</td>
                <td style="background: #FAF4EE;">34,5s - 868,6s</td>
                <td style="background: #F3F7FA; font-weight: 700;">31,3s ± 22,3s</td>
                <td style="background: #F3F7FA;">4,2s - 113,7s</td>
                <td style="font-weight: 800; color: #1E6B37;">7.1x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">218,9s ± 93,8s</td>
                <td style="background: #FAF4EE;">38,4s - 572,3s</td>
                <td style="background: #F3F7FA; font-weight: 700;">28,7s ± 25,2s</td>
                <td style="background: #F3F7FA;">4,5s - 198,8s</td>
                <td style="font-weight: 800; color: #1E6B37;">7.6x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">227,9s ± 99,3s</td>
                <td style="background: #FAF4EE;">51,7s - 705,2s</td>
                <td style="background: #F3F7FA; font-weight: 700;">28,0s ± 21,0s</td>
                <td style="background: #F3F7FA;">4,2s - 113,8s</td>
                <td style="font-weight: 800; color: #1E6B37;">8.1x mais rápido</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td style="background: #FAF4EE; font-weight: 700;">285,1s ± 131,5s</td>
                <td style="background: #FAF4EE;">67,8s - 805,3s</td>
                <td style="background: #F3F7FA; font-weight: 700;">32,5s ± 27,9s</td>
                <td style="background: #F3F7FA;">4,7s - 266,0s</td>
                <td style="font-weight: 800; color: #1E6B37;">8.8x mais rápido</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 9. COMPARATIVO - COMPLETO -->
        <div class="table-wrapper stats-view-table" id="stats_compare_both" style="display: none;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Dataset</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma Tokens</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini Tokens</th>
                <th style="background: #F5EAE0; color: #5C3214;">Gemma Tempo</th>
                <th style="background: #E8F0F5; color: #1A4663;">Gemini Tempo</th>
                <th>Diferença Acurácia</th>
                <th>Aceleração Gemini</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td style="background: #FAF4EE;">9.856,1</td>
                <td style="background: #F3F7FA;">9.462,6</td>
                <td style="background: #FAF4EE;">208,1s</td>
                <td style="background: #F3F7FA;">27,5s</td>
                <td style="font-weight: 800;">+0.00 pp</td>
                <td style="font-weight: 800; color: #1E6B37;">7.6x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td style="background: #FAF4EE;">9.851,3</td>
                <td style="background: #F3F7FA;">8.944,5</td>
                <td style="background: #FAF4EE;">222,4s</td>
                <td style="background: #F3F7FA;">31,3s</td>
                <td style="font-weight: 800;">+3.97 pp</td>
                <td style="font-weight: 800; color: #1E6B37;">7.1x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td style="background: #FAF4EE;">9.732,0</td>
                <td style="background: #F3F7FA;">8.918,5</td>
                <td style="background: #FAF4EE;">218,9s</td>
                <td style="background: #F3F7FA;">28,7s</td>
                <td style="font-weight: 800;">+3.17 pp</td>
                <td style="font-weight: 800; color: #1E6B37;">7.6x mais rápido</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td style="background: #FAF4EE;">9.923,4</td>
                <td style="background: #F3F7FA;">8.991,8</td>
                <td style="background: #FAF4EE;">227,9s</td>
                <td style="background: #F3F7FA;">28,0s</td>
                <td style="font-weight: 800;">+8.33 pp</td>
                <td style="font-weight: 800; color: #1E6B37;">8.1x mais rápido</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td style="background: #FAF4EE;">11.537,0</td>
                <td style="background: #F3F7FA;">10.504,4</td>
                <td style="background: #FAF4EE;">285,1s</td>
                <td style="background: #F3F7FA;">32,5s</td>
                <td style="font-weight: 800;">+11.39 pp</td>
                <td style="font-weight: 800; color: #1E6B37;">8.8x mais rápido</td>
              </tr>
            </tbody>
          </table>
        </div>
    """


# ==============================================================================
# GERAÇÃO DA APRESENTAÇÃO RESUMIDA (ENXUTA, DIRETA, CONFORME REQUISITOS)
# ==============================================================================
def generate_resumida():
    head = get_shared_head("Benchmark ARC-AGI: Raciocínio vs Memorização (Apresentação Resumida)")
    
    body = f"""
  <div class="deck-container">
    <!-- Top Header com Logo UFRGS e Pipeline de 6 Seções (Exemplo dentro de Discussão) -->
    <div class="top-header">
      <div class="ufrgs-brand">
        <img src="data:image/png;base64,{b64_logo_ufrgs}" alt="UFRGS" class="ufrgs-logo-img">
      </div>

      <!-- Barra de Seções -->
      <div class="nav-pipeline">
        <button class="nav-pill active" data-sec="INTRODUÇÃO" onclick="goToSection('INTRODUÇÃO')">Introdução</button>
        <button class="nav-pill" data-sec="HIPÓTESE" onclick="goToSection('HIPÓTESE')">Hipótese</button>
        <button class="nav-pill" data-sec="DESENVOLVIMENTO" onclick="goToSection('DESENVOLVIMENTO')">Desenvolvimento</button>
        <button class="nav-pill" data-sec="RESULTADOS" onclick="goToSection('RESULTADOS')">Resultados</button>
        <button class="nav-pill" data-sec="DISCUSSÃO" onclick="goToSection('DISCUSSÃO')">Discussão</button>
        <button class="nav-pill" data-sec="CONCLUSÃO" onclick="goToSection('CONCLUSÃO')">Conclusão</button>
      </div>

      <div class="header-right">
        <div class="slide-counter" id="slideCounter">Slide 1 de 11</div>
        <div class="hamburger-icon">☰</div>
      </div>
    </div>
    
    <div class="progress-track">
      <div class="progress-fill" id="progressFill"></div>
    </div>

    <!-- Viewport -->
    <div class="slide-viewport">

      <!-- SLIDE 1: Capa -->
      <div class="slide active" data-section="INTRODUÇÃO">
        <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; align-items: center; width: 100%;">
          <div>
            <div style="font-size: 2.6rem; font-weight: 800; color: var(--brown-cognac); margin-bottom: 8px;">ARC-AGI:</div>
            <h1 style="font-size: 5.6rem; font-weight: 900; line-height: 1.02; color: var(--brown-deep); margin-bottom: 28px;">
              Raciocínio<br>ou<br>Memorização?
            </h1>

            <div style="margin-bottom: 28px;">
              <div style="background: #F4EFE6; padding: 14px 24px; border-radius: 14px; display: inline-flex; align-items: center; gap: 14px; border: 1px solid var(--border-cream);">
                <span class="badge" style="background: #FFFFFF; color: var(--brown-deep); font-weight: 900; font-size: 1.1rem;">ARC-AGI 💡</span>
                <span style="font-size: 1.2rem; font-weight: 700; color: var(--brown-espresso);">Testes para medir raciocínio abstrato de inteligências artificiais</span>
              </div>
            </div>

            <div style="display: inline-flex; align-items: center; gap: 14px;">
              <span class="badge badge-gemma" style="font-size: 1.18rem; padding: 10px 22px;">Gemma 4 (31B)</span>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.3rem; background: #F5EDE4; padding: 6px 14px; border-radius: 8px;">VS</span>
              <span class="badge badge-gemini" style="font-size: 1.18rem; padding: 10px 22px;">Gemini 3.5 Flash-Lite</span>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 22px;">
            <div class="card card-brown" style="padding: 28px 32px;">
              <div style="font-size: 1.1rem; font-weight: 800; color: var(--brown-cognac); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Discentes</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: var(--brown-deep); line-height: 1.6;">
                • Gabriel Pieruccini Knopp<br>
                • Leonardo Greco Fin<br>
                • Luis Henrique Caselani Macedo Junior
              </div>
            </div>

            <div class="card card-cognac" style="padding: 28px 32px;">
              <div style="font-size: 1.1rem; font-weight: 800; color: var(--brown-terracotta); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Docentes</div>
              <div style="font-size: 1.25rem; font-weight: 700; color: var(--brown-deep); line-height: 1.6;">
                • Prof. André Grahl Pereira<br>
                • Profa. Érika Fernandes Cota<br>
                • Prof. Frederico Messa Schwartzhaupt<br>
                • Prof. João Cesar Netto
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 2: Hipótese -->
      <div class="slide" data-section="HIPÓTESE">
        <div class="slide-pretitle" style="font-size: 2.6rem;">O que esperamos?</div>
        <h2 class="slide-title" style="font-size: 5.6rem; margin-bottom: 20px;">Hipótese</h2>

        <div style="display: grid; grid-template-columns: 1fr 1.15fr; gap: 40px; align-items: center; margin-top: 20px;">
          <div>
            <div class="quote-hero" style="font-size: 2.8rem; font-style: italic; text-align: center; line-height: 1.35; padding: 48px 44px; border-left: 14px solid var(--brown-deep);">
              “Os modelos de linguagem possuem AGI.”
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 24px;">
            <div class="hypo-box" style="border-left: 10px solid #1E6B37; padding: 32px 36px; font-size: 1.7rem; line-height: 1.45;">
              <div style="color: #1E6B37; font-size: 2.4rem; font-weight: 900; line-height: 1;">▲</div>
              <div>
                <strong>Rotacionar, Refletir ou Permutar cores</strong><br>
                <span style="color: #1E6B37; font-weight: 800;">NÃO altera</span> o resultado.
              </div>
            </div>

            <div class="hypo-box" style="border-left: 10px solid #9C2617; padding: 32px 36px; font-size: 1.7rem; line-height: 1.45;">
              <div style="color: #9C2617; font-size: 2.4rem; font-weight: 900; line-height: 1;">▲</div>
              <div>
                <strong>Rotacionar, Refletir ou Permutar cores</strong><br>
                <span style="color: #9C2617; font-weight: 800;">PODE alterar</span> o resultado.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 3: Metodologia (Texto Ampliado) -->
      <div class="slide" data-section="DESENVOLVIMENTO">
        <div class="slide-pretitle">Como testamos?</div>
        <h2 class="slide-title">Desenvolvimento: Metodologia</h2>

        <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 36px; margin-top: 14px;">
          <div class="card card-brown" style="padding: 36px 40px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: var(--brown-cognac); margin-bottom: 22px;">
              Divisão em duas chamadas por task
            </div>
            
            <div style="margin-bottom: 26px;">
              <strong style="font-size: 1.65rem; color: var(--brown-deep);">Reasoning (Raciocínio)</strong>
              <ul style="margin-top: 10px; font-size: 1.45rem; padding-left: 28px; line-height: 1.65; color: var(--text-main);">
                <li>Temperatura T = 0.6</li>
                <li>Modo High Thinking</li>
                <li>Exploração profunda de hipóteses</li>
              </ul>
            </div>

            <div>
              <strong style="font-size: 1.65rem; color: var(--brown-deep);">Formatting (Extração)</strong>
              <ul style="margin-top: 10px; font-size: 1.45rem; padding-left: 28px; line-height: 1.65; color: var(--text-main);">
                <li>Temperatura T = 0.0</li>
                <li>Modo Minimal Thinking</li>
                <li>Extração estrita do grid numérico</li>
              </ul>
            </div>
          </div>

          <div class="card card-cognac" style="padding: 36px 40px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: var(--brown-terracotta); margin-bottom: 22px;">
              Métricas analisadas
            </div>

            <div style="display: flex; flex-direction: column; gap: 24px;">
              <div>
                <strong style="color: var(--brown-deep); font-size: 1.55rem;">Taxa de acurácia:</strong>
                <p style="color: var(--text-muted); font-size: 1.4rem; margin-top: 6px; line-height: 1.5;">Consistência entre transformações e modelos.</p>
              </div>
              <div>
                <strong style="color: var(--brown-deep); font-size: 1.55rem;">Tokens gastos:</strong>
                <p style="color: var(--text-muted); font-size: 1.4rem; margin-top: 6px; line-height: 1.5;">Dificuldade e esforço computacional.</p>
              </div>
              <div>
                <strong style="color: var(--brown-deep); font-size: 1.55rem;">Tempo gasto:</strong>
                <p style="color: var(--text-muted); font-size: 1.4rem; margin-top: 6px; line-height: 1.5;">Eficiência na resolução das matrizes.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 4: Transformações -->
      <div class="slide" data-section="DESENVOLVIMENTO">
        <div class="slide-pretitle">Como geramos?</div>
        <h2 class="slide-title">Desenvolvimento: Transformações</h2>
        <p class="slide-subtitle">Derivadas exclusivamente das tarefas acertadas previamente por cada modelo.</p>

        <div class="grid-4" style="margin-top: 10px;">
          <div class="card card-brown" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🔄 Rotação</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c1"></div><div class="m-cell c1"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 700; color: var(--text-muted); text-align: center;">90° CW, 180°, 90° CCW</p>
          </div>

          <div class="card card-cognac" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🪞 Reflexão</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 700; color: var(--text-muted); text-align: center;">Espelhamento Axial</p>
          </div>

          <div class="card card-terracotta" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🎨 Coloração</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
                <div class="m-cell c8"></div><div class="m-cell c3"></div><div class="m-cell c8"></div>
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 700; color: var(--text-muted); text-align: center;">Permutação de Paleta</p>
          </div>

          <div class="card card-danger" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🌪️ Merged</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-terracotta); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c8"></div><div class="m-cell c8"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 700; color: var(--brown-terracotta); text-align: center;">Rotação + Reflexão + Cores</p>
          </div>
        </div>
      </div>

      <!-- SLIDE 5: Acurácia -->
      <div class="slide" data-section="RESULTADOS">
        <div class="slide-pretitle">O que obtivemos?</div>
        <h2 class="slide-title">Resultados: Acurácia</h2>
        <p class="slide-subtitle">Comparação: Gemma vs Gemini</p>

        <div class="table-wrapper">
          <table class="data-table" style="font-size: 1.22rem;">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Gemma 4 (31B)</th>
                <th>Gemini 3.5 Flash Lite</th>
                <th>Diferença</th>
                <th>Comportamento Observado</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td><span class="badge badge-gemma">76.00%</span> (304/400)</td>
                <td><span class="badge badge-gemini">67.50%</span> (270/400)</td>
                <td><strong>+8.50 pp</strong></td>
                <td>Gemma aparenta ter maior retenção no dataset público</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td><span class="badge badge-success">87.17%</span> (265/304)</td>
                <td><span class="badge badge-success">85.56%</span> (231/270)</td>
                <td><strong>+1.62 pp</strong></td>
                <td>Alta estabilidade sob rotação</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td><span class="badge badge-success">87.50%</span> (266/304)</td>
                <td><span class="badge badge-success">87.04%</span> (235/270)</td>
                <td><strong>+0.46 pp</strong></td>
                <td>Desempenho quase equivalente em reflexão</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td><span class="badge badge-success">89.14%</span> (271/304)</td>
                <td><span class="badge badge-success">84.44%</span> (228/270)</td>
                <td><strong>+4.70 pp</strong></td>
                <td>Gemma ligeiramente superior em cores</td>
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

      <!-- SLIDE 6: Gráficos -->
      <div class="slide" data-section="RESULTADOS">
        <div class="slide-pretitle">O que podemos ver?</div>
        <h2 class="slide-title">Resultados: Gráficos</h2>

        <div class="chart-tabs">
          <button class="chart-tab-btn active" onclick="switchChartTab('geral', 'Visão Geral 3-em-1 (Acurácia, Tokens e Tempo)', this)">Visão Geral 3-em-1</button>
          <button class="chart-tab-btn" onclick="switchChartTab('acuracia', 'Comparativo de Acurácia (%) por Dataset', this)">Taxa de Acurácia (%)</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tokens', 'Tokens Médios de Pensamento em Tarefas Corretas', this)">Tokens de Pensamento</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tempo', 'Tempo Médio de Execução por Tarefa (s)', this)">Tempo de Inferência (s)</button>
        </div>

        <div class="chart-display-frame">
          <img id="mainChartImg" src="data:image/png;base64,{b64_geral}" alt="Gráfico Comparativo ARC-AGI" style="max-width: 100%; max-height: 480px; object-fit: contain; border-radius: 8px;">
          <p id="chartDesc" style="margin-top: 10px; font-size: 1.18rem; font-weight: 800; color: var(--brown-deep);">
            Visão Geral 3-em-1 (Acurácia, Tokens e Tempo)
          </p>
        </div>
      </div>

      <!-- SLIDE 7: Estatísticas -->
      <div class="slide" data-section="RESULTADOS">
        <div class="slide-pretitle">Como estão distribuídos?</div>
        <h2 class="slide-title">Resultados: Estatísticas</h2>
        <p class="slide-subtitle">Métricas calculadas exclusivamente sobre as tarefas resolvidas com sucesso.</p>

        {get_dispersion_tables_html()}
      </div>

      <!-- SLIDE 8: Discussão: Exemplo -->
      <div class="slide" data-section="DISCUSSÃO">
        <div class="slide-pretitle">Como erraram?</div>
        <h2 class="slide-title">Discussão: Exemplo</h2>
        <p class="slide-subtitle">Task f1cefba8 (Merged) — Alucinação da regra original da base pública.</p>

        <div class="grid-2" style="margin-top: 14px;">
          <div class="card card-danger" style="padding: 34px 38px;">
            <div class="card-title" style="font-size: 1.75rem; margin-bottom: 18px;">
              <span>Evidência no Reasoning</span>
              <span class="badge badge-gemma">Gemma 4 (31B)</span>
            </div>
            <div class="card-body">
              <p style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; background: #FDEEEB; padding: 18px; border-radius: 10px; color: #9C2617; border: 1px solid #F3C9C3; font-weight: 700;">
                "...following the cycle 2 -> 3 -> 8 -> 2..."
              </p>
              <p style="margin-top: 18px; font-size: 1.45rem; line-height: 1.65; text-align: center;">
                Essa regra existia na base pública original, mas havia sido <strong>removida no JSON transformado</strong>.
              </p>
            </div>
          </div>

          <div class="card card-brown" style="padding: 34px 38px; display: flex; flex-direction: column; justify-content: center;">
            <div class="card-title" style="font-size: 1.75rem; margin-bottom: 18px; justify-content: center;">Diagnóstico</div>
            <div class="card-body" style="font-size: 1.45rem; line-height: 1.65; text-align: center;">
              O modelo recuperou da memória os dados e regras vistos no pré-treinamento.
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 9: Discussão (Linguagem Humana, Texto Maior e Resumido) -->
      <div class="slide" data-section="DISCUSSÃO">
        <div class="slide-pretitle">O que isso significa?</div>
        <h2 class="slide-title">Discussão</h2>
        <p class="slide-subtitle">Principais aprendizados observados nos testes.</p>

        <div class="grid-3" style="margin-top: 12px;">
          <!-- Ponto 1: Merged -->
          <div class="card card-danger" style="padding: 34px 36px;">
            <div class="card-title" style="color: var(--brown-terracotta); font-size: 1.8rem; margin-bottom: 18px; justify-content: center;">1. Queda no Merged</div>
            <div class="card-body" style="font-size: 1.5rem; line-height: 1.65; text-align: center;">
              Quando juntamos várias mudanças ao mesmo tempo, os modelos se perdem e erram muito mais.
            </div>
          </div>

          <!-- Ponto 2: Consistência -->
          <div class="card card-cognac" style="padding: 34px 36px;">
            <div class="card-title" style="color: var(--brown-cognac); font-size: 1.8rem; margin-bottom: 18px; justify-content: center;">2. Mesma Consistência</div>
            <div class="card-body" style="font-size: 1.5rem; line-height: 1.65; text-align: center;">
              Nas tarefas que acertaram, os dois modelos tiveram taxas de acerto bem parecidas (em rotação, espelhamento e cores).
            </div>
          </div>

          <!-- Ponto 3: Comparando os Modelos -->
          <div class="card card-brown" style="padding: 34px 36px;">
            <div class="card-title" style="color: var(--brown-espresso); font-size: 1.8rem; margin-bottom: 18px;">3. Comparando os Modelos</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.65;">
              • <strong>Gemma 31B:</strong> Acerta mais no geral, mas é bem mais pesado e lento.<br><br>
              • <strong>Gemini Flash:</strong> É super rápido e leve, com resultado parecido nas tarefas simples.
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 10: Conclusão -->
      <div class="slide" data-section="CONCLUSÃO">
        <div class="slide-pretitle">O que entendemos?</div>
        <h2 class="slide-title">Conclusão</h2>

        <div class="grid-2" style="margin-top: 14px;">
          <div class="card card-brown" style="padding: 38px 42px;">
            <div class="card-title" style="color: var(--brown-cognac); font-size: 1.85rem; margin-bottom: 18px; justify-content: center;">Avaliação da Hipótese</div>
            <div class="card-body" style="font-size: 1.55rem; line-height: 1.65; text-align: center;">
              A nossa hipótese inicial de que os modelos teriam AGI e não sofreriam com as transformações estava <strong>incorreta</strong>.
            </div>
          </div>

          <div class="card card-cognac" style="padding: 38px 42px;">
            <div class="card-title" style="color: var(--brown-deep); font-size: 1.85rem; margin-bottom: 18px; justify-content: center;">Em resumo...</div>
            <div class="card-body" style="font-size: 1.55rem; line-height: 1.65; text-align: center;">
              Para ambos os modelos, enquanto mantiveram estabilidade em simetrias isoladas, a acurácia despencou no conjunto Merged, refutando a tese de generalização irrestrita.
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 11: Conclusão: Extensões -->
      <div class="slide" data-section="CONCLUSÃO">
        <div class="slide-pretitle">Como continuar?</div>
        <h2 class="slide-title">Conclusão: Extensões</h2>
        <p class="slide-subtitle">Direções futuras e continuidade da pesquisa.</p>

        <div class="grid-2" style="margin-top: 12px; gap: 26px;">
          <div class="card card-brown" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Análise Cruzada de Falhas</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Comparar erros em tarefas idênticas entre Gemma e Gemini para verificar se convergem para a mesma lógica falha.
            </div>
          </div>

          <div class="card card-cognac" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Taxonomia de Erros</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Classificar individualmente as razões de falha (pequenos desvios, ruídos, perda de cor, regra antiga) buscando padrões estruturados.
            </div>
          </div>

          <div class="card card-terracotta" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Modelos Maiores</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Avaliar modelos de maior escala para checar se a invariância composicional emerge.
            </div>
          </div>

          <div class="card card-success" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Dados Abertos</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Vamos disponibilizar publicamente para a comunidade os datasets criados, códigos e logs obtidos.
            </div>
          </div>
        </div>

        <div style="text-align: center; margin-top: 26px; font-size: 1.15rem; font-weight: 800; color: var(--text-light);">
          UFRGS • Instituto de Informática • Projeto em Ciência e Inovação (PCI)
        </div>
      </div>

    </div>

    <!-- Bottom Footer -->
    <div class="bottom-footer">
      <button class="nav-btn" id="prevBtn" onclick="navSlide(-1)">← Anterior</button>
      <div style="font-size: 1rem; color: var(--text-muted); font-weight: 700;">
        Navegue com as teclas <kbd>←</kbd> <kbd>→</kbd> ou <kbd>Espaço</kbd>
      </div>
      <button class="nav-btn btn-primary" id="nextBtn" onclick="navSlide(1)">Próximo →</button>
    </div>
  </div>
"""
    tail = get_shared_js()
    return head + body + tail


# ==============================================================================
# GERAÇÃO DA APRESENTAÇÃO COMPLETA (COM DETALHAMENTO, ROTEIRO E LINK PARA RESUMIDA)
# ==============================================================================
def generate_completa():
    head = get_shared_head("Benchmark ARC-AGI: Raciocínio vs Memorização (Apresentação Completa)")
    
    body = f"""
  <div class="deck-container">
    <!-- Top Header com Logo UFRGS, Pipeline e Link -->
    <div class="top-header">
      <div class="ufrgs-brand">
        <img src="data:image/png;base64,{b64_logo_ufrgs}" alt="UFRGS" class="ufrgs-logo-img">
      </div>

      <!-- Barra de Seções -->
      <div class="nav-pipeline">
        <button class="nav-pill active" data-sec="INTRODUÇÃO" onclick="goToSection('INTRODUÇÃO')">Introdução</button>
        <button class="nav-pill" data-sec="HIPÓTESE" onclick="goToSection('HIPÓTESE')">Hipótese</button>
        <button class="nav-pill" data-sec="DESENVOLVIMENTO" onclick="goToSection('DESENVOLVIMENTO')">Desenvolvimento</button>
        <button class="nav-pill" data-sec="RESULTADOS" onclick="goToSection('RESULTADOS')">Resultados</button>
        <button class="nav-pill" data-sec="DISCUSSÃO" onclick="goToSection('DISCUSSÃO')">Discussão</button>
        <button class="nav-pill" data-sec="CONCLUSÃO" onclick="goToSection('CONCLUSÃO')">Conclusão</button>
      </div>

      <div class="header-right">
        <a href="apresentacao_slides_benchmark_arc_resumida.html" class="switch-link">⚡ Versão Resumida</a>
        <div class="slide-counter" id="slideCounter">Slide 1 de 11</div>
      </div>
    </div>
    
    <div class="progress-track">
      <div class="progress-fill" id="progressFill"></div>
    </div>

    <!-- Viewport -->
    <div class="slide-viewport">
      <div class="slide active" data-section="INTRODUÇÃO">
        <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; align-items: center; width: 100%;">
          <div>
            <div style="font-size: 2.6rem; font-weight: 800; color: var(--brown-cognac); margin-bottom: 8px;">ARC-AGI:</div>
            <h1 style="font-size: 5.6rem; font-weight: 900; line-height: 1.02; color: var(--brown-deep); margin-bottom: 24px;">
              Raciocínio<br>ou<br>Memorização?
            </h1>

            <div style="margin-bottom: 24px;">
              <div style="background: #F4EFE6; padding: 14px 24px; border-radius: 14px; display: inline-flex; align-items: center; gap: 14px; border: 1px solid var(--border-cream);">
                <span class="badge" style="background: #FFFFFF; color: var(--brown-deep); font-weight: 900; font-size: 1.1rem;">ARC-AGI 💡</span>
                <span style="font-size: 1.2rem; font-weight: 700; color: var(--brown-espresso);">Conjunto de testes para medir o raciocínio abstrato e a capacidade de generalização de inteligências artificiais</span>
              </div>
            </div>

            <div style="display: inline-flex; align-items: center; gap: 14px;">
              <span class="badge badge-gemma" style="font-size: 1.18rem; padding: 10px 22px;">Gemma 4 (31B-IT)</span>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.3rem; background: #F5EDE4; padding: 6px 14px; border-radius: 8px;">VS</span>
              <span class="badge badge-gemini" style="font-size: 1.18rem; padding: 10px 22px;">Gemini 3.5 Flash Lite</span>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 22px;">
            <div class="card card-brown" style="padding: 28px 32px;">
              <div style="font-size: 1.1rem; font-weight: 800; color: var(--brown-cognac); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Discentes Responsáveis</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: var(--brown-deep); line-height: 1.6;">
                • Gabriel Pieruccini Knopp<br>
                • Leonardo Greco Fin<br>
                • Luis Henrique Caselani Macedo Junior
              </div>
            </div>

            <div class="card card-cognac" style="padding: 28px 32px;">
              <div style="font-size: 1.1rem; font-weight: 800; color: var(--brown-terracotta); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Docentes & Orientadores</div>
              <div style="font-size: 1.25rem; font-weight: 700; color: var(--brown-deep); line-height: 1.6;">
                • Prof. André Grahl Pereira<br>
                • Profa. Érika Fernandes Cota<br>
                • Prof. Frederico Messa Schwartzhaupt<br>
                • Prof. João Cesar Netto
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 2: Hipótese (Completa) -->
      <div class="slide" data-section="HIPÓTESE">
        <div class="slide-pretitle" style="font-size: 2.6rem;">O que esperamos?</div>
        <h2 class="slide-title" style="font-size: 5.6rem; margin-bottom: 20px;">Hipótese</h2>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: center; margin-top: 14px;">
          <div>
            <div class="quote-hero" style="font-size: 2.1rem; font-style: italic; text-align: center; line-height: 1.45; padding: 40px 36px; border-left: 12px solid var(--brown-deep);">
              “Os modelos de linguagem possuem AGI e, portanto, não sofrerão mudança na taxa de acurácia para tarefas com transformações que não alteram* a regra original do problema.”
            </div>

            <div class="obs-box" style="margin-top: 20px;">
              <span style="font-size: 1.4rem;">✱</span>
              <span><strong>Observação:</strong> Enquanto as transformações atômicas não alteram a regra original, algumas composições podem adicionar etapas intermediárias tornando a resolução mais complexa (Merged).</span>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 20px;">
            <div class="hypo-box" style="border-left: 10px solid #1E6B37; padding: 26px 30px; font-size: 1.45rem; line-height: 1.45;">
              <div style="color: #1E6B37; font-size: 2rem; font-weight: 900;">▲</div>
              <div>
                <strong>Se possuem Raciocínio Genuíno:</strong><br>Rotacionar, Refletir ou Permutar cores <strong>NÃO altera</strong> o resultado.
              </div>
            </div>

            <div class="hypo-box" style="border-left: 10px solid #9C2617; padding: 26px 30px; font-size: 1.45rem; line-height: 1.45;">
              <div style="color: #9C2617; font-size: 2rem; font-weight: 900;">▲</div>
              <div>
                <strong>Se memorizam resultados públicos:</strong><br>Rotacionar, Refletir ou Permutar cores <strong>PODE alterar</strong> o resultado.
              </div>
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Roteiro do Orador:</strong>
          "Nossa hipótese investiga a invariância isomórfica: se a rede realmente compreendeu o conceito abstrato da matriz, permutar coordenadas ou paletas não deve degradar a acurácia. A quebra de desempenho sob perturbações é um forte indício de dependência da forma canônica memorizada."
        </div>
      </div>

      <!-- SLIDE 3: Metodologia (Completa) -->
      <div class="slide" data-section="DESENVOLVIMENTO">
        <div class="slide-pretitle">Como testamos?</div>
        <h2 class="slide-title">Desenvolvimento: Metodologia</h2>

        <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 36px; margin-top: 14px;">
          <div class="card card-brown" style="padding: 36px 40px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: var(--brown-cognac); margin-bottom: 22px;">
              Divisão em duas chamadas por task
            </div>
            
            <div style="margin-bottom: 26px;">
              <strong style="font-size: 1.65rem; color: var(--brown-deep);">Reasoning (Raciocínio)</strong>
              <ul style="margin-top: 10px; font-size: 1.45rem; padding-left: 28px; line-height: 1.65; color: var(--text-main);">
                <li>Temperatura T = 0.6</li>
                <li>Modo High Thinking</li>
                <li>Exploração profunda de hipóteses e tentativa de resolução</li>
              </ul>
            </div>

            <div>
              <strong style="font-size: 1.65rem; color: var(--brown-deep);">Formatting (Extração)</strong>
              <ul style="margin-top: 10px; font-size: 1.45rem; padding-left: 28px; line-height: 1.65; color: var(--text-main);">
                <li>Temperatura T = 0.0</li>
                <li>Modo Minimal Thinking</li>
                <li>Extração estrita do reasoning e da matriz final</li>
              </ul>
            </div>
          </div>

          <div class="card card-cognac" style="padding: 36px 40px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: var(--brown-terracotta); margin-bottom: 22px;">
              Métricas analisadas
            </div>

            <div style="display: flex; flex-direction: column; gap: 24px;">
              <div>
                <strong style="color: var(--brown-deep); font-size: 1.55rem;">Taxa de acurácia total:</strong>
                <p style="color: var(--text-muted); font-size: 1.4rem; margin-top: 6px; line-height: 1.5;">Verificar consistência entre transformações e modelos.</p>
              </div>
              <div>
                <strong style="color: var(--brown-deep); font-size: 1.55rem;">Tokens gastos por task:</strong>
                <p style="color: var(--text-muted); font-size: 1.4rem; margin-top: 6px; line-height: 1.5;">Analisar dificuldade e esforço computacional.</p>
              </div>
              <div>
                <strong style="color: var(--brown-deep); font-size: 1.55rem;">Tempo gasto por task:</strong>
                <p style="color: var(--text-muted); font-size: 1.4rem; margin-top: 6px; line-height: 1.5;">Observar eficiência na resolução da task.</p>
              </div>
            </div>

            <div class="obs-box" style="margin-top: 20px; font-size: 1.12rem;">
              <span>✱ 1. Para a resolução do modelo (não representa a dificuldade humana). 2. Sob ótica geral devido a fatores externos de hardware/rede.</span>
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Roteiro do Orador:</strong>
          "Utilizamos a separação em duas etapas para garantir que o pensamento livre do modelo não seja interrompido por restrições de formatação JSON, e depois extraímos deterministamente a matriz predita a temperatura zero."
        </div>
      </div>

      <!-- SLIDE 4: Transformações (Completa) -->
      <div class="slide" data-section="DESENVOLVIMENTO">
        <div class="slide-pretitle">Como geramos?</div>
        <h2 class="slide-title">Desenvolvimento: Transformações</h2>
        <p class="slide-subtitle">Derivadas exclusivamente das tarefas acertadas previamente por cada modelo.</p>

        <div class="grid-4" style="margin-top: 10px;">
          <div class="card card-brown" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🔄 Rotação</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c1"></div><div class="m-cell c1"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 600; color: var(--text-muted); text-align: center;">90° CW, 180°, 90° CCW<br><strong>Input == Output</strong></p>
          </div>

          <div class="card card-cognac" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🪞 Reflexão</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c3"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c3"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c3"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 600; color: var(--text-muted); text-align: center;">Espelhamento Axial<br><strong>Input == Output</strong></p>
          </div>

          <div class="card card-terracotta" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🎨 Coloração</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c1"></div>
                <div class="m-cell c0"></div><div class="m-cell c1"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-cognac); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
                <div class="m-cell c8"></div><div class="m-cell c3"></div><div class="m-cell c8"></div>
                <div class="m-cell c4"></div><div class="m-cell c8"></div><div class="m-cell c4"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 600; color: var(--text-muted); text-align: center;">Permutação (Cor 0 fixa)<br><strong>Input == Output</strong></p>
          </div>

          <div class="card card-danger" style="text-align: center; padding: 26px 20px;">
            <div class="card-title" style="justify-content: center; font-size: 1.55rem;">🌪️ Merged</div>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 18px 0;">
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c1"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c1"></div><div class="m-cell c2"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
              </div>
              <span style="font-weight: 900; color: var(--brown-terracotta); font-size: 1.5rem;">➔</span>
              <div class="matrix-box" style="grid-template-columns: repeat(3, 20px);">
                <div class="m-cell c0"></div><div class="m-cell c0"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c3"></div><div class="m-cell c0"></div>
                <div class="m-cell c0"></div><div class="m-cell c8"></div><div class="m-cell c8"></div>
              </div>
            </div>
            <p style="font-size: 1.2rem; font-weight: 600; color: var(--brown-terracotta); text-align: center;">Rotação + Reflexão + Cores<br><strong>Composição Livre</strong></p>
          </div>
        </div>
      </div>

      <!-- SLIDE 5: Acurácia (Completa) -->
      <div class="slide" data-section="RESULTADOS">
        <div class="slide-pretitle">O que obtivemos?</div>
        <h2 class="slide-title">Resultados: Acurácia</h2>
        <p class="slide-subtitle">Comparação: Gemma vs Gemini</p>

        <div class="table-wrapper">
          <table class="data-table" style="font-size: 1.22rem;">
            <thead>
              <tr>
                <th>Dataset</th>
                <th>Acurácia Gemma (31B)</th>
                <th>Acurácia Gemini (Flash Lite)</th>
                <th>Diferença</th>
                <th>Comportamento Observado</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Original (Treino)</strong></td>
                <td><span class="badge badge-gemma">76.00%</span> (304/400)</td>
                <td><span class="badge badge-gemini">67.50%</span> (270/400)</td>
                <td><strong>+8.50 pp</strong></td>
                <td>Gemma aparenta ter maior retenção no dataset público</td>
              </tr>
              <tr>
                <td><strong>Rotated</strong></td>
                <td><span class="badge badge-success">87.17%</span> (265/304)</td>
                <td><span class="badge badge-success">85.56%</span> (231/270)</td>
                <td><strong>+1.62 pp</strong></td>
                <td>Alta estabilidade sob rotação</td>
              </tr>
              <tr>
                <td><strong>Reflected</strong></td>
                <td><span class="badge badge-success">87.50%</span> (266/304)</td>
                <td><span class="badge badge-success">87.04%</span> (235/270)</td>
                <td><strong>+0.46 pp</strong></td>
                <td>Desempenho quase equivalente em reflexão</td>
              </tr>
              <tr>
                <td><strong>Coloration</strong></td>
                <td><span class="badge badge-success">89.14%</span> (271/304)</td>
                <td><span class="badge badge-success">84.44%</span> (228/270)</td>
                <td><strong>+4.70 pp</strong></td>
                <td>Gemma ligeiramente superior em cores</td>
              </tr>
              <tr class="highlight">
                <td><strong>Merged</strong></td>
                <td><span class="badge badge-danger">44.50%</span> (263/591)</td>
                <td><span class="badge badge-danger">35.93%</span> (194/540)</td>
                <td><strong>+8.57 pp</strong></td>
                <td><strong>Queda acentuada (-43 a -50 pp) em ambos</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- SLIDE 6: Gráficos (Completa) -->
      <div class="slide" data-section="RESULTADOS">
        <div class="slide-pretitle">O que podemos ver?</div>
        <h2 class="slide-title">Resultados: Gráficos</h2>

        <div class="chart-tabs">
          <button class="chart-tab-btn active" onclick="switchChartTab('geral', 'Visão Geral 3-em-1 (Acurácia, Tokens e Tempo)', this)">Visão Geral 3-em-1</button>
          <button class="chart-tab-btn" onclick="switchChartTab('acuracia', 'Comparativo de Acurácia (%) por Dataset', this)">Taxa de Acurácia (%)</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tokens', 'Tokens Médios de Pensamento em Tarefas Corretas', this)">Tokens de Pensamento</button>
          <button class="chart-tab-btn" onclick="switchChartTab('tempo', 'Tempo Médio de Execução por Tarefa (s)', this)">Tempo de Inferência (s)</button>
        </div>

        <div class="chart-display-frame">
          <img id="mainChartImg" src="data:image/png;base64,{b64_geral}" alt="Gráfico Comparativo ARC-AGI" style="max-width: 100%; max-height: 480px; object-fit: contain; border-radius: 8px;">
          <p id="chartDesc" style="margin-top: 10px; font-size: 1.18rem; font-weight: 800; color: var(--brown-deep);">
            Visão Geral 3-em-1 (Acurácia, Tokens e Tempo)
          </p>
        </div>
      </div>

      <!-- SLIDE 7: Estatísticas (Completa) -->
      <div class="slide" data-section="RESULTADOS">
        <div class="slide-pretitle">Como estão distribuídos?</div>
        <h2 class="slide-title">Resultados: Estatísticas</h2>
        <p class="slide-subtitle">Métricas calculadas exclusivamente sobre as tarefas resolvidas com sucesso.</p>

        {get_dispersion_tables_html()}
      </div>

      <!-- SLIDE 8: Discussão: Exemplo (Completa) -->
      <div class="slide" data-section="DISCUSSÃO">
        <div class="slide-pretitle">Como erraram?</div>
        <h2 class="slide-title">Discussão: Exemplo</h2>
        <p class="slide-subtitle">Task f1cefba8 (Merged) — Alucinação da regra original da base pública.</p>

        <div class="grid-2" style="margin-top: 14px;">
          <div class="card card-danger" style="padding: 34px 38px;">
            <div class="card-title" style="font-size: 1.75rem; margin-bottom: 18px;">
              <span>Evidência no Reasoning</span>
              <span class="badge badge-gemma">Gemma 4 (31B)</span>
            </div>
            <div class="card-body">
              <p style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; background: #FDEEEB; padding: 18px; border-radius: 10px; color: #9C2617; border: 1px solid #F3C9C3; font-weight: 700;">
                "...following the cycle 2 -> 3 -> 8 -> 2..."
              </p>
              <p style="margin-top: 18px; font-size: 1.45rem; line-height: 1.65; text-align: center;">
                Essa regra existia na base pública original, mas havia sido <strong>removida no JSON transformado</strong>.
              </p>
            </div>
          </div>

          <div class="card card-brown" style="padding: 34px 38px; display: flex; flex-direction: column; justify-content: center;">
            <div class="card-title" style="font-size: 1.75rem; margin-bottom: 18px; justify-content: center;">Diagnóstico</div>
            <div class="card-body" style="font-size: 1.45rem; line-height: 1.65; text-align: center;">
              O modelo recuperou da memória os dados vistos no pré-treinamento e possuiu preferência pela resposta antiga sob a nova, sem considerar os novos exemplos.
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Roteiro do Orador:</strong>
          "Este é o exemplo mais marcante de alucinação por contaminação: o modelo cita explicitamente uma sequência de cores que existia na tarefa original pública de 2019, mesmo ela tendo sido completamente removida da matriz apresentada no prompt."
        </div>
      </div>

      <!-- SLIDE 9: Discussão (Completa) -->
      <div class="slide" data-section="DISCUSSÃO">
        <div class="slide-pretitle">O que isso significa?</div>
        <h2 class="slide-title">Discussão</h2>
        <p class="slide-subtitle">Principais aprendizados observados nos testes.</p>

        <div class="grid-3" style="margin-top: 12px;">
          <!-- Ponto 1: Merged -->
          <div class="card card-danger" style="padding: 34px 36px;">
            <div class="card-title" style="color: var(--brown-terracotta); font-size: 1.8rem; margin-bottom: 18px; justify-content: center;">1. Queda no Merged</div>
            <div class="card-body" style="font-size: 1.5rem; line-height: 1.65; text-align: center;">
              Quando combinamos múltiplas transformações simultâneas, os modelos sofrem uma queda drástica na acurácia, indicando sobrecarga na inferência.
            </div>
          </div>

          <!-- Ponto 2: Consistência -->
          <div class="card card-cognac" style="padding: 34px 36px;">
            <div class="card-title" style="color: var(--brown-cognac); font-size: 1.8rem; margin-bottom: 18px; justify-content: center;">2. Mesma Consistência</div>
            <div class="card-body" style="font-size: 1.5rem; line-height: 1.65; text-align: center;">
              Entre as tarefas que acertaram, ambos os modelos mantiveram taxas de consistência muito semelhantes em rotações, reflexões e trocas de cores.
            </div>
          </div>

          <!-- Ponto 3: Comparando os Modelos -->
          <div class="card card-brown" style="padding: 34px 36px;">
            <div class="card-title" style="color: var(--brown-espresso); font-size: 1.8rem; margin-bottom: 18px;">3. Comparando os Modelos</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.65;">
              • <strong>Gemma 4 (31B):</strong> Maior retenção e acurácia absoluta, mas é bem mais pesado e lento.<br><br>
              • <strong>Gemini 3.5 Flash Lite:</strong> Alta velocidade e eficiência com desempenho parecido nas tarefas simples.
            </div>
          </div>
        </div>

        <div class="speaker-script">
          <strong>Roteiro do Orador:</strong>
          "Os dados mostram que os modelos possuem heurísticas funcionais para transformações simples, mas sofrem de limitações como leitura linear e sofrem forte degradação quando múltiplos operadores são combinados."
        </div>
      </div>

      <!-- SLIDE 10: Conclusão (Completa) -->
      <div class="slide" data-section="CONCLUSÃO">
        <div class="slide-pretitle">O que entendemos?</div>
        <h2 class="slide-title">Conclusão</h2>

        <div class="grid-2" style="margin-top: 14px;">
          <div class="card card-brown" style="padding: 38px 42px;">
            <div class="card-title" style="color: var(--brown-cognac); font-size: 1.85rem; margin-bottom: 18px; justify-content: center;">Avaliação da Hipótese</div>
            <div class="card-body" style="font-size: 1.55rem; line-height: 1.65; text-align: center;">
              A nossa hipótese inicial de que os modelos de linguagem teriam AGI plena e não sofreriam impacto nas transformações estava <strong>incorreta</strong>.
            </div>
          </div>

          <div class="card card-cognac" style="padding: 38px 42px;">
            <div class="card-title" style="color: var(--brown-deep); font-size: 1.85rem; margin-bottom: 18px; justify-content: center;">Em resumo...</div>
            <div class="card-body" style="font-size: 1.55rem; line-height: 1.65; text-align: center;">
              Para ambos os modelos, enquanto mantiveram estabilidade em simetrias isoladas, a acurácia despencou no conjunto Merged, refutando a tese de generalização irrestrita.
            </div>
          </div>
        </div>
      </div>

      <!-- SLIDE 11: Conclusão: Extensões (Completa) -->
      <div class="slide" data-section="CONCLUSÃO">
        <div class="slide-pretitle">Como continuar?</div>
        <h2 class="slide-title">Conclusão: Extensões</h2>
        <p class="slide-subtitle">Direções futuras e continuidade da pesquisa.</p>

        <div class="grid-2" style="margin-top: 12px; gap: 26px;">
          <div class="card card-brown" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Análise Cruzada de Falhas</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Comparar erros em tarefas idênticas entre Gemma e Gemini para verificar se convergem para a mesma lógica falha.
            </div>
          </div>

          <div class="card card-cognac" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Taxonomia de Erros</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Classificar individualmente as razões de falha (pequenos desvios, ruídos, perda de cor, regra antiga) buscando padrões estruturados.
            </div>
          </div>

          <div class="card card-terracotta" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Modelos Maiores</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Avaliar modelos de maior escala para checar se a invariância composicional emerge.
            </div>
          </div>

          <div class="card card-success" style="padding: 32px 36px;">
            <div class="card-title" style="font-size: 1.7rem; margin-bottom: 14px; justify-content: center;">Dados Abertos</div>
            <div class="card-body" style="font-size: 1.42rem; line-height: 1.6; text-align: center;">
              Vamos disponibilizar publicamente para a comunidade os datasets criados, códigos e logs obtidos.
            </div>
          </div>
        </div>

        <div style="text-align: center; margin-top: 26px; font-size: 1.15rem; font-weight: 800; color: var(--text-light);">
          UFRGS • Instituto de Informática • Projeto em Ciência e Inovação (PCI)
        </div>
      </div>

    </div>

    <!-- Bottom Footer -->
    <div class="bottom-footer">
      <button class="nav-btn" id="prevBtn" onclick="navSlide(-1)">← Anterior</button>
      <div style="font-size: 1rem; color: var(--text-muted); font-weight: 700;">
        Navegue com as teclas <kbd>←</kbd> <kbd>→</kbd> ou <kbd>Espaço</kbd>
      </div>
      <button class="nav-btn btn-primary" id="nextBtn" onclick="navSlide(1)">Próximo →</button>
    </div>
  </div>
"""
    tail = get_shared_js()
    return head + body + tail


def main():
    print("Gerando apresentação resumida...")
    resumida_html = generate_resumida()
    with open('Results/apresentacao_slides_benchmark_arc_resumida.html', 'w', encoding='utf-8') as f:
        f.write(resumida_html)
    print("Apresentação resumida salva em Results/apresentacao_slides_benchmark_arc_resumida.html")

    print("Gerando apresentação completa...")
    completa_html = generate_completa()
    with open('Results/apresentacao_slides_benchmark_arc_completa.html', 'w', encoding='utf-8') as f:
        f.write(completa_html)
    print("Apresentação completa salva em Results/apresentacao_slides_benchmark_arc_completa.html")

if __name__ == '__main__':
    main()
