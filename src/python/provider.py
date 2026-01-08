from pydantic import BaseModel

class GenerationSettings(BaseModel):
    voice: str

class TTSProvider:
    def __init__(self, settings: GenerationSettings):
        self.settings = settings

    def estimate_cost(self, text: str):
        '''
        Estimates cost for generating audio from text for the given provider, in cents.
        
        :param text: text to generate
        :type text: str
        :param settings: GenerationSettings to use; varies by provider
        :type settings: GenerationSettings
        '''
        pass