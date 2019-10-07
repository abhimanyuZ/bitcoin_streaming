from flask import Flask
from flask_restful import Resource, Api
import redis, json

r = redis.Redis()
app = Flask(__name__)
api = Api(app)


class show_transactions(Resource):
    def get(self):
        dic = {}
        li = [x for x in r.lrange("transactions", 0, -1)]
        inx = 0
        for i in li:
            dic[inx] = json.loads(i.decode("utf-8"))
            inx += 1
        return dic


class transactions_count_per_minute(Resource):
    def get(self):
        try:
            keys = r.keys('r*')
            if b'transactions' in keys: keys.remove(b'transactions')
            keys.sort()
            dic = {}
            for key in keys:
                dic[key.decode("utf-8")[1:]] = r.get(key).decode("utf-8")
            return dic

        except Exception as e:
            return {'Error': e}


class high_value_addr(Resource):
    def get(self):
        return {'hello3': 'world'}


api.add_resource(show_transactions, '/show_transactions', '/')
api.add_resource(transactions_count_per_minute, '/transactions_count_per_minute/')
api.add_resource(high_value_addr, '/high_value_addr')
app.run(debug=True)