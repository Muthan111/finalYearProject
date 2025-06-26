from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("recording_21.wav", beam_size=5, word_timestamps=True,initial_prompt="This is a raw, unedited speech. Include all disfluencies, repeated words like 'I-I-I', and fillers such as 'uh', 'um', 'like'. Do not correct them.")
segments = list(segments)
# full_text = " ".join([segment.words for segment in segments])
# print(full_text)
# for segment in segments:
#     print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.words}")
# print("Done")
for segment in segments:
    print(f"[{segment.start:.2f}s --> {segment.end:.2f}s] {segment.text}")
    
    if segment.words:
        for word in segment.words:
            print(f"  {word.word} [{word.start:.2f}s - {word.end:.2f}s]")
