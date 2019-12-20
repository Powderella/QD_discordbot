from discord.ext import commands, tasks # Bot Commands Frameworkのインポート
import discord
from lib import niconico
import aiohttp
import asyncio
from lib import utility
import time
from mutagen.mp4 import MP4

# コグとして用いるクラスを定義。
class VideoCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.savePath = "./resource/douga.mp4"
        utility.setupDirectory(self.savePath)

    def cog_unload(self):
        self.heartBeat.cancel()

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
        start = time.time()
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            self.heartBeat.start(session)
            await utility.download(session, url, self.savePath, 30720)
            self.heartBeat.cancel()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.savePath))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        
        length = MP4(self.savePath).info.length
        playTime = f"{int(length // 60)}:{int(length % 60)}"
        await message.edit(content=f"再生中.\nダウンロードにかかった時間{time.time() - start:.3f}sec.\n再生時間{playTime}")
        
    @niconico.command(name="link")
    async def niconicolink(self, ctx, url):
        """ニコニコ動画のDLリンク生成
        """
        message = await self._fetchNiconicoDlLink(url)
        await ctx.send(message)
    
    async def _fetchNiconicoDlLink(self, url):
        """
        """
        self.nv = niconico.NiconicoVideo(url)
        async with aiohttp.ClientSession() as session:
            try:
                message = await self.nv.getDownloadUrl(session)
            except ConnectionError:
                message = "通信エラー"
        return message

    #
    #   loop
    #

    @tasks.loop(seconds=35)
    async def heartBeat(self, session):
        print("dokudoku!")
        await self.nv.heartBeat(session)

def setup(bot):
    bot.add_cog(VideoCog(bot))
