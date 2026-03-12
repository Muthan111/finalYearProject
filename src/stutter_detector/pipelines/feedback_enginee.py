from src.utils.logger import logger
import traceback
from src.stutter_detector.component_services.feedback_service import (
    FeedbackService,
)

from src.stutter_detector.component_services.stutter_counter_service import (
    StutterCounterService,
)


class FeedbackEngine:
    def __init__(self):

        self.feedback = FeedbackService()
        self.stutter_counter = StutterCounterService()

    def run_engine(self, detections):
        """
        Runs the feedback engine to generate
        feedback and counts based on detected stutters.
        Args:
            detections (dict): Dictionary containing
            lists of detected stutters.
        """
        logger.info("[FeedbackEngine] Running feedback engine...")
        try:
            general_count = self.stutter_counter.convert_count_to_string(
                detections["fillers"],
                detections["repeated_words"],
                detections["blocks"],
                detections["prolongations"],
                detections["repeated_syllables"],
            )
            personlized_feedback = self.feedback.personalized_feedback(
                detections
            )
            logger.info("Feedback engine completed successfully.")
            return {
                "personalized_feedback": personlized_feedback,
                "general_count": general_count,
            }

        except Exception as e:
            logger.error(f"[FeedbackEngine] Error in FeedbackEngine: {e}")
            logger.error(traceback.format_exc())
            return {"error": "Feedback generation failed"}
