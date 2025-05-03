from fastapi import APIRouter


from fastapi.responses import HTMLResponse
from src.calculator.service import CalculatorService
calcService = CalculatorService()
calculator_router = APIRouter()
@calculator_router.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Calculator</title>
        </head>
        <body>
            <h1>Welcome to the Calculator API</h1>
            <p>Use the endpoints to perform calculations.</p>
        </body>
    </html>
    """

@calculator_router.get("/add/{num1}/{num2}")
async def add(num1: int, num2: int):
    result = await calcService.add(num1, num2)
    return {"result": result}