import os

try:
    import config
except ImportError:
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
else:
    DISCORD_TOKEN = config.DISCORD_TOKEN

DB_DIR = "./db/shelve"
