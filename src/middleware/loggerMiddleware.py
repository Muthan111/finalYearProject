from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Response
import logging
from src.utils.logger import logger
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Unhandled error: {str(e)}")
            raise e

        logger.info(f"Response status: {response.status_code}")
        return response
