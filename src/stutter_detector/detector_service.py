from fastapi import HTTPException
import asyncio
import traceback
from src.utils.logger import logger
from sklearn.metrics.pairwise import cosine_similarity
import librosa
import numpy as np
import re
class DetectorService:
    def __init__(self):
        logger.info("Detector Service initialized.")
        self.similarity_threshold = 0.98
        self.min_repetitions = 4
        self.min_time = 0.3
        self.energy_threshold = 2.0
        self.min_duration = 0.5
        self.silent_thresh = 0.01
        self.block_thresh = 1.0

    def detect_repetitions (self,sr, mfcc):
        logger.info("Detecting repetitions in MFCC features...")
        try:
            repeat_indices = []
            for i in range(mfcc.shape[1] - 1):
                sim = cosine_similarity(mfcc[:, i].reshape(1, -1), mfcc[:, i+1].reshape(1, -1))[0][0]
                if sim > self.similarity_threshold:
                    repeat_indices.append(i)
            clustered = []
            cluster = []
            for idx in repeat_indices:
                if not cluster or idx == cluster[-1] + 1:
                    cluster.append(idx)
            else:
                if len(cluster) >= self.min_repetitions:
                    clustered.append(cluster)
                cluster = [idx]
            if len(cluster) >= self.min_repetitions:
                clustered.append(cluster)

            times = [librosa.frames_to_time(c[0], sr=sr, hop_length=512).item() for c in clustered]
            filtered_times = [t for t in times if t >= self.min_time]
            logger.info("detection of repetitions completed")
            return filtered_times
        except Exception as e:
            logger.error(f"Error in detect_repetitions: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Error in detecting repetitions")
    
    def detect_prolongation(self,audio, sr):
        logger.info("Detecting prolongations in audio...")
        try:
            spec = librosa.feature.melspectrogram(y=audio, sr=sr)
            db_spec = librosa.power_to_db(spec, ref=np.max)

            energy_diff = np.abs(np.diff(db_spec, axis=1)).mean(axis=0)
            mean_energy_per_frame = db_spec.mean(axis=0)
            mean_energy_per_frame = mean_energy_per_frame[:-1]
            energy_floor = -40  # tune this!
            prolonged_frames = (energy_diff < self.energy_threshold) & (mean_energy_per_frame > energy_floor)

            # Find contiguous frame sequences
            count = 0
            starts = []
            for i, val in enumerate(prolonged_frames):
                if val:
                    count += 1
                else:
                    if count >= (self.min_duration * sr / 512):
                        starts.append(i - count)
                    count = 0
            logger.info("Prolongation detection completed")
            return [librosa.frames_to_time(s, sr=sr).item() for s in starts]
        except Exception as e:
            logger.error(f"Error in detect_prolongation: {e}")
            raise HTTPException(status_code=500, detail="Error in detecting prolongations")
    
    def detect_blocks_phoneme(self, alignment ):
        logger.info("Detecting blocks of phonemes...")
        try:
            block_thresh=0.3
            blocks = []
            prev_end = 0
            for word in alignment:
                start = float(word['start'])
                if start - prev_end > block_thresh:
                    blocks.append(prev_end)
                prev_end = float(word['end'])
            logger.info("Block detection completed")
            return blocks
        except Exception as e:
            logger.error(f"Error in detect_blocks_phoneme: {e}")
            raise HTTPException(status_code=500, detail="Error in detecting blocks of phonemes")
        
    
    async def repeatedWords(self,transcript):
        logger.info("Detecting repeated words in transcript...")
        max_retries = 2
        for attempt in range(max_retries):
            try:
                repeated_words = re.findall(r'\b(\w+)(?:[ -]+\1\b)+', transcript.lower())
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(f"Retrying recording in 5 seconds...")
                    await asyncio.sleep(5)

                else:
                    repeatedWords = None
        logger.info("Repeated words detection completed")
        return repeated_words

    def fillers(self,transcript):
        logger.info("Detecting fillers in transcript...")
        max_retries = 2
        for attempt in range(max_retries):
            try:
                fillers = re.findall(r'\b(um+|uh+|er+|ah+)\b', transcript.lower())
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.info(f"Retrying recording in 5 seconds...")
                    asyncio.sleep(5)
                else:
                    logger.error(f"Fillers detection failed: {e}")
                    logger.error(traceback.format_exc())
                    fillers = None
        logger.info("Fillers detection completed")
        return fillers
    async def detect_stutters(self,audio, transcription, sr, alignment,mfcc):
        logger.info("Starting stutter detection...")
        try:
            # Detect repeated words
            repeated_words = await self.repeatedWords(transcription)
            blocks = self.detect_blocks_phoneme(alignment)
            fillers = self.fillers(transcription)
            repeated_syllables = self.detect_repetitions(sr, mfcc)
            prolongations = self.detect_prolongation(audio, sr)
            result = {
                "repeated_words": repeated_words,
                "blocks": blocks,
                "fillers": fillers,
                "repeated_syllables": repeated_syllables,
                "prolongations": prolongations
            }
            logger.info("Stutter detection completed successfully.")
            return result
        except Exception as e:
            logger.error(f"Stutter detection failed: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Stutter detection failed")

