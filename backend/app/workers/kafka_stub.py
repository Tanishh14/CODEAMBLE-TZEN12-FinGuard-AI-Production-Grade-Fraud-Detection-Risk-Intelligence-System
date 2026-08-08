"""Kafka producer/consumer lightweight stubs for streaming integration."""
import logging

log = logging.getLogger("finguard.kafka")


class KafkaProducerStub:
    def __init__(self, brokers: str = "localhost:9092"):
        self.brokers = brokers

    async def produce(self, topic: str, message: dict):
        log.info("Kafka produce stub to %s: %s", topic, message)


class KafkaConsumerStub:
    def __init__(self, brokers: str = "localhost:9092"):
        self.brokers = brokers

    async def start(self):
        log.info("Kafka consumer stub start")

    async def stop(self):
        log.info("Kafka consumer stub stop")


producer = KafkaProducerStub()
consumer = KafkaConsumerStub()
