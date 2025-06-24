from fastapi import APIRouter, File,Request, UploadFile,HTTPException
from fastapi.responses import HTMLResponse
from src.stutter_detector.detectorService import DetectorService
# from src.stutter_detector.TestPipelineService import TestPipelineService
from fastapi.templating import Jinja2Templates
import os
import shutil
templates = Jinja2Templates(directory="frontend")
stutter_router = APIRouter()
stutter_service = DetectorService()
# PipelinetTestService = TestPipelineService()



@stutter_router.post("/stutter_detection",
                     summary="Detect Stutter in Audio File",
                     description="Select this to start recording and get feedback on your stutters",)
async def stutter_detection():
    return await stutter_service.detect_stutter()



    
    

    