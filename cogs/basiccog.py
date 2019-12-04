rom discord.ext import commands # Bot Commands Frameworkのインポート
import discord
import shelve

from settings import DB_DIR

# コグとして用いるクラスを定義。
class TestCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def hello(self, ctx):
        """
        応答コマンド
        """
        message = f"こんにちは,{ctx.author}"
        await ctx.send(message)

def setup(bot):
    bot.add_cog(BasicCog(bot))