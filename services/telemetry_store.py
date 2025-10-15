import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional, List


class TelemetryStore:
    def __init__(self) -> None:
        self._data: Dict[str, List[Dict[str, Any]]] = {}  # Cambiar a lista por topic
        self._lock = asyncio.Lock()
        self._max_records_per_topic = 12

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
            if topic not in self._data:
                self._data[topic] = []
            
            # Agregar nuevo registro
            self._data[topic].append(record)
            
            # Mantener solo los últimos 12 registros
            if len(self._data[topic]) > self._max_records_per_topic:
                self._data[topic] = self._data[topic][-self._max_records_per_topic:]

    async def topic(self, topic: str) -> Optional[List[Dict[str, Any]]]:
        """Obtiene los últimos registros de un tópico (máximo 12)"""
        async with self._lock:
            return self._data.get(topic, [])[:]  # Retorna copia de la lista

    async def latest_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obtiene todos los tópicos con sus últimos registros"""
        async with self._lock:
            return {topic: records[:] for topic, records in self._data.items()}

    async def latest_by_topic(self, topic: str) -> Optional[Dict[str, Any]]:
        """Obtiene el registro más reciente de un tópico"""
        async with self._lock:
            records = self._data.get(topic, [])
            return records[-1] if records else None

    async def topic_count(self, topic: str) -> int:
        """Obtiene la cantidad de registros para un tópico"""
        async with self._lock:
            return len(self._data.get(topic, []))

    async def clear_topic(self, topic: str) -> None:
        """Limpia todos los registros de un tópico"""
        async with self._lock:
            if topic in self._data:
                self._data[topic] = []


telemetry_store = TelemetryStore()
