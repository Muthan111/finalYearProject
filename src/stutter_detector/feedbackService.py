class FeedbackService:
    def __init__(self):
        self.feedback = []

    def repetions_feedback(self, repetitions):
        num_repetitions = len(repetitions)
        
        if num_repetitions > 0:
            self.feedback.append(f"⚠️ You have repetitions at these times:  {repetitions}.")
            
        else:
            self.feedback.append("✅ Great! You had no repetitions.")
        return self.feedback
    def prolongations_feedback(self, prolongations):
        num_prolongations = len(prolongations)
        if  num_prolongations > 0:
            self.feedback.append(f"⚠️ You had prolongations at these times:  {prolongations}.")
        else:
            self.feedback.append("✅ Great! No prolongations detected.")
        return self.feedback
    def blocks_feedback(self, blocks):
        num_blocks = len(blocks)
        if num_blocks > 0:
            self.feedback.append(f"⚠️ You had blocks at these times: {blocks}. Try to relax and take a deep breath before speaking.")
            
        else:
            self.feedback.append(" ✅ Great! No blocks detected.")
        return self.feedback
    def repeated_words_feedback(self, repeated_words):
        num_repeated_words = len(repeated_words)
        if num_repeated_words > 0:
            self.feedback.append(f"⚠️ You had tyhe following repeated words {repeated_words}.")
            self.feedback.append(f"Repeated words: {', '.join(repeated_words)}")

        else:
            self.feedback.append("✅ Great! No repeated words detected.")
        return self.feedback
    def fillers_feedback(self, fillers):
        num_fillers = len(fillers)
        
        if num_fillers > 0:
            self.feedback.append(f"⚠️ You had the following fillers {fillers}.")
            
        else:
            self.feedback.append("✅ Great! No fillers detected.")
        return self.feedback
    def return_feedback(self):
        return self.feedback
    def personalized_feedback(self):
        print ("Here is your personalized feedback:")