import librosa
import numpy as np
import asyncio
from sklearn.metrics.pairwise import cosine_similarity
class audioAnalysisService:
    def __init__(self):
        self.n_mfcc = 13
        self.similarity_threshold = 0.98
        self.min_repetitions = 4
        self.min_time = 0.3
        self.energy_threshold = 2.0
        self.min_duration = 0.5
        self.silent_thresh = 0.01
        self.block_thresh = 1.0

    async def extractMFCC(self, audio_file, sr):
        def compute_mfcc():
            mfcc = librosa.feature.mfcc(y=audio_file, sr=sr, n_mfcc=self.n_mfcc)
            mfcc_db = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
            return {
                "mfcc": mfcc,
                "mfcc_db": mfcc_db,
                "sr": sr
            }
        return await asyncio.to_thread(compute_mfcc)
    
    def detect_repetitions (self,sr, mfcc):
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

        print(f"⏱️ Repetition timestamps (filtered): {filtered_times}")
        return filtered_times

    def detect_prolongation(self,audio, sr):
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
        return [librosa.frames_to_time(s, sr=sr).item() for s in starts]
    def detect_block(self, audio,sr):
        energy = librosa.feature.rms(y=audio)[0]
        smoothed_energy = np.convolve(energy, np.ones(5)/5, mode='same')
        silent = smoothed_energy < self.silent_thresh

        first_speech = np.argmax(~silent)
        start_time = librosa.frames_to_time(first_speech, sr=sr)

        if start_time > self.block_thresh:
            return [start_time]
        return []