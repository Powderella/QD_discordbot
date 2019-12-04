from discord.ext import commands, tasks
import datetime
import shelve
import requests

from lib import qiita

from settings import DISCORD_DEFAULT_CHANNEL, QIITA_LOOP_TIME, DB_DIR


class QiitaCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot        
        self.printQiitaArticleLatest.start()
        self.defaultChannel = None
        self.index = 0

    @tasks.loop(minutes=QIITA_LOOP_TIME)
    async def printQiitaArticleLatest(self):
        await self.defaultChannel.send(str(self.index))
        self.index += 1


    @printQiitaArticleLatest.before_loop
    async def beforePrintQiitaArticleLatest(self):
        await self.bot.wait_until_ready()
        self.defaultChannel = self.bot.get_channel(DISCORD_DEFAULT_CHANNEL)

def setup(bot):
    bot.add_cog(QiitaCog(bot))