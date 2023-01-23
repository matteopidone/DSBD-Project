from kafka import KafkaProducer
import json

class MessageProducerClass:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(0, 10, 1),
            acks='all',
            retries = 3
        )


    def send_msg(self, msg, partition_key):
        print("sending message...")
        try:
            future = self.producer.send(self.topic, value=msg, partition=partition_key, key='Metric' + partition_key)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex