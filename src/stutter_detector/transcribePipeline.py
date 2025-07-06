from src.stutter_detector.whisperService import WhisperService
class TranscribePipeline:
    def __init__(self):
        self.whisper_service = WhisperService()

    async def run_pipeline(self, file):
        # Step 1: Transcribe the audio file
        transcription = await self.whisper_service.transcribe(file)
        text_transcription = transcription['text']
        alignment = transcription["words"]
        if "error" in transcription:
            return {"error": transcription["error"]}

        # Return the transcription result
        return {
            "text_transcription": text_transcription,
            "alignment": alignment
        }