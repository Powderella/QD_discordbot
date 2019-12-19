from discord.ext import commands # Bot Commands Frameworkのインポート
from lib import niconico
import aiohttp

# コグとして用いるクラスを定義。
class VideoCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def connect(self, ctx):
        """connect
        
        """
        await ctx.author.voice.channel.connect()
    
    @commands.command()
    async def disconnect(self, ctx):
        """disconnect

        """
        await ctx.message.guild.voice_client.disconnect()
        
    @commands.command()
    async def niconico(self, ctx, url):
        """ニコニコ動画のDLリンク

        """
        nv = niconico.NiconicoVideo(url)
        async with aiohttp.ClientSession() as session:
            try:
                message = await nv.getDownloadUrl(session)
            except TypeError:
                message = "古い動画です。"
            except ConnectionError:
                message = "通信エラー"
        await ctx.send(message)
        
def setup(bot):
    bot.add_cog(VideoCog(bot))
