import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class TelemetryStore:
    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def ingest(self, topic: str, payload: bytes) -> None:
        text = payload.decode(errors="replace")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {"raw": text}

        record = {
            "topic": topic,
            "data": data,
            "received_at": datetime.now(timezone.utc).isoformat(),
        }
        async with self._lock:
            self._data[topic] = record

    async def latest_all(self) -> Dict[str, Dict[str, Any]]:
        async with self._lock:
            return dict(self._data)

    async def latest_by_topic(self, topic: str) -> Optional[Dict[str, Any]]:
        async with self._lock:
            return self._data.get(topic)


telemetry_store = TelemetryStore()
