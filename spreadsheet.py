import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("GEMMA_MODEL", "gemma-4-31b-it")

def save_to_spreadsheet(filename: str, task_name: str, is_correct: bool, reasoning: str, append: bool):
    # Format the data entry
    status = "CORRECT" if is_correct else "INCORRECT"
    cell_data = f"{status}\n\nReasoning:\n{reasoning}"
    
    df_new = pd.DataFrame({
        "Task": [task_name],
        MODEL_NAME: [cell_data]
    })
    
    if append and os.path.exists(filename):
        # Read existing, merge or append
        try:
            df_existing = pd.read_excel(filename)
            # If the task already exists in the file, update it. Otherwise, append.
            if task_name in df_existing['Task'].values:
                df_existing.loc[df_existing['Task'] == task_name, MODEL_NAME] = cell_data
            else:
                df_existing = pd.concat([df_existing, df_new], ignore_index=True)
            df_existing.to_excel(filename, index=False)
        except Exception as e:
            print(f"Error appending to Excel: {e}")
    else:
        # Create new
        df_new.to_excel(filename, index=False)
    
    print(f"Data saved to {filename}")