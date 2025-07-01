import os
import traceback
import logging
from src.utils.logger import logger
class UploadService:
    ALLOWED_CONTENT_TYPES = {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"}
    ALLOWED_EXTENSIONS = {".wav", ".mp3"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    def __init__(self):
        
        self.directory = "uploaded_files"
        

    def create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            print(f"Directory '{self.directory}' created.")
        else:
            print(f"Directory '{self.directory}' already exists.")
    
    def audio_upload(self, file):
        try: 
            self.create_directory()
            if file.content_type not in self.ALLOWED_CONTENT_TYPES:
                raise ValueError(f"Unsupported file type: {file.content_type}. Allowed types are: {self.ALLOWED_CONTENT_TYPES}")
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValueError(f"Unsupported file extension: {ext}. Allowed extensions are: {self.ALLOWED_EXTENSIONS}")
            
            contents = file.file.read()
            if len(contents) > self.MAX_FILE_SIZE:
                raise ValueError(f"File size exceeds the maximum limit of {self.MAX_FILE_SIZE / (1024 * 1024)} MB.")
            file_path = os.path.join(self.directory, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            print(f"File '{file.filename}' uploaded successfully to '{self.directory}'.")
            return {"filename": file.filename, "filepath": file_path}
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            logger.error(traceback.format_exc())
            return {"error": str(e)}
        