import glob, re, os
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

def load_data(model_dir, map_folder):
    meta_df = pd.read_csv(f'New Tasks/{map_folder}/transformed_tasks.csv')
    meta_map = {}
    for _, row in meta_df.iterrows():
        tid = str(row['New_Task_ID']).strip().replace('.json', '')
        orig = str(row['Original_Task']).strip().replace('.json', '')
        meta_map[tid] = orig
        
    ds_data = {}
    datasets = [
        'Training Data Set',
        'Rotated Training Data Set',
        'Reflected Training Data Set',
        'Coloration Training Data Set',
        'Merged Training Data Set'
    ]
    for ds in datasets:
        acc_p = glob.glob(f'{model_dir}/{ds}/*_accuracy.csv')[0]
        tok_p = glob.glob(f'{model_dir}/{ds}/*_tokens.csv')[0]
        tim_p = glob.glob(f'{model_dir}/{ds}/*_times.csv')[0]
        
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
        
        if ds == 'Training Data Set':
            m['orig_task'] = m['task_clean']
        else:
            m['orig_task'] = m['task_clean'].apply(lambda x: meta_map.get(x, x))
            
        ds_data[ds] = m
    return ds_data

gemma_data = load_data('Results/Gemma', 'Gemma')
gemini_data = load_data('Results/Gemini_3.5_Flash_Lite', 'Gemini')

# Determine the 252 shared base tasks
gemma_train_corr = set(gemma_data['Training Data Set'][gemma_data['Training Data Set']['is_correct']]['orig_task'])
gemini_train_corr = set(gemini_data['Training Data Set'][gemini_data['Training Data Set']['is_correct']]['orig_task'])
shared_base_252 = gemma_train_corr.intersection(gemini_train_corr)

print(f"Total base tasks solved by both in Training (shared base): {len(shared_base_252)}")

print("\n" + "="*80)
print("METRICS ON THE SHARED BASE TASKS (N=252 shared original tasks)")
print("="*80)

datasets = [
    ('Training Data Set', 'Original (Treino)'),
    ('Rotated Training Data Set', 'Rotated'),
    ('Reflected Training Data Set', 'Reflected'),
    ('Coloration Training Data Set', 'Coloration'),
    ('Merged Training Data Set', 'Merged')
]

for ds_folder, ds_name in datasets:
    gm_all = gemma_data[ds_folder]
    gn_all = gemini_data[ds_folder]
    
    # Filter strictly to the shared_base_252
    gm_sub = gm_all[gm_all['orig_task'].isin(shared_base_252)].copy()
    gn_sub = gn_all[gn_all['orig_task'].isin(shared_base_252)].copy()
    
    gm_corr = gm_sub[gm_sub['is_correct']]
    gn_corr = gn_sub[gn_sub['is_correct']]
    
    print(f"\n[{ds_name}] (Filtered to shared 252 base tasks)")
    print(f"  Gemma:")
    print(f"    Total Evaluated: {len(gm_sub)}, Correct: {len(gm_corr)} ({len(gm_corr)/len(gm_sub)*100:.2f}%)")
    print(f"    Tokens (Correct): Mean = {gm_corr['tokens'].mean():.1f} ± {gm_corr['tokens'].std():.1f} | Min = {gm_corr['tokens'].min()} | Max = {gm_corr['tokens'].max()} | Total = {gm_corr['tokens'].sum():,}")
    print(f"    Time (Correct)  : Mean = {gm_corr['time_s'].mean():.1f}s ± {gm_corr['time_s'].std():.1f}s | Min = {gm_corr['time_s'].min():.1f}s | Max = {gm_corr['time_s'].max():.1f}s | Total = {gm_corr['time_s'].sum():.1f}s")
    
    print(f"  Gemini:")
    print(f"    Total Evaluated: {len(gn_sub)}, Correct: {len(gn_corr)} ({len(gn_corr)/len(gn_sub)*100:.2f}%)")
    print(f"    Tokens (Correct): Mean = {gn_corr['tokens'].mean():.1f} ± {gn_corr['tokens'].std():.1f} | Min = {gn_corr['tokens'].min()} | Max = {gn_corr['tokens'].max()} | Total = {gn_corr['tokens'].sum():,}")
    print(f"    Time (Correct)  : Mean = {gn_corr['time_s'].mean():.1f}s ± {gn_corr['time_s'].std():.1f}s | Min = {gn_corr['time_s'].min():.1f}s | Max = {gn_corr['time_s'].max():.1f}s | Total = {gn_corr['time_s'].sum():.1f}s")
    
    # Speedup and Token Delta
    tok_diff = gm_corr['tokens'].mean() - gn_corr['tokens'].mean()
    speedup = gm_corr['time_s'].mean() / gn_corr['time_s'].mean() if gn_corr['time_s'].mean() > 0 else 0
    acc_diff = (len(gm_corr)/len(gm_sub)*100) - (len(gn_corr)/len(gn_sub)*100)
    print(f"  Comparison:")
    print(f"    Token Delta (Gemma - Gemini): {tok_diff:+.1f} tokens")
    print(f"    Speedup (Gemma / Gemini): {speedup:.1f}x")
    print(f"    Accuracy Diff: {acc_diff:+.2f} pp")
