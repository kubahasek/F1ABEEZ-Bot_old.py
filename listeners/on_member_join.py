import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
import logging
import utils.info as info

class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        serverID = member.guild.id
        if(member.guild.id == int(info.f1abeezID)):
            role = nextcord.utils.get(member.guild.roles, name="Academy Driver")
            await member.add_roles(role)
        elif(member.guild.id == int(info.f2abeezID)):
            role = nextcord.utils.get(member.guild.roles, name="Academy Driver")
            await member.add_roles(role)
        channel = self.bot.get_channel(info.get_channelID(serverID, "welcomeChannel"))
        if(type(channel) != type(None)):
            if(member.guild.id == int(info.f1abeezID)):
                await channel.send(f"**Welcome {member.mention}**\n\nPlease use this chat if you have any questions and someone will be on hand.\n\nAll the information you need is on <#865379267977412618>")
            elif(member.guild.id == int(info.f2abeezID)):
                await channel.send(f"Welcome to F2ABEEZ!{member.mention}\n\nYour dedicated F2 racing discord community. Please read <#937998062842957824> to get equated with our brand and information then, head over to <#937997355737833482> to get a seat in the next race that suits your pace! Please **put your gamertag into brackets behind your discord name**, thank you!")
        else:
            logging.error("welcomeChannel not found")

def setup(bot):
    bot.add_cog(MemberJoin(bot))