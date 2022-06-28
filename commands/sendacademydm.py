from nextcord.ext import commands
import nextcord
from nextcord import Interaction
import utils.info as info
import utils.utilities as utils
import asyncio

class AcademyDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="sendacademydm", description="Sends a DM to the academy", guild_ids=[int(info.f1abeezID),  int(info.f2abeezID), int(info.testServerID), int(info.f1abeezEsportsID)])
    async def sendAcademyDM(self, interaction: Interaction):
        if(utils.check_roles(interaction.user.roles, ["Admin", "Moderator"])):
            await interaction.response.defer()
            role: nextcord.Role = interaction.guild.get_role(info.get_roleID(interaction.guild_id, "academyRole"))
            inboxChannel: nextcord.TextChannel = self.bot.get_channel(870004492639301692)
            members: list[nextcord.Member] = interaction.guild.members
            members = [member for member in members if role in member.roles]
            count: int = 0
            message: nextcord.Message = await interaction.send("Sending DMs to Academy...")
            for member in members:
                count += 1
            try:
                await member.send(f"Hello {member.name},\n\nThis is an automated message we are sending out to all academy drivers as some of you have been here for a long time and haven’t gotten in yet.\n\nWe want to get you in when the next game is out so you can experience all the great stuff we have in store for it and clear out the academy section as well!\n\nIf you’d like to get in please reach out either to F1AB Azzer (Azzer175nh)#8290 or  GeorgeP31#6289 and they’ll get you all sorted!\n\nThank you,\nF1ABEEZ Admin Team.")
                await inboxChannel.send(content=f"Sending DMs to Academy... - last message to **{member.name}** - **status: {count}/{len(members)}**")
                await asyncio.sleep(300)
            except Exception as e:
                await inboxChannel.send(content=f"Sending DMs to Academy... - last message to **{member.name}** failed - **status: {count}/{len(members)}**")
                print("academy dm:")
                print(e)
            await inboxChannel.send(content="Sending DMs to Academy... - **done!**")
        else:
            await interaction.send("You do not have permission to use this command!")

def setup(bot):
    bot.add_cog(AcademyDM(bot))