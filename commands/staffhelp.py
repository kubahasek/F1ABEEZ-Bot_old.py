from nextcord.ext import commands
import utils.info as info
import nextcord
from nextcord import Interaction
import utils.utilities as utils

class StaffHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getStaffHelpCommand(self):
        embed = nextcord.Embed(title="Staff Help", color=info.color)
        embed.add_field(name=";lobbytier<tierNumber>", value="Sends the lobby is open message. Enter the tier number instead of <tierNumber>. Options: [1,2,3,4,5,M,NA]", inline=False)
        embed.add_field(name=";readytier<tierNumber>", value="Sends the ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2,3,4,5,M,NA]", inline=False)
        embed.add_field(name=";racetier<tierNumber>", value="Sends the race ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2,3,4,5,M,NA]", inline=False)
        embed.add_field(name=";lobbyf2tier<tierNumber>", value="Sends the lobby is open message. Enter the tier number instead of <tierNumber>. Options: [1,2]")
        embed.add_field(name=";readyf2tier<tierNumber>", value="Sends the ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2]")
        embed.add_field(name=";racef2tier<tierNumber>", value="Sends the race ready up instruction. Enter the tier number instead of <tierNumber>. Options: [1,2]")
        embed.add_field(name=";stewardsdecision <roundNumber>", value="Send the links to respective tier race reports. Enter round number instead of <roundNumber>", inline=False)
        embed.add_field(name=";academymessage", value="Send the academy info message", inline=False)
        embed.add_field(name=";warn <user> <reason>", value="(ADMIN ONLY) - allows to warn a user, sending the warning into the proper channel to keep track.")
        embed.add_field(name=";ban <user> <reason>", value="(ADMIN ONLY) - allows to ban a user, and automatically sends it into the ban channel.", inline=False)
        embed.add_field(name=";racereport <roundNumber>", value="Send the links to respective tier race reports. Enter round number instead of <roundNumber>", inline=False)
        embed.add_field(name=";channelname", value="Provide the channel name separated by - (e.g. this-is-a-channel) and the bot will return the name in the special font", inline=False)
        return embed

    @nextcord.slash_command(name="staffhelp", description="Shows the staff help menu", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
    async def StaffHelpCommand(self, interaction: Interaction):
        await interaction.response.defer()
        if(utils.check_roles(interaction.user.roles, ["Staff"])):
            await interaction.send(embed = self.getStaffHelpCommand())
        else:
            await interaction.send("You do not have permission to use this command!")

def setup(bot):
    bot.add_cog(StaffHelp(bot))