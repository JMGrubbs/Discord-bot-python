import toml

config = toml.load("api_config.toml")

API_KEY = config["agent_api"]["api_key"]
