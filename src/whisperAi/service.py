import asyncio
import whisper

class WhisperAiService:

    def __init__(self):
        self.result = None
        self.model = whisper.load_model("base")
        self.language = "en"

    async def transcribe(self, audio_file):
        await asyncio.sleep(0)  # Simulate async behavior
        self.result = self.model.transcribe(audio_file, language=self.language)
        print("Transcription:", self.result["text"])
        return self.result["text"]

    