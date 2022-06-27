import bpy
import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0)

last1 = None
last2 = None


def worker():
    global last1, last2
    message = r.get('media_pipe')
    print(message)
    if message:
        cor = json.loads(message)
        # print(cor)1

        cor1 = cor[0]
        cor2 = cor[1]

        if last1 and last2:
            cor1 = [i * 0.4 + j * 0.6 for i, j in zip(last1, cor1)]
            cor2 = [i * 0.4 + j * 0.6 for i, j in zip(last2, cor2)]
        else:
            last1 = cor1
            last2 = cor2

        bpy.data.objects['4'].location = [-cor1[0] - 0.05, 0, -cor1[1]]
        bpy.data.objects['8'].location = [-cor2[0] + 0.05, 0, -cor2[1]]

    return 0.2


bpy.app.timers.register(worker)