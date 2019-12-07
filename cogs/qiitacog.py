from discord.ext import commands, tasks
import discord
import datetime
import shelve
import requests

from lib import qiita

from settings import DISCORD_DEFAULT_CHANNEL, QIITA_LOOP_TIME, DB_DIR


class QiitaCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.defaultChannel = None
        self.defaultDatetime = datetime.datetime.strptime("1990-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.printQiitaArticleLatest.start()
        with shelve.open(DB_DIR) as db:
            self.qiita_tags = db.get("qiita_tags", list())
            self.articlesCreatedAt = db.get("articles_createdat", dict())

    def cog_unload(self):
        self.printQiitaArticleLatest.cancel()
    
    @tasks.loop(minutes=QIITA_LOOP_TIME)
    async def printQiitaArticleLatest(self):

        try:
            qtapi = qiita.QiitaTagAPI()
            articlesInfo = qtapi.getArticlesFromTags(self.qiita_tags, query=["title", "url", "created_at"])
        except requests.exceptions.HTTPError as e:
            print(e)

        for tag in self.qiita_tags:            
            # 読み取った最新の記事の作られた時間を保存
            latestArticle = datetime.datetime.strptime(articlesInfo[tag][0]["created_at"],
                                                    "%Y-%m-%dT%H:%M:%S+09:00")
            # 初回記事だった場合タグを先頭につけるために最初のループを判断する
            first_tagarticles_loop = True

            for articleInfo in articlesInfo[tag]:
                atricleCreatedAt = datetime.datetime.strptime(articleInfo["created_at"], "%Y-%m-%dT%H:%M:%S+09:00")
                
                if (self.articlesCreatedAt[tag] >= atricleCreatedAt):
                    break
                if first_tagarticles_loop:
                    msg = tag
                    first_tagarticles_loop = False
                msg += f'tag\n{articleInfo["title"]}\n{articleInfo["url"]}' 
                await self.defaultChannel.send(msg)fo
            self.articlesCreatedAt[tag] = latestArticle

        self._check_tag()


    @printQiitaArticleLatest.before_loop
    async def beforePrintQiitaArticleLatest(self):
        await self.bot.wait_until_ready()
        self.defaultChannel = self.bot.get_channel(DISCORD_DEFAULT_CHANNEL)


    """
    QIITA TAG COMMAND AREA
    """   
    @commands.group()
    async def qiita(self, ctx):
        """
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドを入力してください。")

    @qiita.command()
    async def add(self, ctx, tag):
        if tag in self.qiita_tags:
            await ctx.send(f"すでに{tag}は存在しています。")
            return
        
        self.qiita_tags.append(tag)
        self.articlesCreatedAt[tag] = self.defaultDatetime
        message = f"QIITA_TAGSに{tag}が追加されました。"
        print(message)
        await ctx.send(message)
        self._check_tag()
        await ctx.send(f"\nCurrent tags:{self.qiita_tags}")
    
    @qiita.command()
    async def remove(self, ctx, tag):
        if tag not in self.qiita_tags:
            await ctx.send(f"{tag}は存在しません。")
            return

        self.qiita_tags.remove(tag)
        message = f"QIITA_TAGSに{tag}が削除されました。"
        print(message)
        await ctx.send(message)
        self._check_tag()
        await ctx.send(f"\nCurrent tags:{self.qiita_tags}")

    
    @qiita.command()
    async def check(self, ctx):
        self._check_tag()
        await ctx.send(f"\nCurrent tags:{self.qiita_tags}")

    
    def _check_tag(self):
        with shelve.open(DB_DIR) as db:
            db["qiita_tags"] = self.qiita_tags
            print(db["qiita_tags"])
            db["articles_createdat"] = self.articlesCreatedAt
            print(db["articles_createdat"])

def setup(bot):
    bot.add_cog(QiitaCog(bot))