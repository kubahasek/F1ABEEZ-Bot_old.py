from nextcord.ext import commands
import nextcord
from nextcord import Interaction
import utils.info as info
import utils.utilities as utils

class ClearChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="clearchannel", description="Clears a channel without the pinned messages", guild_ids=[int(info.f1abeezID),  int(info.f2abeezID), int(info.testServerID), int(info.f1abeezEsportsID)])
    async def clearChannel(self, interaction: Interaction):
        if(utils.check_roles(interaction.user.roles, ["Admin", "Moderator"])):
            await interaction.response.defer()
            def check(m: nextcord.Message):
                return m.pinned == False
            await interaction.channel.purge(check=check)
        else:
            await interaction.send("You do not have permission to use this command!")

def setup(bot):
    bot.add_cog(ClearChannel(bot))