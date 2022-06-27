import json

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
while True:
    try:
        m = r.set("media_pipe", json.dumps(["pombe"]))
        print(m)
    except Exception as e:
        print(e)

    # print(r)
