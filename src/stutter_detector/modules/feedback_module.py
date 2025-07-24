import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.utils.logger import logger
import traceback
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
class FeedbackService:
    def __init__(self):
        
        self.feedback = []
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def repetions_feedback(self, repetitions):
        try:
            num_repetitions = len(repetitions)
            
            if num_repetitions > 0:
                time_ranges = [
                f"{rep['start_time']:.2f}s to {rep['end_time']:.2f}s"
                for rep in repetitions
                ]
                time_string = "; ".join(time_ranges)
                self.feedback.append(f"⚠️ You had {num_repetitions} repetition(s) at: {time_string}.")
                
            else:
                self.feedback.append("✅ Great! You had no repetitions.")
        except Exception as e:
            logger.error(f"Error in repetions_feedback: {e}")
            logger.error(traceback.format_exc())
            self.feedback.append("❌ Error generating repetitions feedback.")
        return self.feedback
    def prolongations_feedback(self, prolongations):
        try: 
            num_prolongations = len(prolongations)
            if  num_prolongations > 0:
                self.feedback.append(f"⚠️ You had prolongations at these times:  {prolongations}.")
            else:
                self.feedback.append("✅ Great! No prolongations detected.")
        except Exception as e:
            logger.error(f"Error in prolongations_feedback: {e}")
            logger.error(traceback.format_exc())
            self.feedback.append("❌ Error generating prolongations feedback.")
        return self.feedback
    def blocks_feedback(self, blocks):
        try:
            num_blocks = len(blocks)
            if num_blocks > 0:
                time_ranges = [
                    f"{individal_block['start']:.2f}s to {individal_block['end']:.2f}s"
                    for individal_block in blocks
                ]
                time_string = "; ".join(time_ranges)
                self.feedback.append(f"⚠️ You had {num_blocks} block(s) at: {time_string}.")
                
            else:
                self.feedback.append(" ✅ Great! No blocks detected.")
        except Exception as e:
            logger.error(f"Error in blocks_feedback: {e}")
            logger.error(traceback.format_exc())
            self.feedback.append("❌ Error generating blocks feedback.")
        return self.feedback
    def repeated_words_feedback(self, repeated_words):
        try: 
            num_repeated_words = len(repeated_words)
            if num_repeated_words > 0:
                self.feedback.append(f"⚠️ You had tyhe following repeated words {repeated_words}.")
                self.feedback.append(f"Repeated words: {', '.join(repeated_words)}")

            else:
                self.feedback.append("✅ Great! No repeated words detected.")
        except Exception as e:
            logger.error(f"Error in repeated_words_feedback: {e}")
            logger.error(traceback.format_exc())
            self.feedback.append("❌ Error generating repeated words feedback.")
        return self.feedback
    def fillers_feedback(self, fillers):
        try:
            num_fillers = len(fillers)
            
            if num_fillers > 0:
                self.feedback.append(f"⚠️ You had the following fillers {fillers}.")
                
            else:
                self.feedback.append("✅ Great! No fillers detected.")
        except Exception as e:
            logger.error(f"Error in fillers_feedback: {e}")
            logger.error(traceback.format_exc())
            self.feedback.append("❌ Error generating fillers feedback.")
        return self.feedback
    def convert_feedback_to_string(self,fillers, repeated_words, blocks, prolongations, repetitions):
        self.fillers_feedback(fillers)
        self.repeated_words_feedback(repeated_words) 
        self.blocks_feedback(blocks)
        self.prolongations_feedback(prolongations)
        self.repetions_feedback(repetitions)
        return self.feedback
    def convert_alignment_to_string(self, alignment):
        logger.info("Converting alignment to string...")
        word_timestamps = [
            f"{word['word']} ({word['start']:.2f}s to {word['end']:.2f}s)"
            for word in alignment
        ]
        word_and_timestamps_string = ", ".join(word_timestamps)
        logger.info("Alignment converted to string successfully.")
        return word_and_timestamps_string

    def personalized_feedback(self,detection_feedback):
        logger.info("Generating personalized feedback...")
        try:
            prompt = f"""
            You are a feedback generator for stuttering detection.
            The voice recording has been analyzed and the following feedback has been generated:
            {detection_feedback}
            Generate a personalized feedback message based on the provided feedback.
            The feedback should be concise, encouraging, and provide actionable advice for improvement.
            """
            response = self.model.generate_content(prompt)
            logger.info("Personalized feedback generated successfully.")
            return response.text
        except Exception as e:
            print(f"Error generating personalized feedback: {e}")
            response = None
            return response
    def clear_feedback(self):
        logger.info("Clearing feedback list.")
        self.feedback = []
        return self.feedback