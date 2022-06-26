from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
import logging

class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("Command not found")
        logging.error(error)

def setup(bot):
    bot.add_cog(CommandError(bot))