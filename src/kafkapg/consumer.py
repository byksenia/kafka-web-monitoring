from kafka import KafkaConsumer
from postgres import db_script


def consumer(kafka_topic, pg_uri, service_uri, ca_path, cert_path, key_path):

    consumer = KafkaConsumer(
        auto_offset_reset='earliest',
        bootstrap_servers=service_uri,
        security_protocol="SSL",
        ssl_cafile=ca_path,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
    )

    # Receiving message from topic
    consumer.subscribe([kafka_topic])
    for message in consumer:
        print(message.value)
        db_script(pg_uri, message.value)


if __name__ == '__main__':
    consumer()
