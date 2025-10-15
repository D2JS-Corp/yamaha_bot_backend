from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings): # pylint: disable=too-few-public-methods
    PROJECT_NAME: str = "Museum Robot API"
    API_V1_PREFIX: str = "/api/v1"

    # MQTT (async con gmqtt)
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_CLIENT_ID: str = "museum-admin-api"
    MQTT_TOPICS: List[str] = [
        "ros2/battery",
        "ros2/dock",
        "ros2/velocity",
        "ros2/goal",
        "ros2/position"
    ]
    
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    MQTT_QOS: int = 1

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
