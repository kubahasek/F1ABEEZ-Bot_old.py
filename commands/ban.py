from nextcord.ext import commands
import nextcord
from nextcord import Interaction, Member, SlashOption
import utils.info as info
import utils.utilities as utils


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ban", description="Bans a user", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
    @commands.has_any_role("Admin")
    async def ban(self, interaction: Interaction, user: Member = SlashOption(name="user", description="The user to ban", required=True), reason: str = SlashOption(name="reason", description="The reason for the ban", required=True)):
        await interaction.response.defer()
        if(utils.check_roles(interaction.user.roles, ["Admin"])):
            member = await interaction.guild.fetch_member(user.id)
            embed = nextcord.Embed(title="A Ban has been issued", color=info.color)
            embed.add_field(name="User", value=member.name, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(info.get_channelID(interaction.guild.id, "banChannel"))
            await channel.send(embed = embed)
            await member.ban(reason = reason)
            await interaction.send(embed = embed)   
        else:
            await interaction.send("You do not have permission to use this command!")

    ## TODO: Add ban database to store bans

def setup(bot):
    bot.add_cog(Ban(bot))