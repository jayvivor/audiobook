import provider
import requests
import base64
import uuid
import os

OUTPUT_PATH="inworld"

class InWorldSettings(provider.GenerationSettings):
    voice: str
    model: str
    api_key: str
    temperature: float=1.1
    output_path: str=OUTPUT_PATH

class InWorldProvider(provider.TTSProvider):
    def __init__(self, settings: InWorldSettings):
        self.settings = settings

    def estimate_cost(self, text: str):
        return len(text)/1000
    
    def generate(self, text: str):
        os.makedirs(f"output/{self.settings.output_path}", exist_ok=True)
        generation_id = uuid.uuid8()

        # https://docs.inworld.ai/docs/quickstart-tts
        url = "https://api.inworld.ai/tts/v1/voice"
        headers = {
            "Authorization": f"Basic {self.settings.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "voiceId": self.settings.voice,
            "modelId": self.settings.model,
            "temperature": self.settings.temperature,
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        audio_content = base64.b64decode(result['audioContent'])


        with open(f"output/{self.settings.output_path}/{generation_id}.mp3", "wb") as f:
            f.write(audio_content)

        return generation_id, result
        
