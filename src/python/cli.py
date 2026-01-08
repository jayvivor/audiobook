import inworld
import elevenlabs_provider as eleven
import provider
import os
from dotenv import load_dotenv  # For local testing
import requests
import base64
import json
import argparse
import yaml

load_dotenv()  # For local testing

parser = argparse.ArgumentParser(description="Generate audio from text using InWorld API.")
parser.add_argument("-i", "--input", required=True, help="Path to the input text file.")
parser.add_argument("-c", "--config", required=False, help="Path to the configuration file (optional).")
parser.add_argument("-e", "--estimate", action="store_true", help="Flag to estimate cost without generating audio.")
parser.add_argument("-s", "--split", action="store_true", help="If true, splits the audio into chunks based on paragraphs.")

args = parser.parse_args()

default_settings = inworld.InWorldSettings(
    voice="Dennis",
    api_key=os.environ.get("INWORLD_API_KEY"),
    model="inworld-tts-1-max"
)

if not args.config:
    settings = default_settings
else:
    with open(args.config, "r") as configfile:
        full_config = yaml.safe_load(configfile)
    match full_config["spec"]:
        case "inworld":
            api_key = os.environ.get(full_config["api_key_var"])
            settings = inworld.InWorldSettings(
                voice=full_config["voice"],
                model=full_config["model"],
                api_key=api_key,
                output_path=full_config.get("output_path") or inworld.OUTPUT_PATH
            )
            tts_provider = inworld.InWorldProvider(settings)
        case "elevenlabs":
            api_key = os.environ.get(full_config["api_key_var"])
            if full_config.get("model"):
                settings = eleven.ElevenLabsSettings(
                    voice=full_config["voice"],
                    model=full_config["model"],
                    api_key=api_key,
                )
            else:
                settings = eleven.ElevenLabsSettings(
                    voice=full_config["voice"],
                    api_key=api_key,
                )
            tts_provider = eleven.ElevenLabsProvider(settings)
        case _:  # By default, just get voice
            settings = provider.GenerationSettings(**full_config)
            tts_provider = provider.TTSProvider(settings)

with open(args.input, "r", encoding="utf-8") as inputfile:
    full_text = inputfile.read()

if args.estimate:
    print(f"Estimated cost: ~{tts_provider.estimate_cost(full_text)}c")
else:
    if args.split:
        filenames = []
        for section in full_text.split("\n"):
            gen_id, results = tts_provider.generate(section)
            print(f"File: {gen_id}\nCost: ~{tts_provider.estimate_cost(section)}c")
            # filenames.append(gen_id) do something here idk. TODO
    else:
        gen_id, results = tts_provider.generate(full_text)
        print(f"File: {gen_id}\nCost: ~{tts_provider.estimate_cost(full_text)}c")