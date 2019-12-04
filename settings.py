import os

try:
    import config
except ImportError:
    QIITA_TOKEN = os.environ["QIITA_TOKEN"]
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
    DISCORD_DEFAULT_CHANNEL = int(os.environ["DISCORD_DEFAULT_CHANNEL"])
else:
    QIITA_TOKEN = config.QIITA_TOKEN
    DISCORD_TOKEN = config.DISCORD_TOKEN
    DISCORD_DEFAULT_CHANNEL = config.DISCORD_DEFAULT_CHANNEL

QIITA_TAG_URL = "https://qiita.com/api/v2/tags/{}/items"
QIITA_LOOP_TIME = 5.0   # minute

DB_DIR = "./db/shelve"
