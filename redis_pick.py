import json
from time import sleep
import bpy

import redis

mo = bpy.ops.mesh.primitive_monkey_add()
mo2 = bpy.ops.mesh.primitive_monkey_add()
i = 0
r = redis.StrictRedis(host='localhost', port=6379, db=0)
while True:
    try:
        m = json.loads(r.get("media_pipe"))
        print(m)
        bpy.data.objects["Suzanne"].location = [m * 20 for m in m[0]]
        print(m)
        bpy.data.objects["Suzanne"].keyframe_insert(data_path="location", frame=70 * i)
        print(m)
        bpy.ops.object.constraint_add(type='FOLLOW_TRACK')

        i += 1
        bpy.data.objects["Suzanne.001"].location = [m * 20 for m in m[1]]
        print(m)
        bpy.data.objects["Suzanne.001"].keyframe_insert(data_path="location", frame=70 * i)
        print(m)

        i += 1
        if i * 70 > 250:
            break


    except Exception as e:
        print(e)
        break

    # print(r)
