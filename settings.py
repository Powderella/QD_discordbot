import os

try:
    import config
except ImportError:
    QIITA_TOKEN = os.environ["QIITA_TOKEN"]
    DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
    DISCORD_DEFAULT_CHANNEL = int(os.environ["DISCORD_DEFAULT_CHANNEL"])
    DISCORD_OWNER_ID = int(os.environ["DISCORD_OWNER_ID"])
    DROPBOX_TOKEN = os.environ["DROPBOX_TOKEN"]
else:
    QIITA_TOKEN = config.QIITA_TOKEN
    DISCORD_TOKEN = config.DISCORD_TOKEN
    DISCORD_DEFAULT_CHANNEL = config.DISCORD_DEFAULT_CHANNEL
    DISCORD_OWNER_ID = config.DISCORD_OWNER_ID
    DROPBOX_TOKEN = config.DROPBOX_TOKEN


QIITA_TAG_URL = "https://qiita.com/api/v2/tags/{}/items"
QIITA_LOOP_TIME = 5.0   # minute

DB_DIR = "./db/shelve"

LOCAL_PATH_DBFILE = "./db.zip"
LOCAL_PATH_DBFOLDER = "db"

PATH_DROPBOX = "/db.zip"
UPLOAD_LOOP_TIME = 10.0  # minute