import provider
import requests
import base64
import uuid
import os
from elevenlabs.client import ElevenLabs

OUTPUT_PATH="elevenlabs"



class ElevenLabsSettings(provider.GenerationSettings):
    voice: str
    api_key: str
    model: str="eleven_multilingual_v2"
    output_format: str="mp3_44100_128"
    output_path: str=OUTPUT_PATH

class ElevenLabsProvider(provider.TTSProvider):

    def __init__(self, settings: ElevenLabsSettings):
        self.settings = settings
        self.elevenlabs = ElevenLabs(
        api_key=settings.api_key,
        )

    def estimate_cost(self, text: str):
        return 15*len(text)/1000
    
    def generate(self, text: str):
        os.makedirs(f"output/{self.settings.output_path}", exist_ok=True)

        generation_id = uuid.uuid8()
        
        audio_content = self.elevenlabs.text_to_speech.convert(
        text=text,
            voice_id=self.settings.voice,
            model_id=self.settings.model,
            output_format=self.settings.output_format,
        )

        with open(f"output/{self.settings.output_path}/{generation_id}.mp3", "wb") as f:
            for chunk in audio_content:
                if chunk:
                    f.write(chunk)

        return generation_id, {"status":200}