import json
import logging
from confluent_kafka import Producer
from models.state import AgentMessage

logger = logging.getLogger(__name__)

class KafkaEventBus:
    def __init__(self, broker_url: str):
        self.producer = Producer({'bootstrap.servers': broker_url})

    def delivery_report(self, err, msg):
        if err: logger.error(f"Delivery failed: {err}")
        else: logger.debug(f"Delivered to {msg.topic()}")

    def publish_event(self, topic: str, message: AgentMessage):
        payload = message.model_dump_json().encode('utf-8')
        self.producer.produce(topic, value=payload, callback=self.delivery_report)
        self.producer.poll(0)

    def flush(self):
        self.producer.flush()
