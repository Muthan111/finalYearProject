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

@stutter_router.post(
    "/stutter_detectionV2",
    summary="Detect Stutter in Audio File",
    description="Select this to start recording and get feedback on your stutters"
)
@limiter.limit("5/minute")
async def stutter_detectionV2(request: Request, file: UploadFile = File(...)):
    return await stutter_service.detect_stutterV2(file)

@stutter_router.post("/upload_file", summary="Upload Audio File", response_class=JSONResponse)
def upload_file(file: UploadFile = File(...)):
    try:
        upload_result = stutter_service.test_upload(file)
        if "error" in upload_result:
            raise HTTPException(status_code=500, detail=upload_result["error"])
        return {
            "filename": upload_result["filename"],
            "filepath": upload_result["filepath"],
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



    
    

    