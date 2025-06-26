import pyaudio
import wave
import os
class MicrophoneService:
    def __init__(self):
        self.result = None
        self.language = "en"
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels  = 1
        self.format = pyaudio.paInt16
        self.frames = []
        self.clip_duration = 30  # seconds
    

    async def start_recording(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                   channels=self.channels,
                                   rate=self.sample_rate,
                                   input=True,
                                   frames_per_buffer=self.chunk_size)
        
        self.frames = []
        for _ in range(0, int(self.sample_rate / self.chunk_size * self.clip_duration)):
            data = self.stream.read(self.chunk_size)
            self.frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        if len(self.frames) == 0:
            print("No audio data captured. Please check your microphone settings.")
        else:
            filepath = "../recordings"
            audioSaved = self.save_audio(self.frames, "recording", filepath)
            audiofilename = audioSaved["filename"]
            audiofilepath = audioSaved["filepath"]
            return {
            "audiofile": audiofilename,
            "audiofilepath": audiofilepath,
            
        
        }
    
    def save_audio(self,frames, inputename, filepath):
        os.makedirs(filepath, exist_ok=True)  # Ensure the directory exists
        audioId = 0
        while True:
            filename = f"{inputename}_{audioId}.wav"
            if not os.path.exists(os.path.join(filepath, filename)):
                break
            audioId += 1
        full_path = os.path.join(filepath, filename)
        with wave.open(full_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
        return {
        "audioId": audioId,
        "filename": filename,
        "filepath": full_path
        }