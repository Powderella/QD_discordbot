from discord.ext import commands # Bot Commands Frameworkのインポート
import discord
from lib import niconico
import aiohttp
import asyncio
from lib import utility

# コグとして用いるクラスを定義。
class VideoCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.savePath = "./resource/douga.mp3"

    def _makeEmbedPlayer(self):
        pass

    @commands.group()
    async def niconico(self, ctx):
        """
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドを入力してください。")

    @niconico.command(name="play")
    async def niconicoplay(self, ctx, url):
        url = await self._fetchNiconicoDlLink(url)
        message = await ctx.send("ダウンロード中...")
        async with aiohttp.ClientSession() as session:
            utility.download(session, url, self.savePath, 307200)
        await message.edit(content="ダウンロード完了")

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.savePath))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await message.edit(content="再生中")
        
    @niconico.command(name="link")
    async def niconicolink(self, ctx, url):
        """ニコニコ動画のDLリンク生成
        """
        message = await self._fetchNiconicoDlLink(url)
        await ctx.send(message)
    
    async def _fetchNiconicoDlLink(self, url):
        """
        """
        nv = niconico.NiconicoVideo(url)
        async with aiohttp.ClientSession() as session:
            try:
                message = await nv.getDownloadUrl(session)
            except ConnectionError:
                message = "通信エラー"
        return message

def setup(bot):
    bot.add_cog(VideoCog(bot))
