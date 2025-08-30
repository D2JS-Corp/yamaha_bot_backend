import asyncio
from typing import Awaitable, Callable, List

from gmqtt import Client as GMQTTClient
from core.config import settings

MessageHandler = Callable[[str, bytes], Awaitable[None]]

class AsyncMQTTClient:
    def __init__(self) -> None:
        self.client = GMQTTClient(client_id=settings.MQTT_CLIENT_ID)
        if settings.MQTT_USERNAME:
            self.client.set_auth_credentials(settings.MQTT_USERNAME, settings.MQTT_PASSWORD or "")

        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.on_subscribe = self._on_subscribe

        self._handlers: List[MessageHandler] = []
        self._connected = asyncio.Event()
        self._stop = False

    def add_message_handler(self, handler: MessageHandler) -> None:
        self._handlers.append(handler)
    
    async def connect(self) -> None:
        attempt = 0
        while not self._stop:
            try:
                await self.client.connect(
                    host=settings.MQTT_BROKER_HOST,
                    port=settings.MQTT_BROKER_PORT,
                    keepalive=60
                )

                await self._connected.wait()
                return
            except Exception as exc:
                wait = min(30, 2 ** attempt)
                print(f"[MQTT] Conexión fallida ({exc}). Reintentando en {wait}s...")
                await asyncio.sleep(wait)
                attempt += 1
            
    async def disconnect(self) -> None:
        self._stop = True
        try:
            await self.client.disconnect()
        except Exception as exc:
            print(f"[MQTT] Error al desconectar: {exc}")

    # ---------- Callbacks de gmqtt ----------

    def _on_connect(self, client, flags, rc, properties) -> None:
        print("[MQTT] Conectado ✓")
        for topic in settings.MQTT_TOPICS:
            client.subscribe(topic, qos=settings.MQTT_QOS)
            print(f"[MQTT] Suscrito a: {topic} (QoS={settings.MQTT_QOS})")
        self._connected.set()

    def _on_message(self, client, topic, payload, qos, properties) -> None:
        # Ejecuta handlers sin bloquear el hilo del loop
        for handler in self._handlers:
            coro = handler(topic, payload)
            if asyncio.iscoroutine(coro):
                asyncio.create_task(coro)

    def _on_subscribe(self, client, mid, qos, properties) -> None:
        pass  # opcional: logs o métricas

    def _on_disconnect(self, client, packet, exc=None) -> None:
        self._connected.clear()
        msg = f"[MQTT] Desconectado. exc={exc!r}" if exc else "[MQTT] Desconectado."
        print(msg)

mqtt = AsyncMQTTClient()