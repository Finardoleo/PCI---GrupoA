import random
from typing import List, Dict, Tuple, Callable

# Tipos para representação de grid
Grid = List[List[int]]

def copy_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]

# --- 1. IDENTIDADE ---
def identity(grid: Grid, **kwargs) -> Grid:
    return copy_grid(grid)

# --- 2. ROTAÇÕES ---
def rotate_90_cw(grid: Grid, **kwargs) -> Grid:
    """Rotaciona o grid 90 graus no sentido horário (para a direita)."""
    if not grid or not grid[0]:
        return grid
    H = len(grid)
    W = len(grid[0])
    return [[grid[H - 1 - r][c] for r in range(H)] for c in range(W)]

def rotate_90_ccw(grid: Grid, **kwargs) -> Grid:
    """Rotaciona o grid 90 graus no sentido anti-horário (para a esquerda)."""
    if not grid or not grid[0]:
        return grid
    H = len(grid)
    W = len(grid[0])
    return [[grid[r][W - 1 - c] for r in range(H)] for c in range(W)]

def rotate_180(grid: Grid, **kwargs) -> Grid:
    """Rotaciona o grid 180 graus."""
    if not grid or not grid[0]:
        return grid
    return [row[::-1] for row in grid[::-1]]

# --- 3. REFLEXÕES ---
def reflect_horizontal(grid: Grid, **kwargs) -> Grid:
    """Espelhamento horizontal (inverte a ordem das colunas, eixo vertical)."""
    if not grid or not grid[0]:
        return grid
    return [row[::-1] for row in grid]

def reflect_vertical(grid: Grid, **kwargs) -> Grid:
    """Espelhamento vertical (inverte a ordem das linhas, eixo horizontal)."""
    if not grid or not grid[0]:
        return grid
    return [row[:] for row in grid[::-1]]

# --- 4. COLORAÇÃO (MUDANÇA DE CORES) ---
def color_permute(grid: Grid, color_map: Dict[int, int] = None, **kwargs) -> Grid:
    """Substitui os números/cores do grid conforme o mapeamento fornecido."""
    if not grid or not color_map:
        return copy_grid(grid)
    return [[color_map.get(val, val) for val in row] for row in grid]

# --- TABELA DE TRANSFORMAÇÕES ATÔMICAS ---
ROTATION_TRANSFORMS = [
    ("rotate_90_cw", "Rotation", rotate_90_cw),
    ("rotate_90_ccw", "Rotation", rotate_90_ccw),
    ("rotate_180", "Rotation", rotate_180)
]

REFLECTION_TRANSFORMS = [
    ("reflect_horizontal", "Reflexion", reflect_horizontal),
    ("reflect_vertical", "Reflexion", reflect_vertical)
]

COLORATION_TRANSFORMS = [
    ("color_permute", "Coloration", color_permute)
]

IDENTITY_TRANSFORM = ("identity", "Identity", identity)

def generate_color_mapping(task_data: dict, include_zero: bool = True) -> Dict[int, int]:
    """
    Gera um mapeamento de permutação aleatório e não-trivial para as cores presentes na task.
    Se include_zero for True, a cor 0 (background) também pode ser permutada juntamente com as cores 1-9.
    """
    colors_present = set()
    for split in ["train", "test"]:
        for pair in task_data.get(split, []):
            for grid_key in ["input", "output"]:
                grid = pair.get(grid_key, [])
                for row in grid:
                    for val in row:
                        if isinstance(val, int) and (val >= 0 if include_zero else val > 0):
                            colors_present.add(val)
                            
    active_colors = sorted(list(colors_present))
    if not active_colors:
        return {}
        
    # Se há apenas 1 cor, escolhe outra cor aleatória de 0 a 9 diferente dela
    if len(active_colors) == 1:
        c = active_colors[0]
        possible = [x for x in range(0 if include_zero else 1, 10) if x != c]
        new_c = random.choice(possible)
        return {c: new_c}
        
    # Se há 2 ou mais cores, faz um desarranjo/permutação para que as cores mudem
    shuffled = active_colors[:]
    for _ in range(50):
        random.shuffle(shuffled)
        if any(a != b for a, b in zip(active_colors, shuffled)):
            break
            
    return {orig: new_c for orig, new_c in zip(active_colors, shuffled)}

def format_color_map_description(mapping: Dict[int, int]) -> str:
    if not mapping:
        return "color_permute(none)"
    swaps = [f"{k}->{v}" for k, v in sorted(mapping.items()) if k != v]
    return f"color_permute({','.join(swaps)})"

def get_atomic_transformation(transform_choice: str) -> Tuple[str, str, Callable]:
    """
    Retorna uma tupla (nome_especifico, familia, funcao) a partir de uma escolha.
    Opções: 'identity', 'rotation', 'reflection', 'coloration', 'random'.
    """
    choice = transform_choice.strip().lower()
    
    if choice in ["identity", "identidade", "none"]:
        return IDENTITY_TRANSFORM
    elif choice in ["rotation", "rotacao", "rotação"]:
        return random.choice(ROTATION_TRANSFORMS)
    elif choice in ["reflection", "reflexion", "reflexao", "reflexão"]:
        return random.choice(REFLECTION_TRANSFORMS)
    elif choice in ["coloration", "coloracao", "coloração", "colors"]:
        return COLORATION_TRANSFORMS[0]
    elif choice == "random":
        # Sorteia entre as 3 transformações ativas
        pool = ROTATION_TRANSFORMS + REFLECTION_TRANSFORMS + COLORATION_TRANSFORMS
        return random.choice(pool)
    else:
        # Tenta match por nome exato
        all_transforms = [IDENTITY_TRANSFORM] + ROTATION_TRANSFORMS + REFLECTION_TRANSFORMS + COLORATION_TRANSFORMS
        for name, fam, func in all_transforms:
            if choice == name.lower():
                return name, fam, func
        # Fallback para random
        return random.choice(ROTATION_TRANSFORMS + REFLECTION_TRANSFORMS + COLORATION_TRANSFORMS)

def build_composed_transformation(transform_choice: str) -> Tuple[str, List[str], Callable]:
    """
    Monta a transformação (simples ou merged).
    Retorna (descricao_str, lista_de_familias, funcao_composta).
    """
    choice = transform_choice.strip().lower()
    
    if choice in ["merged", "merge"]:
        # Escolhe 2 transformações não-identidade de famílias distintas (Rotação, Reflexão, Coloração)
        families_pool = [
            ("Rotation", ROTATION_TRANSFORMS),
            ("Reflexion", REFLECTION_TRANSFORMS),
            ("Coloration", COLORATION_TRANSFORMS)
        ]
        fam_sample = random.sample(families_pool, 2)
        _, pool1 = fam_sample[0]
        _, pool2 = fam_sample[1]
        
        name1, fam1, func1 = random.choice(pool1)
        name2, fam2, func2 = random.choice(pool2)
        
        families = [fam1, fam2]
        desc = f"{name1}+{name2}"
        
        def composed_func(grid: Grid, color_map: Dict[int, int] = None) -> Grid:
            g1 = func1(grid, color_map=color_map)
            g2 = func2(g1, color_map=color_map)
            return g2
            
        return desc, families, composed_func
    else:
        name, fam, func = get_atomic_transformation(choice)
        return name, [fam], func
