import re
import asyncio
import traceback
from src.utils.logger import logger
from fastapi import HTTPException
import librosa
import numpy as np
class BlockDetectionService:
    def __init__(self):
        pass 

    # def detect_blocks_phoneme(self, alignment ):
    #     """
    #     Detects blocks of phonemes in the alignment data.
    #     Args:
    #         alignment (list): List of words with start and end times.
    #     Returns:
    #         list: A list of blocks with start, end, and duration.

    #     """
    #     logger.info(f"[detect_blocks_phoneme] Detecting blocks of phonemes...")
    #     try:
    #         block_thresh=0.15
    #         blocks = []
    #         prev_end = 0
    #         for word in alignment:
    #             start = float(word['start'])
    #             if start - prev_end > block_thresh:
    #                 blocks.append({
    #                 "start": prev_end,
    #                 "end": start,
    #                 "duration": start - prev_end
    #             })
    #             prev_end = float(word['end'])
    #         logger.info(f"[detect_blocks_phoneme] Block detection completed")
    #         return blocks
    #     except Exception as e:
    #         logger.error(f"[detect_blocks_phoneme] Error in detect_blocks_phoneme: {e}")
    #         raise HTTPException(status_code=500, detail="Error in detecting blocks of phonemes")
    # def detect_energy_blocks(self,audio_path, alignment, sr, frame_duration=0.02, hop_duration=0.01, threshold_db=-35, min_block_duration=0.2):
    #     print(f"\n🔍 Loading audio: {audio_path}")
    #     # y, sr = librosa.load(audio_path, sr=sr)
    #     y=audio_path
    #     frame_length = int(frame_duration * sr)
    #     hop_length = int(hop_duration * sr)

    #     rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    #     times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length, n_fft=frame_length)
    #     db = librosa.amplitude_to_db(rms, ref=np.max)

    #     low_energy = db < threshold_db

    #     blocks = []
    #     start = None

    #     for t, is_silent in zip(times, low_energy):
    #         if is_silent and start is None:
    #             start = t
    #         elif not is_silent and start is not None:
    #             end = t
    #             if end - start >= min_block_duration:
    #                 blocks.append({
    #                     "start": round(start, 2),
    #                     "end": round(end, 2),
    #                     "duration": round(end - start, 2)
    #                 })
    #             start = None

    #     if start is not None:
    #         end = times[-1]
    #         if end - start >= min_block_duration:
    #             blocks.append({
    #                 "start": round(start, 2),
    #                 "end": round(end, 2),
    #                 "duration": round(end - start, 2)
    #             })

    #     print(f"\n🧱 Detected blocks: {blocks if blocks else 'None found'}")
        
    #     print("\n📌 Word alignment:")
    #     for word in alignment:
    #         print(f"{word['word']} ({word['start']} → {word['end']})")

    #     return blocks
    def detect_energy_blocks(self,audio_path, alignment, sr, frame_duration=0.02, hop_duration=0.01, threshold_db=-35, min_block_duration=0.2):
        print(f"\n🔍 Loading audio...")

        y = audio_path  # audio_path is already the waveform
        frame_length = int(frame_duration * sr)
        hop_length = int(hop_duration * sr)

        # Calculate RMS and convert to dB
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
        db = librosa.amplitude_to_db(rms, ref=np.max)

        # Detect pure low-energy blocks (traditional)
        low_energy = db < threshold_db
        blocks = []
        start = None

        for t, is_silent in zip(times, low_energy):
            if is_silent and start is None:
                start = t
            elif not is_silent and start is not None:
                end = t
                if end - start >= min_block_duration:
                    blocks.append({
                        "type": "rms_silence_block",
                        "start": round(start, 2),
                        "end": round(end, 2),
                        "duration": round(end - start, 2)
                    })
                start = None

        # Check if last segment is a block
        if start is not None:
            end = times[-1]
            if end - start >= min_block_duration:
                blocks.append({
                    "type": "rms_silence_block",
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "duration": round(end - start, 2)
                })

        # Alignment-vs-Energy mismatch check
        print("\n🔍 Checking for alignment vs energy mismatch blocks...")
        for i in range(len(alignment) - 1):
            w1 = alignment[i]
            w2 = alignment[i + 1]

            word_gap = w2['start'] - w1['end']
            if 0 <= word_gap <= 0.05:
                # Suspect that Whisper snapped the next word too early
                mask = (times >= w1['end']) & (times <= w2['start'] + 0.6)
                silence_segment_db = db[mask]
                if len(silence_segment_db) == 0:
                    continue

                if np.all(silence_segment_db < threshold_db):
                    duration = times[mask][-1] - times[mask][0]
                    if duration >= min_block_duration:
                        blocks.append({
                            "type": "alignment_mismatch_block",
                            "start": round(times[mask][0], 2),
                            "end": round(times[mask][-1], 2),
                            "duration": round(duration, 2),
                            "words": (w1['word'], w2['word'])
                        })

        print(f"\n🧱 Detected blocks: {blocks if blocks else 'None found'}")

        print("\n📌 Word alignment:")
        for word in alignment:
            print(f"{word['word']} ({word['start']} → {word['end']})")

        return blocks