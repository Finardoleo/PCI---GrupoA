import os, glob, re
import pandas as pd
import numpy as np

def clean_df(csv_path):
    df = pd.read_csv(csv_path)
    summary_tasks = {'Batch Accuracy', 'Tempo do Batch', 'Tokens do Batch', 'Total', 'Accuracy'}
    return df[~df['Task'].astype(str).str.strip().isin(summary_tasks)].copy()

def parse_tok(s):
    if pd.isna(s): return 0
    m = re.search(r'Total:\s*(\d+)', str(s))
    if m: return int(m.group(1))
    try: return int(float(str(s).strip()))
    except: return 0

def parse_time(s):
    if pd.isna(s): return 0.0
    m = re.search(r'Total:\s*([\d\.]+)s?', str(s))
    if m: return float(m.group(1))
    try: return float(str(s).replace('s','').strip())
    except: return 0.0

def load_model_data(model_dir, map_folder):
    meta_df = pd.read_csv(f'New Tasks/{map_folder}/transformed_tasks.csv')
    meta_map = {}
    for _, row in meta_df.iterrows():
        tid = str(row['New_Task_ID']).strip().replace('.json', '')
        orig = str(row['Original_Task']).strip().replace('.json', '')
        meta_map[tid] = orig
        
    ds_data = {}
    datasets = [
        ('Training Data Set', 'Original (Treino)'),
        ('Rotated Training Data Set', 'Rotated'),
        ('Reflected Training Data Set', 'Reflected'),
        ('Coloration Training Data Set', 'Coloration'),
        ('Merged Training Data Set', 'Merged')
    ]
    for ds_folder, ds_name in datasets:
        acc_p = glob.glob(f'{model_dir}/{ds_folder}/*_accuracy.csv')[0]
        tok_p = glob.glob(f'{model_dir}/{ds_folder}/*_tokens.csv')[0]
        tim_p = glob.glob(f'{model_dir}/{ds_folder}/*_times.csv')[0]
        
        acc_df = clean_df(acc_p)
        tok_df = clean_df(tok_p)
        tim_df = clean_df(tim_p)
        
        col = acc_df.columns[1]
        m = pd.merge(acc_df[['Task', col]], tok_df[['Task', col]], on='Task', suffixes=('_acc', '_tok'))
        m = pd.merge(m, tim_df[['Task', col]], on='Task')
        m.rename(columns={f'{col}_acc': 'status', f'{col}_tok': 'tok_str', col: 'time_str'}, inplace=True)
        m['task_clean'] = m['Task'].astype(str).str.strip().str.replace('.json', '')
        m['tokens'] = m['tok_str'].apply(parse_tok)
        m['time_s'] = m['time_str'].apply(parse_time)
        m['is_correct'] = m['status'].astype(str).str.strip() == 'CORRECT'
        
        if ds_folder == 'Training Data Set':
            m['orig_task'] = m['task_clean']
        else:
            m['orig_task'] = m['task_clean'].apply(lambda x: meta_map.get(x, x))
            
        ds_data[ds_folder] = m
    return ds_data

gemma_data = load_model_data('Results/Gemma', 'Gemma')
gemini_data = load_model_data('Results/Gemini_3.5_Flash_Lite', 'Gemini')

datasets = [
    ('Training Data Set', 'Original (Treino)'),
    ('Rotated Training Data Set', 'Rotated'),
    ('Reflected Training Data Set', 'Reflected'),
    ('Coloration Training Data Set', 'Coloration'),
    ('Merged Training Data Set', 'Merged')
]

# Shared 252 base tasks (solved by both in training)
gemma_train_corr = set(gemma_data['Training Data Set'][gemma_data['Training Data Set']['is_correct']]['orig_task'])
gemini_train_corr = set(gemini_data['Training Data Set'][gemini_data['Training Data Set']['is_correct']]['orig_task'])
shared_base_252 = gemma_train_corr.intersection(gemini_train_corr)

print(f"Base tasks in common (solved by both in training baseline): {len(shared_base_252)}")

summary_rows = []

for ds_folder, ds_name in datasets:
    gm_all = gemma_data[ds_folder]
    gn_all = gemini_data[ds_folder]
    
    gm_sub = gm_all[gm_all['orig_task'].isin(shared_base_252)].copy()
    gn_sub = gn_all[gn_all['orig_task'].isin(shared_base_252)].copy()
    
    gm_corr = gm_sub[gm_sub['is_correct']]
    gn_corr = gn_sub[gn_sub['is_correct']]
    
    gm_tot = len(gm_sub)
    gm_c = len(gm_corr)
    gm_acc = (gm_c / gm_tot * 100) if gm_tot else 0
    gm_tok_m = gm_corr['tokens'].mean()
    gm_tok_s = gm_corr['tokens'].std()
    gm_tok_min = gm_corr['tokens'].min()
    gm_tok_max = gm_corr['tokens'].max()
    gm_tim_m = gm_corr['time_s'].mean()
    gm_tim_s = gm_corr['time_s'].std()
    gm_tim_min = gm_corr['time_s'].min()
    gm_tim_max = gm_corr['time_s'].max()
    
    gn_tot = len(gn_sub)
    gn_c = len(gn_corr)
    gn_acc = (gn_c / gn_tot * 100) if gn_tot else 0
    gn_tok_m = gn_corr['tokens'].mean()
    gn_tok_s = gn_corr['tokens'].std()
    gn_tok_min = gn_corr['tokens'].min()
    gn_tok_max = gn_corr['tokens'].max()
    gn_tim_m = gn_corr['time_s'].mean()
    gn_tim_s = gn_corr['time_s'].std()
    gn_tim_min = gn_corr['time_s'].min()
    gn_tim_max = gn_corr['time_s'].max()
    
    delta_acc = gm_acc - gn_acc
    delta_tok = gm_tok_m - gn_tok_m
    speedup = gm_tim_m / gn_tim_m if gn_tim_m else 0
    
    summary_rows.append({
        'dataset': ds_name,
        'gemma_tot': gm_tot,
        'gemma_c': gm_c,
        'gemma_acc': gm_acc,
        'gemma_tok_mean': gm_tok_m,
        'gemma_tok_std': gm_tok_s,
        'gemma_tok_min': gm_tok_min,
        'gemma_tok_max': gm_tok_max,
        'gemma_tim_mean': gm_tim_m,
        'gemma_tim_std': gm_tim_s,
        'gemma_tim_min': gm_tim_min,
        'gemma_tim_max': gm_tim_max,
        'gemini_tot': gn_tot,
        'gemini_c': gn_c,
        'gemini_acc': gn_acc,
        'gemini_tok_mean': gn_tok_m,
        'gemini_tok_std': gn_tok_s,
        'gemini_tok_min': gn_tok_min,
        'gemini_tok_max': gn_tok_max,
        'gemini_tim_mean': gn_tim_m,
        'gemini_tim_std': gn_tim_s,
        'gemini_tim_min': gn_tim_min,
        'gemini_tim_max': gn_tim_max,
        'delta_acc': delta_acc,
        'delta_tok': delta_tok,
        'speedup': speedup
    })

df_res = pd.DataFrame(summary_rows)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 1000)
print(df_res)
