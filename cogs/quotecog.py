from discord.ext import commands # Bot Commands Frameworkのインポート
import discord
import datetime
from pytz import timezone
import re

class QuoteCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.pattern = r"https://discordapp.com/channels/\d+/\d+/\d+"

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        match = re.findall(self.pattern, message.content)
        if not len(match):
            return

        for m in match:
            quote = await channel.fetch_message(m.split("/")[-1])
            if len(quote.embeds):
                content = m
            else:
                content = quote.content
            embed=discord.Embed(description=content)
            
            embed.set_author(name=quote.author.name, url=quote.author.avatar_url,icon_url=quote.author.avatar_url)
            embed.set_thumbnail(url=message.guild.icon_url)

            # UTCからJSTに変換かつ、文字列化
            jst = message.created_at.astimezone(timezone('Asia/Tokyo'))
            jstStr = jst.strftime("Created at %Y-%m-%d %H:%M:%S")
            embed.set_footer(text=f"via {self.bot.user} • " + jstStr)

            await channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(QuoteCog(bot))