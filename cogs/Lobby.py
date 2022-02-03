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

    @nextcord.slash_command(name="lobby",guild_ids=[int(info.testServerID)])
    async def lobby(self, interaction: Interaction, tier: str = SlashOption(name="tier", description="Select your Tier", choices={"Tier 1": "1", "Tier 2": "2", "Tier 3": "3", "Tier 4": "4", "Tier 5": "5", "Tier M": "M", "Tier NA": "NA"})):
        match tier:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case "M":
                pass
            case "NA":
                pass
                    

def setup(bot):
    bot.add_cog(Lobby(bot))