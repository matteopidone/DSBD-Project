from kafka import KafkaProducer, KafkaAdminClient
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

    def create_topic(self, num_partitions) :
        admin_client = KafkaAdminClient(bootstrap_servers=self.broker)
        topic_name = self.topic
        replication_factor = 1

        new_topic = {
            "topic": topic_name,
            "num_partitions": num_partitions,
            "replication_factor": replication_factor,
            "configs": {}
        }

        admin_client.create_topics([new_topic])


    def send_msg(self, msg, partition = 0):
        print("sending message... at the partition " + str(partition))
        try:
            future = self.producer.send(self.topic, key=str(partition).encode(), value=msg)
            self.producer.flush()
            future.get(timeout=60)
            print("message sent successfully...")
            return {'status_code':200, 'error':None}
        except Exception as ex:
            return ex