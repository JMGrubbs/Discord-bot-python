import toml

config = toml.load("api_config.toml")

API_KEY = config["agent_api"]["api_key"]

OPEN_AI_API_KEY = config["openai"]["api_key"]
OPEN_AI_API_SECRET = config["openai"]["organization"]

NAEBLIS_AGENT_ID = config["openai"]["naeblis"]
ALEXANDER_AGENT_ID = config["openai"]["alexander"]
KIRK_AGENT_ID = config["openai"]["kirk"]

REDIS_HOST = config["redis_cache"]["host"]
REDIS_PORT = config["redis_cache"]["port"]
