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

# %%
database=client["ziggle_db"]
collection=database["ziggle_content"]

# %%
# collection.insert_many(df.to_dict('records'))
# # %%
# collection.update_many({}, {"$unset": {"Unnamed: 0": ""}})

# # %%
# for index, row in df.iterrows():
#     document=collection.find_one({"title": row["title"], "views": row["views"]})
#     if document:
#         collection.update_one({"_id": document["_id"]}, {"$set": {"body_embedded": row["body_embedded"]}})
# # %%
# print(len(df["body_embedded"][0]))
# %%
query_body="""
[:cat: 인포팀(정보국) 2024년도 신규 부원 모집 :cat:]
:dizzy: 인포팀 소개 페이지
:dizzy: 인포팀 서류 접수 페이지

서류 접수 시 'AMS가 처음이 아니신가요?' 버튼은 무시하셔도 됩니다!

:dizzy: 문의사항 연락처
제 카톡 개인 메세지로 문의해주세요!
※ 학번을 아직 발급받지 못한 신입생 여러분들은 학번을 발급받고 신청해주세요!
"""
# %%
def mute_detection(query_body):
    pipeline=[
        {
        "$vectorSearch":{
            "index": "vector_index",
            "path": "body_embedded",
            "queryVector": embedding.get_embedding(query_body),
            "numCandidates": 5,
            "limit": 1,
            }
        }, {
            "$project": {
                "_id":0,
                "title":1,
                "body":1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    results=collection.aggregate(pipeline)

    for result in results:
        if result["score"]>=0.95:
            return {"mute":True, "mute_content":{"title": result["title"], "body": result["body"]}}
        elif result["score"]<0.95:
            return {"mute":False}
# %%
if __name__=="__main__":
    mute_result=mute_detection(query_body)
    print(mute_result)
# %%
