import json
from pykafka import KafkaClient
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable

from websocket import create_connection

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['test']

try:
    with topic.get_sync_producer() as producer:
        ws = create_connection("wss://ws.blockchain.info/inv")
        ws.send(json.dumps({"op": "unconfirmed_sub"}))

        while True:
            result = json.loads(ws.recv())
            producer.produce(json.dumps(result).encode("utf-8"))


except (SocketDisconnectedError, LeaderNotAvailable) as e:
    producer = topic.get_producer()
    producer.stop()
    print(e)


