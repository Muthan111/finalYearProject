import asyncio

# import whisper
from faster_whisper import WhisperModel
from src.utils.logger import logger
import traceback
from fastapi import HTTPException
from gradio_client import Client, file
import sys
import os
from dotenv import load_dotenv

load_dotenv()
gradio_url = os.getenv("GRADIO_URL")
# Add the absolute path of the project root to sys.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
)


class WhisperService:

    def __init__(self, use_gradio: bool = False):
        self.use_gradio = use_gradio

        self.result = None

        self.language = "en"
        self.initial_prompt = "uh um like you know so"
        self.beam_size = 5
        self.temperature = [0.0, 0.2, 0.4]

        if self.use_gradio:
            self.gradio_url = gradio_url
            self.client = Client(self.gradio_url)
        else:
            self.model = WhisperModel(
                "medium.en", device="cpu", compute_type="int8"
            )

    def transcribe_gradio(self, audio_path):
        try:
            audio = file(audio_path)
            segments = self.client.predict(
                audio, api_name="/predict"
            )  # Expecting list of segments from Colab
            logger.info(
                f"[transcribe_gradio function] Received segments: {segments}"
            )
            full_text = ""
            word_timestamps = []

            for segment in segments:
                full_text += segment.get("text", "") + " "

                if "words" in segment and segment["words"]:
                    for word in segment["words"]:
                        word_timestamps.append(
                            {
                                "word": word.get("word", "").strip(),
                                "start": float(word.get("start", 0)),
                                "end": float(word.get("end", 0)),
                            }
                        )

            return {
                "transcription": full_text.strip(),
                "word_timestamps": word_timestamps,
            }

        except Exception as e:
            logger.error(
                f"[transcribe_gradio function] Transcription failed: {e}"
            )
            logger.error(traceback.format_exc())
            return {"error": f"Transcription failed: {str(e)}"}

    async def transcribe_using_local_model(self, audio_file):
        logger.info(" Transcribing audio file")
        await asyncio.sleep(0)
        max_retries = 2
        for attempt in range(max_retries):
            try:
                segments, info = self.model.transcribe(
                    audio_file,
                    language=self.language,
                    initial_prompt=self.initial_prompt,
                    word_timestamps=True,
                    beam_size=self.beam_size,
                    temperature=self.temperature,
                )
                full_text = ""
                word_timestamps = []
                for segment in segments:
                    full_text += segment.text + " "
                    if segment.words:  # only if words are available
                        for word in segment.words:
                            word_timestamps.append(
                                {
                                    "word": word.word.strip(),
                                    "start": float(word.start),
                                    "end": float(word.end),
                                }
                            )
                return {"text": full_text.strip(), "words": word_timestamps}

            except Exception as e:
                logger.error(f"""[transcribe function]
                        Transcription failed: {e}""")
                logger.error(traceback.format_exc())
                if attempt < max_retries - 1:
                    logger.info("Retrying transcription in 5 seconds...")
                    await asyncio.sleep(5)
                else:
                    logger.error(
                        "Transcription failed after multiple attempts."
                    )
                    logger.error(traceback.format_exc())
                    segments = None
                    raise HTTPException(
                        status_code=500, detail="Transcription failed"
                    )

    async def transcribe(self, audio_file):
        logger.info(
            f"Transcribing audio file (use_gradio = {self.use_gradio})"
        )
        await asyncio.sleep(0)
        if self.use_gradio:
            try:
                return self.transcribe_gradio(audio_file)
            except Exception as e:
                logger.error(f"""[transcribe function]
                             Gradio transcription failed: {e}""")
                logger.error(traceback.format_exc())
                raise HTTPException(
                    status_code=500, detail="Gradio transcription failed"
                )

        else:
            try:
                return await self.transcribe_using_local_model(audio_file)
            except Exception as e:
                logger.error(f"""[transcribe function]
                    Local transcription failed: {e}""")
                logger.error(traceback.format_exc())
                raise HTTPException(
                    status_code=500, detail="Local transcription failed"
                )

    def convert_alignment_to_string(self, alignment):
        logger.info("Converting alignment to string...")
        word_timestamps = [
            f"{word['word']} ({word['start']:.2f}s to {word['end']:.2f}s)"
            for word in alignment
        ]
        word_and_timestamps_string = ", ".join(word_timestamps)
        logger.info("Alignment converted to string successfully.")
        return word_and_timestamps_string
