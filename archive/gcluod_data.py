# %%
import pandas as pd
import os
# %%
base=os.path.dirname(os.path.abspath(__file__))
print(base)
# %%
df=pd.read_csv(f'{base}/data/deadline-detection-finetune-refine.csv', encoding='cp949')
# %%
df
# %%
jsonl_data=df.apply(lambda row: {"messages": [{"role": "user", "content": {row["body"]}}, {"role": "model", "content": {row["AI_deadline_refine"]}} ]}, axis=1)
# %%
jsonl_df=pd.DataFrame(jsonl_data.tolist())
# %%
jsonl_df.to_json(f'{base}/data/gc_finetune_training.jsonl', orient='records', lines=True)
# %%
