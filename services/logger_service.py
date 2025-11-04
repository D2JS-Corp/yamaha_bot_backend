import logging
from typing import Dict, Any, Optional


class LoggerService:
    def __init__(self, name: str = "yamaha_bot_backend"):
        self.logger = logging.getLogger(name)
    
    def debug(self, message: str, extra_fields: Optional[Dict[str, Any]] = None) -> None:
        self._log("DEBUG", message, extra_fields)
    
    def info(self, message: str, extra_fields: Optional[Dict[str, Any]] = None) -> None:
        self._log("INFO", message, extra_fields)
    
    def warning(self, message: str, extra_fields: Optional[Dict[str, Any]] = None) -> None:
        self._log("WARNING", message, extra_fields)
    
    def error(self, message: str, extra_fields: Optional[Dict[str, Any]] = None, exc_info: bool = True) -> None:
        self._log("ERROR", message, extra_fields, exc_info)
    
    def critical(self, message: str, extra_fields: Optional[Dict[str, Any]] = None) -> None:
        self._log("CRITICAL", message, extra_fields)
    
    def _log(self, level: str, message: str, extra_fields: Optional[Dict[str, Any]] = None, exc_info: bool = False) -> None:
        extra = {}
        if extra_fields:
            extra = {"extra_fields": extra_fields}
        
        if level == "DEBUG":
            self.logger.debug(message, extra=extra, exc_info=exc_info)
        elif level == "INFO":
            self.logger.info(message, extra=extra, exc_info=exc_info)
        elif level == "WARNING":
            self.logger.warning(message, extra=extra, exc_info=exc_info)
        elif level == "ERROR":
            self.logger.error(message, extra=extra, exc_info=exc_info)
        elif level == "CRITICAL":
            self.logger.critical(message, extra=extra, exc_info=exc_info)


# Loggers específicos
main_logger = LoggerService("yamaha_bot_backend.main")
mqtt_logger = LoggerService("yamaha_bot_backend.mqtt")
robot_logger = LoggerService("yamaha_bot_backend.robot")
api_logger = LoggerService("yamaha_bot_backend.api")