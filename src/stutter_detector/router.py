from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse
from src.stutter_detector.detectorService import DetectorService
stutter_router = APIRouter()
stutter_service = DetectorService()

@stutter_router.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Stutter Detector</title>
        </head>
        <body>
            <h1>Welcome to the Stutter Detector API</h1>
            <p>Use the endpoints to interact with the Stutter Detector service.</p>
        </body>
    </html>
    """

@stutter_router.post("/stutter_detection")
async def stutter_detection():
    return await stutter_service.detect_stutter()
    