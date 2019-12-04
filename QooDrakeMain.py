from discord.ext import commands
import discord
import traceback
import os
import shelve

from settings import DISCORD_TOKEN, DB_DIR

cogs = os.listdir("./cogs/")

INITIAL_COGS = ["cogs." + cog.strip(".py") for cog in cogs if cog.endswith(".py")]

if not os.path.exists("./db/"):
    os.makedirs("./db/")
with shelve.open(DB_DIR) as db:
    db["cogs"] = INITIAL_COGS

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

if __name__ == "__main__":
    bot = QooDrakeMain(command_prefix="?")
    bot.run(DISCORD_TOKEN)