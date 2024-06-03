# %%
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import numpy as np
import pandas as pd
import embedding
import os

load_dotenv(override=True)
# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
# client.admin.command("ping")

database=client["ziggle_db"]
collection=database["ziggle_content"]

# %%
def insert_mongodb(target_dict):
    if "body_embedded" not in target_dict.keys():
        target_dict["body_embedded"]=embedding.get_embedding(target_dict["body"])
    collection.insert_one(target_dict)

# %%
if __name__=="__main__":
    database=client["ziggle_db"]
    collection=database["ziggle_content"]

    df=pd.read_excel("./data/formatted_notice.xlsx")
    for i in range(0, len(df)):
        row_dict=df.loc[i].to_dict()
        row_dict["author"]={"uuid": row_dict["author_uuid"], "name": row_dict["author_name"]}
        row_dict.pop("author_uuid")
        row_dict.pop("author_name")

        row_dict["body_embedded"]=embedding.get_embedding(row_dict["body"])
        collection.insert_one(row_dict)

# %%
len(row_dict["body_embedded"])
# %%
