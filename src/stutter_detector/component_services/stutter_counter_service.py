import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.utils.logger import logger
import traceback
class StutterCounterService:
    def __init__(self):
        self.stutter_count = []
    def repetitions_count(self, repetitions):
        """
        Counts and logs the number of repetitions in the provided list.
        Args:
            repetitions (list): A list of repetition occurrences, each containing start and end times.
        Returns:
            list: A list of  messages regarding repetitions.
        """
        try:
            num_repetitions = len(repetitions)
            
            if num_repetitions > 0:
                time_ranges = [
                f"{rep['start_time']:.2f}s to {rep['end_time']:.2f}s"
                for rep in repetitions
                ]
                time_string = "; ".join(time_ranges)
                self.stutter_count.append(f"⚠️ You had {num_repetitions} repetition(s) at: {time_string}.")
                
            else:
                self.stutter_count.append("✅ Great! You had no repetitions.")
        except Exception as e:
            logger.error(f"Error in repetions_count: {e}")
            logger.error(traceback.format_exc())
            self.stutter_count.append("❌ Error generating repetitions count.")
        return self.stutter_count
    def prolongations_count(self, prolongations):
        """Counts and logs the number of prolongations in the provided list.
        Args:
            prolongations (list): A list of prolongation occurrences, each containing start and end times.
        Returns:
            list: A list of messages regarding prolongations.
        """
        try: 
            num_prolongations = len(prolongations)
            if  num_prolongations > 0:
                self.stutter_count.append(f"⚠️ You had prolongations at these times:  {prolongations}.")
            else:
                self.stutter_count.append("✅ Great! No prolongations detected.")
        except Exception as e:
            logger.error(f"Error in prolongations_count: {e}")
            logger.error(traceback.format_exc())
            self.stutter_count.append("❌ Error generating prolongations count.")
        return self.stutter_count
    def blocks_count(self, blocks):
        """
        Counts and logs the number of alignment mismatch blocks in the provided list.
        Args:
            blocks (list): A list of block occurrences, each containing start and end times.
        Returns:
            list: A list of messages regarding alignment mismatch blocks.
        """
        try:
            # Filter blocks for type 'alignment_mismatch_block'
            mismatch_blocks = [
                b for b in blocks if b.get('type') == 'alignment_mismatch_block'
            ]
            num_blocks = len(mismatch_blocks)
            
            if num_blocks > 0:
                time_ranges = [
                    f"{block['start']:.2f}s to {block['end']:.2f}s"
                    for block in mismatch_blocks
                ]
                time_string = "; ".join(time_ranges)
                self.stutter_count.append(f"⚠️ You had {num_blocks} alignment mismatch block(s) at: {time_string}.")
            else:
                self.stutter_count.append(" ✅ Great! No  blocks detected.")
                
        except Exception as e:
            logger.error(f"Error in blocks_count: {e}")
            logger.error(traceback.format_exc())
            self.stutter_count.append("❌ Error generating blocks count.")

        return self.stutter_count
    def repeated_word_count(self, repeated_words):
        """
        Counts and logs the number of repeated words in the provided list.
        Args:
            repeated_words (list): A list of repeated words.
        Returns:
            list: A list of messages regarding repeated words.

        """
        try: 
            num_repeated_words = len(repeated_words)
            if num_repeated_words > 0:
                self.stutter_count.append(f"⚠️ You had the following repeated words {repeated_words}.")
                self.stutter_count.append(f"Repeated words: {', '.join(repeated_words)}")

            else:
                self.stutter_count.append("✅ Great! No repeated words detected.")
        except Exception as e:
            logger.error(f"Error in repeated_word_count: {e}")
            logger.error(traceback.format_exc())
            self.stutter_count.append("❌ Error generating repeated words count.")
        return self.stutter_count
    def fillers_count(self, fillers):
        """
        Counts and logs the number of fillers in the provided list.
        Args:
            fillers (list): A list of filler words.
        Returns:
            list: A list of messages regarding fillers.
        """
        try:
            num_fillers = len(fillers)
            
            if num_fillers > 0:
                self.stutter_count.append(f"⚠️ You had the following fillers {fillers}.")
                
            else:
                self.stutter_count.append("✅ Great! No fillers detected.")
        except Exception as e:
            logger.error(f"Error in fillers_count: {e}")
            logger.error(traceback.format_exc())
            self.stutter_count.append("❌ Error generating fillers count.")
        return self.stutter_count
    def convert_count_to_string(self, fillers, repeated_words, blocks, prolongations, repetitions):
        self.fillers_count(fillers)
        self.repeated_word_count(repeated_words)
        self.blocks_count(blocks)
        self.prolongations_count(prolongations)
        self.repetitions_count(repetitions)
        return self.stutter_count

    def clear_count(self):
        logger.info("Clearing Stutter Counter list.")
        self.stutter_count = []
        return self.stutter_count