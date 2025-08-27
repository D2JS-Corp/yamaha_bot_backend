import paho.mqtt.client as mqtt
from typing import Any

from core.config import settings

class MQTTClient:
    def __init__(self) -> None:
        self.client = mqtt.Client()

    def connect(self) -> None:
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
        self.client.loop_start()

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: dict[str, int], rc: int) -> None:
        print("Connected to MQTT broker")
        client.subscribe(settings.MQTT_TOPIC)

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        payload = msg.payload.decode()
        print(f"Received: {payload}")

mqtt_client = MQTTClient()
