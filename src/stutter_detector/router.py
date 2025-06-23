from fastapi import APIRouter, File, UploadFile,HTTPException
from fastapi.responses import HTMLResponse
from src.stutter_detector.detectorService import DetectorService
# from src.stutter_detector.TestPipelineService import TestPipelineService
import os
import shutil
stutter_router = APIRouter()
stutter_service = DetectorService()
# PipelinetTestService = TestPipelineService()

# @stutter_router.get("/", response_class=HTMLResponse)
# async def read_root():
#     return """
#     <html>
#         <head>
#             <title>Stutter Detector</title>
#         </head>
#         <body>
#             <h1>Welcome to the Stutter Detector API</h1>
#             <p>Use the endpoints to interact with the Stutter Detector service.</p>
#         </body>
#     </html>
#     """

@stutter_router.post("/stutter_detection",
                     summary="Detect Stutter in Audio File",
                     description="Select this to start recording and get feedback on your stutters",)
async def stutter_detection():
    return await stutter_service.detect_stutter()



    # return {"message": f"File '{file.filename}' saved successfully!"}
    

    