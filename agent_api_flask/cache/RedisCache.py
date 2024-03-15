import redis
import json

# Connect to the Redis server
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)


def store_message(message_id, message_data):
    # Store the message in Redis with an expiration time of 1 hour (3600 seconds)
    redis_client.setex(message_id, 3600, json.dumps(message_data))


def get_message(message_id):
    # Retrieve a message from Redis
    message_json = redis_client.get(message_id)
    if message_json:
        return json.loads(message_json)
    else:
        return None


def get_all_messages():
    # Get all keys in the Redis cache
    all_keys = redis_client.keys("*")

    # Initialize a list to store the retrieved messages
    messages = []

    # Iterate through all keys and retrieve their values
    for key in all_keys:
        message_json = redis_client.get(key)
        if message_json:
            messages.append(json.loads(message_json))

    return messages
