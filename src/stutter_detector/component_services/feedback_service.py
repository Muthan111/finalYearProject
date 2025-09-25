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

   
    
   

    
    
    
    

    def personalized_feedback(self,detection_feedback):
        logger.info("[FeedbackService] Generating personalized feedback...")
        try:
            prompt = f"""
            You are a feedback generator for stuttering detection.
            The voice recording has been analyzed and the following feedback has been generated:
            {detection_feedback}
            Ignore any blocks with the type rms_silence_block
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
    