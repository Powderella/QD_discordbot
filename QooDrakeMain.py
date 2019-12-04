from discord.ext import commands
import os
import traceback

from config import DISCORD_TOKEN
bot = commands.Bot(command_prefix='?')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def hello(ctx):
    await ctx.send('hello,{ctx.author}')


bot.run(DISCORD_TOKEN)