# Bitcoin Transaction Streaming App

A streaming application for realtime bitcoin transactions using Kafka, Redis and Flask

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites


```
Python 3.6
Kafka
Redis
```

### Installing


After cloning the repo, fire up your terminal and enter these commands:
```
pip3 install -r requirements.txt
```
If installation finishes successfully, you are good to go.



## Deployment

Fire up your terminals

Start zookeeper and then kafka server
```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

Create a kafka topic named "test"
```
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
```

List the topics to verify "test" is created
```
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Start Redis server by entering the following command on terminal
```
redis-server
```

And finally run the producer.py, consumer.py and then myapi.py
```
python3 producer.py
python3 consumer.py
python3 myapi.py
```

## Built With

* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) - The web framework used for API
* [Kafka](https://kafka.apache.org/quickstart) - Streaming platform
* [Redis](https://rometools.github.io/rome/) - Used to store transactions and related details


