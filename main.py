# %%
from functools import lru_cache
import config

import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import mute_detection
import mongodb

app=FastAPI()
router = APIRouter()
class DetectionRequest(BaseModel):
    body: str 

@lru_cache
def get_settings():
    return config.Settings()

@app.get('/')
async def root():
    return {"message": "Ziggle-ai backend is running!"}

@app.post("/mute_detection")
def mute_check(body_query: DetectionRequest):
    return mute_detection.mute_detection(body_query.body)

@app.post("/similar_notices")
def similar_notices(body_query: DetectionRequest):
    result =  mute_detection.similar_notices(body_query.body)
    return result

@app.post("/upload_notice_to_mongodb")
def upload_notice_to_vector_index(target_dict: dict):
    return mongodb.insert_mongodb(target_dict)
# %%
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)