import asyncio
# import whisper
import re
from faster_whisper import WhisperModel
class WhisperService:

    def __init__(self):
        self.result = None
        # self.model = whisper.load_model("medium.en",)
        self.model = WhisperModel("medium.en", device="cpu", compute_type="int8")
        self.language = "en"
        self.initialPrompt = "uh um like you know so"

    # async def transcribe(self, audio_file):
    #     await asyncio.sleep(0)  # Simulate async behavior
    #     self.result = self.model.transcribe(audio_file, language=self.language, initial_prompt=self.initialPrompt,temperature=0.0,
    #     best_of=5,
    #     beam_size=5,
    #     word_timestamps=True)
    #     print("Transcription:", self.result["text"])
    #     return self.result["text"]
    async def transcribe(self, audio_file):
        await asyncio.sleep(0)
        segments, info = self.model.transcribe(
            audio_file, 
            language=self.language, 
            initial_prompt=self.initialPrompt,
            word_timestamps=True
        )

        full_text = " ".join([segment.text for segment in segments])
        return  full_text
        
    def repeatedWords(self,transcript):
        repeated_words = re.findall(r'\b(\w+)(?:[ -]+\1\b)+', transcript.lower())
        return repeated_words

    def fillers(self,transcript):
        fillers = re.findall(r'\b(um+|uh+|er+|ah+)\b', transcript.lower())
        return fillers
    