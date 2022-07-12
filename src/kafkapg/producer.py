import time
import json
from data_generator import website_data
from kafka import KafkaProducer


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


def producer(kafka_topic, service_uri, ca_path, cert_path, key_path, website_url):

    producer = KafkaProducer(
        bootstrap_servers=service_uri,
        security_protocol="SSL",
        ssl_cafile=ca_path,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
        value_serializer=serializer
    )

    # Collect metrics periodically
    while True:
        # Get website data
        check_website = website_data(website_url)
        print(check_website)
        # Send it to topic
        producer.send(kafka_topic, check_website)

        # Sleep for 3 mins
        time.sleep(180)


if __name__ == '__main__':
    producer()
