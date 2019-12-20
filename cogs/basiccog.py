from discord.ext import commands # Bot Commands Frameworkのインポート
import discord
import os
import requests

from settings import DISCORD_DEFAULT_CHANNEL

# コグとして用いるクラスを定義。
class BasicCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def hello(self, ctx):
        """
        応答コマンド
        """
        print(os.listdir("./db/"))
        message = f"こんにちは,{ctx.author}"
        await ctx.send(message)

    @commands.command(hidden=True, aliases=["cog"])
    async def reloadcog(self, ctx, cogName):
        """
        こぐのリロード
        """
        message = (f"コグ{cogName}をリロードします。")
        await ctx.send(message)
        try:
            self.bot.reload_extension(cogName)
            message = f"リロード完了。"
        except Exception as e:
            print(e)
            message = f"リロードできませんでした。"
        finally:
            await ctx.send(message)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def kill(self, ctx):
        """
        ぼっと殺害事件
        """
        print("kill bot")
        await self.bot.logout()
    
    @commands.command(aliases=["game"])
    async def changegame(self, ctx, game):
        game = discord.Game(game)
        await self.bot.change_presence(activity=game)

    @commands.command()
    async def trans(self, ctx, *text):
        target_url = "https://script.google.com/macros/s/AKfycbzX-3H38aJUBIVhPxiPwfJg7TlRWhOpFwW7gOD0MNH1nk97knAF/exec"
        params = {"text":" ".join(text), "source":"en", "target":"ja"}

        req = requests.get(target_url, params=params)
        await ctx.send(req.text)
    
def setup(bot):
    bot.add_cog(BasicCog(bot))