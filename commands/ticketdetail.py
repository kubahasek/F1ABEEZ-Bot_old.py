from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord
import utils.notion as nt
import utils.info as info

class TicketDetail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ticketdetail", description="Gets the details for the ticket", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
    async def TicketDetail(self, interaction: Interaction, ticketID: str = SlashOption(name="ticketid", description="The ticket ID to get the details for", required=True)):
        await interaction.response.defer()
        await interaction.send(embed = nt.TicketDetailQuery(ticketID))

def setup(bot):
    bot.add_cog(TicketDetail(bot))