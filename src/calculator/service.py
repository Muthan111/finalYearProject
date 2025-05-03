import asyncio
class CalculatorService:
    def __init__(self):
        self.result = 0

    async def add(self, a, b):
        await asyncio.sleep(0)  # Simulate async behavior
        self.result = a + b
        return self.result
    
    def subtract(self, a, b):
        self.result = a - b
        return self.result
    

    def multiply(self, a, b):
        self.result = a * b
        return self.result
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        self.result = a / b
        return self.result