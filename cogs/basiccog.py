from discord.ext import commands # Bot Commands Frameworkのインポート
import discord

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
        message = f"こんにちは,{ctx.author}"
        await ctx.send(message)

    @commands.command()
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

    @commands.command()
    async def kill(self, ctx):
        """
        ぼっと殺害事件
        """
        print("kill bot")
        await self.bot.logout()
    
    @commands.command()
    @commands.is_owner()
    async def change_game(self, ctx, game):
        game = discord.Game(game)
        await self.bot.change_presence(activity=game)

    
def setup(bot):
    bot.add_cog(BasicCog(bot))