from kafka import KafkaConsumer
import json
import os

class MessageConsumerClass:
    broker = ""
    topic = ""
    group_id = ""
    logger = None

    def __init__(self, broker, topic, group_id, db_instance):
        self.broker = broker
        self.topic = topic
        self.group_id = group_id
        self.db_instance = db_instance

    def activate_listener(self):
        consumer = KafkaConsumer(
            bootstrap_servers=self.broker,
            group_id=self.group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('ascii')),
            api_version=(0, 10, 1)
        )

        consumer.subscribe(self.topic)
        print("Consumer is listening....")
        try:
            for message in consumer:
                message_received = message.value
                if message_received['type'] == 'statistics' :
                    value = self.db_instance.insert_or_update_stats(metric_name = message_received['name'], values = message_received['values'])
                    print("Update statistics: " + str(value))
                elif message_received['type'] == 'prediction' :
                    value = self.db_instance.insert_or_update_prediction(metric_name = message_received['name'], values = message_received['values'])
                    print("Update prediction: " + str(value))
                elif message_received['type'] == 'metadata' :
                    value = self.db_instance.insert_or_update_metadata(metric_name = message_received['name'], values = message_received['values'])
                    print("Update metadata: " + str(value))
                consumer.commit()
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            consumer.close()


def start_consumers(db) :
    broker = os.environ['KAFKA_BROKER']
    topic = os.environ['KAFKA_TOPIC']
    group_id = 'consumer-1'

    consumer1 = MessageConsumerClass(broker, topic, group_id, db)
    consumer1.activate_listener()

    consumer2 = MessageConsumerClass(broker, topic, group_id, db)
    consumer2.activate_listener()