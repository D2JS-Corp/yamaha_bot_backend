import asyncio
import pytest
from unittest.mock import AsyncMock

from yamaha_bot_backend.services.robot_service import RobotService
from yamaha_bot_backend.services.telemetry_store import TelemetryStore
from yamaha_bot_backend.infrastructure.mqtt_async import AsyncMQTTClient


@pytest.fixture
def robot_service():
    return RobotService()


@pytest.fixture
def telemetry_store():
    return TelemetryStore()


@pytest.fixture
def mock_mqtt_client():
    client = AsyncMock(spec=AsyncMQTTClient)
    client._handlers = []
    client.add_message_handler = lambda handler: client._handlers.append(handler)
    return client


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
