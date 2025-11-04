import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from yamaha_bot_backend.services.logger_service import api_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log de request
        api_logger.info(
            "Request started",
            {
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "")
            }
        )
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log de response exitosa
            api_logger.info(
                "Request completed",
                {
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time": round(process_time, 4),
                    "client_ip": request.client.host if request.client else "unknown"
                }
            )
            
            return response
            
        except Exception as exc:
            process_time = time.time() - start_time
            
            # Log de error
            api_logger.error(
                "Request failed",
                {
                    "method": request.method,
                    "url": str(request.url),
                    "process_time": round(process_time, 4),
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc)
                },
                exc_info=True
            )
            raise