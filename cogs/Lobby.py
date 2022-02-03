from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands
import nextcord
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import utils.info as info

class Lobby(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(naemguild_ids=[int(info.testServerID)])
    async def lobby(self, interaction: Interaction):
        await interaction.response.send_message("This is the lobby")

def setup(bot):
    bot.add_cog(Lobby(bot))