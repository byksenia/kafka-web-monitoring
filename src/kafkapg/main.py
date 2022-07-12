import argparse
from os.path import exists

from consumer import consumer
from producer import producer


def check_files_exist(files):
    for path in files:
        if not exists(path):
            raise Exception("File not found at: " + path)


def parameters():
    arguments = argparse.ArgumentParser(description='Python - Kafka application with PostgreSQL integration')

    arguments.add_argument('--kafka_topic', help="Kafka Topic name",
                      required=True)
    arguments.add_argument('--pg_uri', help="PostgreSQL URI",
                      required=True)
    arguments.add_argument('--service_uri', help="Service URI (host:port)",
                      required=True)
    arguments.add_argument('--ca_path', help="Path to project CA certificate",
                      required=True)
    arguments.add_argument('--key_path', help="Path to the Kafka Access Key",
                      required=True)
    arguments.add_argument('--cert_path', help="Path to the Kafka Certificate Key",
                      required=True)
    arguments.add_argument('--website_url', help="Website url for monitoring", required=True)
    arguments.add_argument('--producer', action='store_true', default=False, help="Run Kafka producer example")

    arguments.add_argument('--consumer', action='store_true', default=False, help="Run Kafka consumer example")

    args = arguments.parse_args()
    files = [args.ca_path, args.key_path, args.cert_path]
    check_files_exist(files)

    if args.producer:
        print("Starting producer")
        producer(args.kafka_topic, args.service_uri, args.ca_path, args.cert_path, args.key_path, args.website_url)
    elif args.consumer:
        print("Starting consumer")
        consumer(args.kafka_topic, args.pg_uri, args.service_uri, args.ca_path, args.cert_path, args.key_path)


if __name__ == '__main__':
    parameters()
