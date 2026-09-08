import pandas as pd

def analyze_model(name, path_run1, path_run2):
    print(f"\n" + "="*70)
    print(f"ANÁLISE DE CONSISTÊNCIA ENTRE RUNS: {name}")
    print(f"="*70)
    
    df1 = pd.read_csv(path_run1)
    df2 = pd.read_csv(path_run2)
    
    task_col_1 = df1.columns[0]
    val_col_1 = df1.columns[1]
    
    task_col_2 = df2.columns[0]
    val_col_2 = df2.columns[1]
    
    # Filter out summary row if present (e.g. 'Batch Accuracy')
    df1 = df1[~df1[task_col_1].astype(str).str.contains('Batch Accuracy|Summary|Total', case=False, na=False)].copy()
    df2 = df2[~df2[task_col_2].astype(str).str.contains('Batch Accuracy|Summary|Total', case=False, na=False)].copy()
    
    # Clean task names
    df1['clean_task'] = df1[task_col_1].astype(str).str.replace('.json', '', case=False).str.strip()
    df2['clean_task'] = df2[task_col_2].astype(str).str.replace('.json', '', case=False).str.strip()
    
    # Check values
    def is_correct(val):
        s = str(val).strip().upper()
        return s in ['CORRECT', '1', '1.0', 'TRUE', 'ACERTOU', 'CORRETO', 'PASS']
    
    correct_1 = set(df1[df1[val_col_1].apply(is_correct)]['clean_task'])
    correct_2 = set(df2[df2[val_col_2].apply(is_correct)]['clean_task'])
    
    total_1 = len(df1)
    total_2 = len(df2)
    
    both_correct = correct_1.intersection(correct_2)
    only_run1 = correct_1 - correct_2
    only_run2 = correct_2 - correct_1
    
    failed_1 = set(df1['clean_task']) - correct_1
    failed_2 = set(df2['clean_task']) - correct_2
    both_failed = failed_1.intersection(failed_2)
    
    diff_tasks = only_run1.union(only_run2)
    
    print(f"Total de Tarefas Avaliadas: Run 1 = {total_1}, Run 2 = {total_2}")
    print(f"Tasks Corretas no Run 1 (Original): {len(correct_1)} / {total_1} ({len(correct_1)/total_1*100:.2f}%)")
    print(f"Tasks Corretas no Run 2 (Second):   {len(correct_2)} / {total_2} ({len(correct_2)/total_2*100:.2f}%)")
    print(f"-"*70)
    print(f"Tasks Corretas em AMBOS os Runs (Intersecção de Acertos): {len(both_correct)}")
    print(f"Tasks Erradas em AMBOS os Runs (Intersecção de Erros):     {len(both_failed)}")
    print(f"-"*70)
    print(f"Tasks que ACERTOU no Run 1 mas ERROU no Run 2 (Perdidas):  {len(only_run1)}")
    print(f"Tasks que ERROU no Run 1 mas ACERTOU no Run 2 (Novas):     {len(only_run2)}")
    print(f"-"*70)
    print(f"TOTAL DE TASKS COM RESULTADO DIFERENTE: {len(diff_tasks)} ({len(diff_tasks)/total_1*100:.2f}% de variação)")
    print(f"Taxa de Concordância (Mesmo resultado nos 2 runs): {(len(both_correct) + len(both_failed)) / total_1 * 100:.2f}% ({len(both_correct) + len(both_failed)}/{total_1})")
    print(f"Índice Jaccard de Consistência nos Acertos: {len(both_correct) / len(correct_1.union(correct_2))*100:.2f}% ({len(both_correct)}/{len(correct_1.union(correct_2))})")
    
    print(f"\n>>> Tasks que ACERTOU no Run 1 mas ERROU no Run 2 ({len(only_run1)}):")
    for i, t in enumerate(sorted(list(only_run1)), 1):
        print(f"  {i:2d}. {t}")
        
    print(f"\n>>> Tasks que ERROU no Run 1 mas ACERTOU no Run 2 ({len(only_run2)}):")
    for i, t in enumerate(sorted(list(only_run2)), 1):
        print(f"  {i:2d}. {t}")
        
    return {
        'model': name,
        'total': total_1,
        'correct_1': len(correct_1),
        'correct_2': len(correct_2),
        'both_correct': len(both_correct),
        'both_failed': len(both_failed),
        'only_1': sorted(list(only_run1)),
        'only_2': sorted(list(only_run2)),
        'diff': sorted(list(diff_tasks)),
        'concordance_pct': (len(both_correct) + len(both_failed)) / total_1 * 100,
        'jaccard_pct': len(both_correct) / len(correct_1.union(correct_2))*100
    }

if __name__ == '__main__':
    gemma = analyze_model(
        "Gemma 4 (31B-IT)",
        r"Results/Gemma/Training Data Set/train_results_accuracy.csv",
        r"Results/GEMMA_train_results_second_run_accuracy.csv"
    )
    
    gemini = analyze_model(
        "Gemini 3.5 Flash Lite",
        r"Results/Gemini_3.5_Flash_Lite/Training Data Set/train_results_accuracy.csv",
        r"Results/train_results_second_run_accuracy.csv"
    )
