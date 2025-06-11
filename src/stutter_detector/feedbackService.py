class FeedbackService:
    def __init__(self):
        self.feedback = []

    def repetions_feedback(self, repetitions):
        num_repetitions = len(repetitions)
        
        if num_repetitions > 0:
            self.feedback.append(f"⚠️ You had {num_repetitions} repetitions. Try to pace your speech more steadily.")
        else:
            self.feedback.append("✅ Great! You had no repetitions.")
    def prolongations_feedback(self, prolongations):
        num_prolongations = len(prolongations)
        if  num_prolongations > 0:
            self.feedback.append(f"⚠️ You had {num_prolongations} repetitions. Try to pace your speech more steadily.")
        else:
            self.feedback.append("✅ Great! No prolongations detected.")

    def blocks_feedback(self, blocks):
        num_blocks = len(blocks)
        if num_blocks > 0:
            self.feedback.append(f"⚠️ You had {num_blocks} blocks. Try to relax and take a deep breath before speaking.")
            
        else:
            self.feedback.append(" ✅ Great! No blocks detected.")

    def repeated_words_feedback(self, repeated_words):
        num_repeated_words = len(repeated_words)
        if num_repeated_words > 0:
            self.feedback.append(f"⚠️ You had {num_repeated_words} repeated words. Try to vary your vocabulary.")
            self.feedback.append(f"Repeated words: {', '.join(repeated_words)}")

        else:
            self.feedback.append("✅ Great! No repeated words detected.")

    def fillers_feedback(self, fillers):
        num_fillers = len(fillers)
        
        if num_fillers > 0:
            self.feedback.append(f"⚠️ You had {num_fillers} fillers. Try to reduce the use of fillers in your speech.")
            
        else:
            self.feedback.append("✅ Great! No fillers detected.")