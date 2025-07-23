# src/middleware/performance_monitor_middleware.py
import time
import psutil
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

logger = logging.getLogger("performance")

class PerformanceMonitorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.process = psutil.Process(os.getpid())

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        start_mem = self.process.memory_info().rss
        start_cpu = self.process.cpu_percent(interval=None)

        response: Response = await call_next(request)

        end_time = time.perf_counter()
        end_mem = self.process.memory_info().rss
        end_cpu = self.process.cpu_percent(interval=None)

        logger.info(f"[Performance] {request.method} {request.url.path} - "
                    f"Time: {end_time - start_time:.2f}s | "
                    f"CPU: {end_cpu - start_cpu:.2f}% | "
                    f"Memory: {(end_mem - start_mem) / (1024 * 1024):.2f} MB")

        return response
