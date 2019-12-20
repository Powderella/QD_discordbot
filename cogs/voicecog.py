from discord.ext import commands # Bot Commands Frameworkのインポート

class VoiceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx):
        """vc connect
        
        """
        vc = ctx.voice_client
        botVoiceclients = [vc.channel for vc in self.bot.voice_clients] 
        if not vc is None and not vc.channel in botVoiceclients:
            vc = await vc.channel.connect()
            vc.stop()

    
    @commands.command()
    async def disconnect(self, ctx):
        """vc disconnect

        """
        vc = ctx.message.guild.voice_client
        if vc.is_connected():
            await vc.disconnect()

        
def setup(bot):
    bot.add_cog(VoiceCog(bot))
