from nextcord.ext import commands
import nextcord
from nextcord import Interaction, SlashOption
import utils.info as info
import utils.utilities as utils

class ChannelName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="channelname", description="Gets the channel name in correct font", guild_ids=[int(info.f1abeezID),  int(info.f2abeezID), int(info.testServerID), int(info.f1abeezEsportsID)])
    async def channelName(self, interaction: Interaction, channelName: str = SlashOption(name="channelname", description="The channel name", required=True)):
        await interaction.response.defer()
        if(utils.check_roles(interaction.user.roles, ["Admin", "Moderator"])):
            nameDic = {"a": "ᴀ","b": "ʙ", "c": "ᴄ", "d":  "ᴅ", "e": "ᴇ", "f":"ꜰ", "g": "ɢ", "h":"ʜ", "i":"ɪ", "j":"ᴊ", "k":"ᴋ", "l":"ʟ", "m":"ᴍ", "n": "ɴ", "o": "ᴏ", "p":"ᴘ", "q":"Q", "r":"ʀ", "s":"ꜱ", "t":"ᴛ", "u":"ᴜ", "v":"ᴠ", "w":"ᴡ", "x":"x", "y":"ʏ", "z":"ᴢ", "-":"-", "0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9", "-": "-", " ": "-"}
            returnName = ""
            for i in range(len(channelName)):
                char = channelName[i].lower()
                returnName += nameDic.get(char)
            await interaction.send("︱" + returnName)
        else:
            await interaction.send("You do not have permission to use this command!")

def setup(bot):
    bot.add_cog(ChannelName(bot))