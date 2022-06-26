from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
import logging
import utils.info as info

class MemberRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        memberName = member.name
        memberRole = member.roles
        channel = self.bot.get_channel(info.get_channelID(member.guild.id, "leavingChannel"))
        profilesChannel = self.bot.get_channel(info.get_channelID(member.guild.id, "profilesChannel"))
        profileMsg = f"{memberName} has left the server\n**Roles:** \n"
        if(type(channel) != type(None)):
            await channel.send(f"**{memberName}** has left the server.")
        else:
            logging.error("leavingChannel not found", exc_info=True)
        if(member.guild.id == int(info.f1abeezID) or member.guild.id == int(info.testServerID)):
            if(type(profilesChannel) != type(None)):
                if(["Full Time Driver", "Reserve Driver"] in memberRole):
                    for role in memberRole:
                        if(role.name != "@everyone"):
                            profileMsg += f"> {role.name}\n"
                    await profilesChannel.send(profileMsg)
            else:
                logging.error("profilesChannel not found", exc_info=True)

def setup(bot):
    bot.add_cog(MemberRemove(bot))