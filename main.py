# %%
from functools import lru_cache
import config

from fastapi import FastAPI
import mute_detection

app=FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get('/')
async def root():
    return {"message": "Hello FastAPI"}

@app.post("/mute_detection")
def mute_check(body_query):
    return mute_detection.mute_detection(body_query)
# %%
