from discord.ext import commands, tasks
import discord
import datetime
import shelve
import requests
import re

from lib import qiita

from settings import DISCORD_DEFAULT_CHANNEL, QIITA_LOOP_TIME, DB_DIR


class QiitaCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.defaultChannel = None
        self.favorite = "⭐"
        self.qtapi = qiita.QiitaTagAPI()
        self.defaultDatetime = datetime.datetime.strptime("1990-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.printQiitaArticleLatest.start()
        with shelve.open(DB_DIR) as db:
            self.qiita_tags = db.get("qiita_tags", list())
            self.articlesCreatedAt = db.get("articles_createdat", dict())

    def cog_unload(self):
        self.printQiitaArticleLatest.cancel()
    
    @tasks.loop(minutes=QIITA_LOOP_TIME)
    async def printQiitaArticleLatest(self):
        for tag in self.qiita_tags:
            # 記事取得
            self.qtapi.tag = tag
            articles = await self.qtapi.fetchArticlesFromTag(item_num=10)
            # 読み取った最新の記事の作られた時間を保存
            latestArticle = datetime.datetime.strptime(articles[0]["created_at"],
                                                    "%Y-%m-%dT%H:%M:%S+09:00")
            for article in articles[::-1]:
                atricleCreatedAt = datetime.datetime.strptime(article["created_at"], "%Y-%m-%dT%H:%M:%S+09:00")
                
                if (self.articlesCreatedAt[tag] >= atricleCreatedAt):
                    break
                msg = f'{tag}\n{article["title"]}\n{article["url"]}'
                sentMessage = await self.defaultChannel.send(msg)
                await sentMessage.add_reaction(self.favorite)
            self.articlesCreatedAt[tag] = latestArticle

        self._check_tag()


    @printQiitaArticleLatest.before_loop
    async def beforePrintQiitaArticleLatest(self):
        await self.bot.wait_until_ready()
        self.defaultChannel = self.bot.get_channel(DISCORD_DEFAULT_CHANNEL)
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or not reaction.message.author.bot \
            or not "https://qiita.com" in reaction.message.content:
            
            return

        with shelve.open(DB_DIR) as db:
            msg = reaction.message
            tag = msg.content.split("\n")[0].title()
            try:
                db["fav" + tag].append(msg.id)
            except AttributeError:
                db["fav" + tag] = [msg.id]



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
    async def add(self, ctx, preTag):
        tag = preTag.title()
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
    async def remove(self, ctx, preTag):
        tag = preTag.title()
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
    
    @qiita.command(aliases=["fav"])
    async def show_favorites(self, ctx, tag):
        with shelve.open(DB_DIR) as db:
            ctx.send(str(db["fav"+tag]))

    
    def _check_tag(self):
        with shelve.open(DB_DIR) as db:
            db["qiita_tags"] = self.qiita_tags
            print(db["qiita_tags"])
            db["articles_createdat"] = self.articlesCreatedAt
            print(db["articles_createdat"])

def setup(bot):
    bot.add_cog(QiitaCog(bot))
