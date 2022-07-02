import logging
import nextcord
from nextcord.ext import commands

from app import highlightMenu, reportMenu



class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def on_ready(self):
        logging.info("We have logged in as {0.user}".format(self.bot))
        self.bot.add_view(reportMenu())
        self.bot.add_view(highlightMenu())
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="The F1AB Family 🚀"))

def setup(bot):
    bot.add_cog(Ready(bot))