from nextcord.ext import commands
import utils.info as info
import nextcord
from nextcord import Interaction

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def GetHelpCommand(self):
        embed = nextcord.Embed(title="Help", color=info.color)
        embed.add_field(name=";standings", value="This command gives you a menu to select the tier of which you want to see standings and then it returns them in the channel.", inline=False)
        embed.add_field(name=";calendar", value="This command gives you a selection of the F1 or Nations League calendar and then sends it in the channel.", inline=False)
        embed.add_field(name=";gettickets <gamertag>", value="This command is useful when you don’t know the number of your ticket. The command lists all tickets you’ve been involved (whether you reported it or someone else reported you) and gives you the number of the ticket and the direct link to the website.", inline=False)
        embed.add_field(name=";getappeals <gamertag>", value="This command gets you a list of appeals you've been involeved in (whether you appealed or someone appealed against you) and gives you the number of the appeal, a direct link to the website and the status of the appeal.")
        embed.add_field(name=";ticketdetail <number of ticket>", value="This command gets you the details of ticket you provide. It lists the status, penalty that was awarded and who was involved.", inline=False)
        embed.add_field(name=";incidentreport", value="This command allows you to submit an incident from nextcord. Please read the messages carefully and reply correctly.", inline=False)
        embed.add_field(name=";submitappeal", value="This command allows you to submit an appeal to a decision that has been made by the stewards. Please use ;gettickets before you start submitting it to make sure you know the case number of the incident you want to appeal", inline=False)
        return embed

    @nextcord.slash_command(name="help", description="Shows the help menu", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
    async def HelpCommand(self, interaction: Interaction):
        await interaction.send(embed = self.GetHelpCommand())

def setup(bot):
    bot.add_cog(Help(bot))