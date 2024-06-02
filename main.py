# %%
from functools import lru_cache
import config

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import mute_detection

app=FastAPI()
router = APIRouter()
class DetectionRequest(BaseModel):
    body: str 

@lru_cache
def get_settings():
    return config.Settings()

@app.get('/')
async def root():
    return {"message": "Hello FastAPI"}

@app.post("/mute_detection")
def mute_check(body_query: DetectionRequest):
    return mute_detection.mute_detection(body_query.body)

# %%
app.include_router(router, prefix="/api")