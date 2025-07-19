from fastapi import APIRouter, File,Request, UploadFile,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from src.stutter_detector.service import stutterDetectorService
# from src.stutter_detector.TestPipelineService import TestPipelineService
from fastapi.templating import Jinja2Templates
import os
import shutil
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
templates = Jinja2Templates(directory="frontend")
stutter_router = APIRouter()
stutter_service = stutterDetectorService()
# PipelinetTestService = TestPipelineService()



@stutter_router.post(
    "/stutter_detection",
    summary="Detect Stutter in Audio File",
    description="Select this to start recording and get feedback on your stutters"
)

@limiter.limit("5/minute")
async def stutter_detection(request: Request, file: UploadFile = File(...)):
    return await stutter_service.detect_stutter(file)





    
    

    