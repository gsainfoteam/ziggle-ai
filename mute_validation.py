# %% TODO: mute detection model validation (find edge cases)
# {source body, result body, similarity score}

# %%
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os

load_dotenv(override=True)
# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
client.admin.command("ping")

# %%
database=client["ziggle_db"]
collection=database["mute_edge_cases"]

# %%
def insert_edge_case(mute_failed_case):
    collection.insert_one(mute_failed_case)