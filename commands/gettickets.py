from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord
import utils.notion as nt
import utils.info as info

class GetTickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="gettickets", description="Gets the tickets for the gamertag", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
    async def GetTickets(self, interaction: Interaction, gamertag: str = SlashOption(name="gamertag", description="The gamertag to get the tickets for", required=True)):
        await interaction.response.defer()
        await interaction.send(embed=nt.queryTickets(gamertag))

def setup(bot):
    bot.add_cog(GetTickets(bot))