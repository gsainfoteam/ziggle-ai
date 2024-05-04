# %%
import torchtext
import pandas as pd

df=pd.read_excel("./data/data_processed.xlsx", engine="openpyxl")
df.head()
# %% step1: tag 제거
def tag_processing(df) -> list[str]:
    if type(df)==pd.core.frame.DataFrame:
        body_list=df.body.to_list()
    custom_replacement=torchtext.data.custom_replace([(r'<(?!\/?strong\s*\/?)[^>]+>', '')])
    body_list=list(custom_replacement(body_list))

    columns=df.columns.tolist()
    df_matrix=[0 for i in range(len(columns))]

    for i in range(len(columns)):
        col=columns[i]
        if col=="body":
            df_matrix[i]=body_list
            continue
        
        df_matrix[i]=df[col].to_list()
    return df_matrix
# %% check whether tag_processing works well
df_matrix=tag_processing(df)
df_matrix[1][:5]
# %%