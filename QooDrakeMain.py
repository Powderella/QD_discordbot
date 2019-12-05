from discord.ext import commands
import discord
import traceback
import os
import shelve

from settings import DISCORD_TOKEN, DISCORD_OWNER_ID, DROPBOX_TOKEN, LOCAL_PATH_DBFILE, LOCAL_PATH_DBFOLDER, PATH_DROPBOX

# cogの名前の読み込みと、dbフォルダがなかった時に作る
cogs = os.listdir("./cogs/")

if not os.path.exists("./db/"):
    import dropbox
    import zipfile

    os.makedirs("./db/")

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    dbx.users_get_current_account()
    try:
        dbx.files_download_to_file(LOCAL_PATH_DBFILE, PATH_DROPBOX)
    except Exception:
        print(Exception)
    else:
        with zipfile.ZipFile(LOCAL_PATH_DBFILE) as extract_zf:
            extract_zf.extractall(LOCAL_PATH_DBFOLDER)


INITIAL_COGS = ["cogs." + cog.strip(".py") for cog in cogs if cog.endswith(".py")]

class QooDrakeMain(commands.Bot):
    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print("opus lib is loaded :", discord.opus.is_loaded())
        self.owner_id = DISCORD_OWNER_ID

if __name__ == "__main__":
    bot = QooDrakeMain(command_prefix="?")
    bot.run(DISCORD_TOKEN)