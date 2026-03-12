import os
import pytest
from src.stutter_detector.component_services.audio_clean_service import (
    AudioCleanService,
)


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
    test_file_path = os.path.join(
        os.path.dirname(__file__), "FluencyBank_096_1.wav"
        )

    # Run the audio processing pipeline
    result = await audio_pipeline.preprocess_audio(test_file_path)

    assert "error" not in result
    assert "cleanedAudio" in result
    assert "sr" in result
