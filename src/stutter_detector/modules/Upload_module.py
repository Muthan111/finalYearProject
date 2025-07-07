import os
import traceback
import logging
from src.utils.logger import logger
import uuid
import shutil

class UploadService:
    """
    This service handles the upload of audio files.
    It checks for allowed content types, file extensions, and size limits.
    It saves the uploaded files to a specific directory and returns the file path and display URL.
    It also creates the directory if it does not exist.
    """
    
    ALLOWED_CONTENT_TYPES = {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"}
    ALLOWED_EXTENSIONS = {".wav", ".mp3"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    def __init__(self):
        
        self.directory = "uploaded_files"
        

    def create_directory(self):
        """        Creates the directory for uploaded files if it does not exist.
        """
        logger.info("Creating directory for uploaded files.")
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            print(f"Directory '{self.directory}' created.")
        else:
            print(f"Directory '{self.directory}' already exists.")
    
    def audio_upload(self, file):
        """
        Handles the upload of an audio file.
        Args:
            file: The audio file to be uploaded.
        Returns:
            A dictionary containing the filename, file path, and display URL if successful.
            An error message if an exception occurs.
        """
        try:
            logger.info(f" [audio_upload] Starting audio upload process.")
            self.create_directory()
            audio_displayURL = "http://127.0.0.1:8000/static"
            # === Content type and extension check ===
            if file.content_type not in self.ALLOWED_CONTENT_TYPES:
                raise ValueError(f"Unsupported content type: {file.content_type}")

            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValueError(f"Unsupported file extension: {ext}")

            # === Temp read to check size ===
            contents = file.file.read()
            size = len(contents)
            if size > self.MAX_FILE_SIZE:
                raise ValueError(f"File size {size / (1024 * 1024):.2f}MB exceeds limit of {self.MAX_FILE_SIZE / (1024 * 1024)}MB")

            # Rewind for writing
            file.file.seek(0)

            # Safe filename to avoid overwrites or injection
            safe_filename = f"{uuid.uuid4().hex}{ext}"
            file_path = os.path.join(self.directory, safe_filename)
            website_audio = os.path.join(audio_displayURL, safe_filename)
            # === Save the file ===
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            logger.info(f"✅ File '{safe_filename}' uploaded successfully to '{self.directory}'")
            return {"filename": safe_filename, "filepath": file_path,"audioDisplayURL": website_audio}

        except Exception as e:
            logger.error(f"❌ Error uploading file: {e}")
            logger.error(traceback.format_exc())
            return {"error": str(e)}
        