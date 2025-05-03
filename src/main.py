from fastapi import FastAPI
from src.calculator.router import calculator_router
app = FastAPI()
app.include_router(calculator_router)