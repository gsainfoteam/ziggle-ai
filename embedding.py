# %%
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
import pandas as pd

load_dotenv(override=True)
client=OpenAI()
enc=tiktoken.get_encoding("cl100k_base")
# %%
def get_embedding(input):
    encode=enc.encode(input)
    if len(encode)>8192:
        encode=encode[:8192]
        input=enc.decode(encode)

    embedding=client.embeddings.create(
            model="text-embedding-3-small",
            input=input
        )
    return embedding.data[0].embedding
# %%
if __name__ == "__main__":
    df=pd.read_excel("./data/formatted_notice.xlsx", engine="openpyxl")
# %%
    df["body_embedded"]=df["body"].apply(get_embedding)
    df.head()
# %%
    # print(type(df["body_embedded"][0]))
# %%
    df.to_excel("./data/formatted_embedded_notice.xlsx", index=False)

# %%
df.head()
# %%
