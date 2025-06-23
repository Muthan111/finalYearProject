import asyncio
import whisper
import re

class WhisperService:

    def __init__(self):
        self.result = None
        self.model = whisper.load_model("medium.en",)
        self.language = "en"
        self.initialPrompt = "uh um like you know so"

    async def transcribe(self, audio_file):
        await asyncio.sleep(0)  # Simulate async behavior
        self.result = self.model.transcribe(audio_file, language=self.language, initial_prompt=self.initialPrompt,temperature=0.0,
        best_of=5,
        beam_size=5)
        print("Transcription:", self.result["text"])
        return self.result["text"]
    
    def repeatedWords(self,transcript):
        repeated_words = re.findall(r'\b(\w+)(?:[ -]+\1\b)+', transcript.lower())
        return repeated_words

    def fillers(self,transcript):
        fillers = re.findall(r'\b(um+|uh+|er+|ah+)\b', transcript.lower())
        return fillers
    