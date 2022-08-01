# kafka-web-monitoring

Project monitors website availability over the network, produces metrics about this and passes these events through an Kafka instance into an PostgreSQL database.

### To produce metrics about website availability:

```
python .\main.py --kafka_topic "TOPIC_NAME" --pg_uri "PG_URI" --service_uri "SERVICE_URI" --ca_path "PATH_TO_CA.PEM" --key_path "PATH_TO_SERVICE.KEY" --cert_path "PATH_TO_SERVICE.CERT" --website_url "URL" --producer
```

### To consume metrics about website availability:

```
python .\main.py --kafka_topic "TOPIC_NAME" --pg_uri "PG_URI" --service_uri "SERVICE_URI" --ca_path "PATH_TO_CA.PEM" --key_path "PATH_TO_SERVICE.KEY" --cert_path "PATH_TO_SERVICE.CERT" --website_url "URL" --consumer
```

### To test project:

```
python .\mytest.py "PG_URI" "URL"
```
