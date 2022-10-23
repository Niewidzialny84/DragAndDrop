from dotenv import dotenv_values

config = dotenv_values("shared/.env")

DISCORD_WEBHOOK = config["DISCORD_WEBHOOK"]
LOGIN = config["LOGIN"].encode("utf-8")
PASSWORD = config["PASSWORD"].encode("utf-8")
