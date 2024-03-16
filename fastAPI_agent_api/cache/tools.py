import json

from cache.cache import redis_connection


async def get_set_cache(key=None, callback=None, *args, **kwargs):
    namespace = kwargs.get("namespace")
    print(f"Namespace: {namespace}")
    print(f"Key: {key}")
    async with redis_connection() as rd:
        if namespace == "threads" and key:
            thread = kwargs.get("thread")
            await rd.hset(namespace, mapping={key: json.dumps(thread)})
        elif namespace == "threads" and not key:
            threads = await rd.hgetall(namespace)
            if threads:
                for thread in threads:
                    threads[thread] = json.loads(threads[thread])
                print(threads)
                return threads
            else:
                return {}
