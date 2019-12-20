from discord.ext import commands # Bot Commands Frameworkのインポート

class VoiceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx):
        """vc connect
        
        """
        vc = ctx.author.voice
        botVoiceChannels = [vc.channel for vc in self.bot.voice_clients] 
        if vc is None or vc.channel in botVoiceChannels:
            return
        vc = await vc.channel.connect()
    
    @commands.command()
    async def disconnect(self, ctx):
        """vc disconnect

        """
        vc = ctx.voice_client
        if vc is None:
            return
        if vc.is_connected():
            await vc.disconnect()
    
    @commands.command()
    async def pause(self, ctx):
        """
        """
        vc = ctx.voice_client
        if vc is None:
            return
        if vc.is_playing():
            vc.pause() 

    @commands.command()
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc is None:
            return
        if vc.is_paused():
            vc.resume()
    
    @commands.command()
    async def stop(self, ctx):
        vc = ctx.voice_client
        if vc is None:
            return
        if vc.is_playing():
            vc.stop()
        
def setup(bot):
    bot.add_cog(VoiceCog(bot))
