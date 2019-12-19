from discord.ext import commands # Bot Commands Frameworkのインポート
import niconico
import aiohttp

# コグとして用いるクラスを定義。
class VideoCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def niconico(self, ctx, url):
        """ニコニコ動画のDLリンク

        """
        nv = niconico.NiconicoVideo()
        async with aiohttp.ClientSession() as session:
            url = await nv.getDownloadUrl(session)
        await ctx.send(url)
        
def setup(bot):
    bot.add_cog(VideoCog(bot))