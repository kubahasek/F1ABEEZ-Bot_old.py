from discord import SelectOption
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands
import nextcord
import logging
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import utils.info as info
import utils.utilities as utils

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="academymessage", description="Sends a message to the Academy Channel", guild_ids=[int(info.f1abeezID), int(info.testServerID)])
    async def academyMSG(self, interaction: Interaction):
        roles = interaction.user.roles
        rolesToFind = ["Admin", "Moderator", "Trialist Manager"]
        await interaction.response.send_message(f"Working on it...")
        followup = interaction.followup
        if(utils.check_roles(roles, rolesToFind)):
            await interaction.delete_original_message()
            academyID = info.get_roleID(interaction.guild.id, "academyRole")
            await followup.send(f"<@&{academyID}>\n**TRIAL RACE BRIEFING:**\nWelcome to the F1ABEEZ trial race! I would just like to run through what is expected of you from your trial:\n- Please drive clean - we are a clean racing league, show respect to your fellow drivers! dirty driving will not be tolerated\n- Drive fast! It's still a race after all, we would like to see a true reflection of your pace\n- Do not use medium tyres in Qualifying for this trial race, as this lets us compare your quali pace!\n- Have fun! That's what we're all here for\n\nThe format is short qualifying, 25% race\nAfter the race is completed, one of the trialist leaders will DM you individually with their decision\nPlease react with a thumbs up once you have read this, good luck!")
            last = interaction.channel.last_message_id
            msg = await interaction.channel.fetch_message(int(last))
            await msg.add_reaction("👍")
        else:
            await interaction.delete_original_message()
            await followup.send("You do not have permission to use this command!")

def setup(bot):
    bot.add_cog(Announcements(bot))