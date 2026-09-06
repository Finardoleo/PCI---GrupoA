import os, sys, glob, re
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

gemma_data = load_data('Results/Gemma', 'Gemma')
gemini_data = load_data('Results/Gemini_3.5_Flash_Lite', 'Gemini')

datasets = [
    ('Training Data Set', 'Original (Treino)'),
    ('Rotated Training Data Set', 'Rotated'),
    ('Reflected Training Data Set', 'Reflected'),
    ('Coloration Training Data Set', 'Coloration'),
    ('Merged Training Data Set', 'Merged')
]

gemma_train_corr = set(gemma_data['Training Data Set'][gemma_data['Training Data Set']['is_correct']]['orig_task'])
gemini_train_corr = set(gemini_data['Training Data Set'][gemini_data['Training Data Set']['is_correct']]['orig_task'])
shared_base_252 = gemma_train_corr.intersection(gemini_train_corr)

print("="*90)
print("INTERPRETATION 1: Filtered to Shared 252 Base Tasks (Correct in each model)")
print("="*90)
for ds_folder, ds_name in datasets:
    gm = gemma_data[ds_folder]
    gn = gemini_data[ds_folder]
    
    gm_sub = gm[gm['orig_task'].isin(shared_base_252)]
    gn_sub = gn[gn['orig_task'].isin(shared_base_252)]
    
    gm_corr = gm_sub[gm_sub['is_correct']]
    gn_corr = gn_sub[gn_sub['is_correct']]
    
    t_diff = gm_corr['tokens'].mean() - gn_corr['tokens'].mean()
    spd = gm_corr['time_s'].mean() / gn_corr['time_s'].mean()
    acc_diff = (len(gm_corr)/len(gm_sub)*100) - (len(gn_corr)/len(gn_sub)*100)
    
    print(f"\n[{ds_name}] (Base: 252 shared original tasks)")
    print(f"  Gemma : {len(gm_corr)}/{len(gm_sub)} ({len(gm_corr)/len(gm_sub)*100:.2f}%) | Tok: {gm_corr['tokens'].mean():.1f} ± {gm_corr['tokens'].std():.1f} [{gm_corr['tokens'].min()} - {gm_corr['tokens'].max()}] | Time: {gm_corr['time_s'].mean():.1f}s ± {gm_corr['time_s'].std():.1f}s [{gm_corr['time_s'].min():.1f}s - {gm_corr['time_s'].max():.1f}s]")
    print(f"  Gemini: {len(gn_corr)}/{len(gn_sub)} ({len(gn_corr)/len(gn_sub)*100:.2f}%) | Tok: {gn_corr['tokens'].mean():.1f} ± {gn_corr['tokens'].std():.1f} [{gn_corr['tokens'].min()} - {gn_corr['tokens'].max()}] | Time: {gn_corr['time_s'].mean():.1f}s ± {gn_corr['time_s'].std():.1f}s [{gn_corr['time_s'].min():.1f}s - {gn_corr['time_s'].max():.1f}s]")
    print(f"  Delta Tok: {t_diff:+.1f} | Speedup: {spd:.1f}x | Acc Diff: {acc_diff:+.2f} pp")

print("\n" + "="*90)
print("INTERPRETATION 2: Strictly Correct in BOTH models on each dataset")
print("="*90)
for ds_folder, ds_name in datasets:
    gm = gemma_data[ds_folder]
    gn = gemini_data[ds_folder]
    
    gm_sub = gm[gm['orig_task'].isin(shared_base_252)]
    gn_sub = gn[gn['orig_task'].isin(shared_base_252)]
    
    gm_corr = gm_sub[gm_sub['is_correct']]
    gn_corr = gn_sub[gn_sub['is_correct']]
    
    both_corr_orig = set(gm_corr['orig_task']).intersection(set(gn_corr['orig_task']))
    
    gm_both = gm_corr[gm_corr['orig_task'].isin(both_corr_orig)]
    gn_both = gn_corr[gn_corr['orig_task'].isin(both_corr_orig)]
    
    t_diff = gm_both['tokens'].mean() - gn_both['tokens'].mean()
    spd = gm_both['time_s'].mean() / gn_both['time_s'].mean()
    
    print(f"\n[{ds_name}] (N_both_correct_orig: {len(both_corr_orig)})")
    print(f"  Gemma : {len(gm_both)} tasks | Tok: {gm_both['tokens'].mean():.1f} ± {gm_both['tokens'].std():.1f} [{gm_both['tokens'].min()} - {gm_both['tokens'].max()}] | Time: {gm_both['time_s'].mean():.1f}s ± {gm_both['time_s'].std():.1f}s [{gm_both['time_s'].min():.1f}s - {gm_both['time_s'].max():.1f}s]")
    print(f"  Gemini: {len(gn_both)} tasks | Tok: {gn_both['tokens'].mean():.1f} ± {gn_both['tokens'].std():.1f} [{gn_both['tokens'].min()} - {gn_both['tokens'].max()}] | Time: {gn_both['time_s'].mean():.1f}s ± {gn_both['time_s'].std():.1f}s [{gn_both['time_s'].min():.1f}s - {gn_both['time_s'].max():.1f}s]")
    print(f"  Delta Tok: {t_diff:+.1f} | Speedup: {spd:.1f}x")
