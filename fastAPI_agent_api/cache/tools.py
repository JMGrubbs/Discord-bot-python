import json

from cache.cache import redis_connection


async def get_set_cache(key=None, *args, **kwargs):
    namespace = kwargs.get("namespace")
    # print(f"Namespace: {namespace}")
    # print(f"Key: {key}")
    async with redis_connection() as rd:
        if namespace and key and kwargs.get("obj_type"):
            obj_type = kwargs.get("obj_type")[key]
            # print(f"Object Type: {type(obj_type)} {obj_type}")
            await rd.hset(namespace, mapping={key: json.dumps(obj_type)})
        elif namespace and key:
            obj_type = await rd.hget(namespace, key)
            if obj_type:
                return json.loads(obj_type)
            else:
                return {}
        elif namespace and not key:
            obj_type_list = await rd.hgetall(namespace)
            if obj_type_list:
                for obj_type_el in obj_type_list:
                    obj_type_list[obj_type_el] = json.loads(obj_type_list[obj_type_el])
                return obj_type_list
            else:
                return {}
