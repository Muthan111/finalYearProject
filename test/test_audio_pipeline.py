import asyncio
import sys
import os
from src.stutter_detector.component_services.audio_clean_service import (
    AudioCleanService,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def test_audio_pipeline():
    """
    Test the audio processing pipeline
    by simulating an audio file upload and processing.
    """
    # Create an instance of the AudioPipeline
    audio_pipeline = AudioCleanService()

    # Simulate an audio file upload
    # (replace 'test_audio.wav' with your test file)
    test_file_path = "empty.wav"

    # Run the audio processing pipeline
    result = await audio_pipeline.preprocess_audio(test_file_path)

    # Check if there was an error in processing
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("Audio processing completed successfully.")
        print(f"Original Audio Path: {result['original_audio_path']}")
        print(f"Cleaned Audio Path: {result['cleaned_audio_path']}")
        print(f"Audio Display URL: {result['audio_display_url']}")
        print(f"Sample Rate: {result['sr']}")


if __name__ == "__main__":
    asyncio.run(test_audio_pipeline())
