import sys
import os
import pytest
from src.stutter_detector.component_services.audio_clean_service import (
    AudioCleanService,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.mark.asyncio
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

    assert "error" not in result
    assert "cleaned_audio_path" in result
