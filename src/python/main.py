import inworld
import os
from dotenv import load_dotenv  # For local testing
import requests
import base64
import json

load_dotenv()  # For local testing

default_settings = inworld.InWorldSettings(
    voice="Dennis",
    api_key=os.environ.get("INWORLD_API_KEY"),
    model="inworld-tts-1-max"
)

default_provider = inworld.InWorldProvider(default_settings)
text=""

gen_id, results = default_provider.generate(text)

print(f"File: {gen_id}\nCost: ~{default_provider.estimate_cost(text)}c")