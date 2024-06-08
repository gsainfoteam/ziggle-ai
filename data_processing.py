# %%
import emoji
import re
import pandas as pd

df=pd.read_excel("./data/formatted_notice.xlsx", engine="openpyxl")
# %% step1: delete tags except <strong>
def tag_processing(body: str) -> str:
    return re.sub(r'<(?!\/?strong\s*\/?)[^>]+>', '', body)

# %% step2: demojize
def demojize(body: str) -> str:
    return emoji.demojize(body)

# %% step3: revert demojized emoji
def revert_demojize(body: str) -> str:
    return emoji.emojize(body)

# %%
if __name__=="__main__":
    df["body"]=df["body"].apply(tag_processing)
    df["body"]=df["body"].apply(demojize)
    df.to_excel("./data/formatted_notice.xlsx", index=False)
# %%
