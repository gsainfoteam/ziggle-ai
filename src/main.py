# %%
from functools import lru_cache
import config

import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from deadline_detection import extract_deadline
# import mongodb
# from mute_detection import mute_detection
# from mute_validation import mute_validation

app=FastAPI()
router = APIRouter()
class DetectionRequest(BaseModel):
    body: str 

class MuteEdgeCase(BaseModel):
    source_body: str
    result_body: str
    similarity_score: float

class DeadlineRequest(BaseModel):
    body: str
    createdAt: str

@lru_cache
def get_settings():
    return config.Settings()

@app.get('/')
async def root():
    return {"message": "Ziggle-ai backend is running!"}

@app.post("/deadline_detection")
def get_deadline(body_query: DeadlineRequest):
    return extract_deadline(body=body_query.body, createdAt=body_query.createdAt)

# @app.post("/mute_detection")
# def mute_check(body_query: DetectionRequest):
#     return mute_detection.mute_detection(body_query.body)

# @app.post("/similar_notices")
# def similar_notices(body_query: DetectionRequest):
#     result =  mute_detection.similar_notices(body_query.body)
#     return result

# @app.post("/upload_notice_to_mongodb")
# def upload_notice_to_vector_index(target_dict: DetectionRequest):
#     return mongodb.insert_mongodb(target_dict)

# @app.post("/insert_mute_edge_case")
# def insert_mute_edge_case(mute_failed_case: MuteEdgeCase):
#     return mute_validation.insert_edge_case(mute_failed_case)
# %%
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)