import json
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import redis

from pykafka import KafkaClient
from pykafka.common import OffsetType
from pykafka.exceptions import SocketDisconnectedError


# stores txn rate in redis
def count_txn_rate():
    global r, cnt
    temp = cnt
    cnt = 0
    r.set(str(datetime.datetime.now().strftime("%M:%S")), str(temp), ex=1000)


# redis
r = redis.Redis()

# kafka client
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['test']
consumer = topic.get_simple_consumer(
    auto_offset_reset=OffsetType.LATEST,
    reset_offset_on_start=True
)


# Schedules count_txn_rate() to be run per minute
scheduleRate = BackgroundScheduler()
cnt = 0
scheduleRate.add_job(count_txn_rate, 'cron', second='0')
scheduleRate.start()


try:
    for message in consumer:
        if message is not None:
            cnt += 1
            x = message.value.decode("utf-8")
            jsonVar = json.loads(x)
            r.lpush("transactions", str(jsonVar))
            r.ltrim("transactions", 0, 99)  # storing only last 100 transaction
            print(message.offset)

except SocketDisconnectedError as e:
    consumer = topic.get_simple_consumer()
    # use either the above method or the following:
    consumer.stop()
    consumer.start()


