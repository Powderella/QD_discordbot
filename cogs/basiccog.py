from discord.ext import commands # Bot Commands Frameworkのインポート
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
        message = f"こんにちは,{ctx.author}!!"
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
    async def reload_allcogs(self, ctx):
        """
        すべてのこぐのリロード
        """
        all_ok = True
        with shelve.open(DB_DIR) as db:
            loadedCogs = db["cogs"]
        for cog in loadedCogs:
            try:
                self.bot.reload_extension(cog)
            except Exception:
                all_ok = False
                print(f"reload {cog}: FAILED")
                print(Exception)
            else:
                print(f"reload {cog}: SUCCESS")
        if all_ok:
            await ctx.send("リロード完了。")
        else:
            await ctx.send("リロード失敗。")

def setup(bot):
    bot.add_cog(TestCog(bot))