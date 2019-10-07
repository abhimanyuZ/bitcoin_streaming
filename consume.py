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
    pref = "r"
    r.set(pref + str(datetime.datetime.now().strftime("%H:%M")), str(temp), ex=3600)


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

# prefix to identify keys related to address and values
pre = "v"

try:
    for message in consumer:
        if message is not None:
            cnt += 1
            x = message.value.decode("utf-8")
            jsonVar = json.loads(x)
            r.lpush("transactions", json.dumps(jsonVar).encode("utf-8"))
            r.ltrim("transactions", 0, 99)  # storing only last 100 transaction
            print(message.offset)

            for i in jsonVar["x"]["out"]:
                if not i["spent"]:
                    # update address value if found already
                    if r.exists(pre + str(i["addr"])):
                        r.set(pre + str(i["addr"]), str(int(i["value"]) + int(r.get(pre + str(i["addr"])))), ex=10800)
                    else:
                        r.set(pre + str(i["addr"]), str(i["value"]), ex=10800)
                else:
                    r.set(pre + str(i["addr"]), str("0"), ex=10800)

except SocketDisconnectedError as e:
    consumer = topic.get_simple_consumer()
    # use either the above method or the following:
    consumer.stop()
    consumer.start()


