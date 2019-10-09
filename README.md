# Bitcoin Transaction Streaming App

A streaming application for realtime bitcoin transactions using Kafka, Redis and Flask<br><br>
It receives the stream of bitcoin transaction data from this [API](https://www.blockchain.com/api/api_websocket). Transaction log is streamed to kafka where it's analyzed in realtime.
Transactions are consumed from a kafka consumer and only transactions made in the last 3 hours are stored in Redis for analysis.
A REST API shows the details related to transcations.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites


* [Python 3.6](https://www.python.org/downloads/)
* [Redis](https://redis.io/topics/quickstart)
* [Kafka](https://kafka.apache.org/quickstart)
* Python3-pip   ```sudo apt-get install python3-pip```



### Installing


* Clone the repo and navigate into repo's directory
* Fire up your terminal and enter this command:
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



## API Endpoints

```
http://127.0.0.1:5000/show_transactions
```
Displays latest 100 transactions in JSON format

```
http://127.0.0.1:5000/transactions_count_per_minute/{minute_value}
```
Display number of transactions per minute for the given minute_value.
If {minute_value} is not mentioned, number of transactions per minute for the last hour will be displayed.

```
http://127.0.0.1:5000/high_value_addr
```
Displays the bitcoin addresses which has the most aggregate value in transactions in the last 3 hours.




## Built With

* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) - The web framework used for API
* [Kafka](https://kafka.apache.org/quickstart) - Streaming platform
* [Redis](https://redis.io/topics/quickstart) - Used to store transactions and related details


