from unicodedata import name
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

class Lobby(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="lobby",guild_ids=[int(info.testServerID), int(info.f1abeezID)])
    async def lobbyF1(self, interaction: Interaction, tier: str = SlashOption(name="tier", description="Select your Tier", choices={"Tier 1": "1", "Tier 2": "2", "Tier 3": "3", "Tier 4": "4", "Tier 5": "5", "Tier M": "M", "Tier NA": "NA"})):
        match tier:
            case "1":
                tier1ID = info.get_roleID(interaction.guild.id, "tier1Role")
                reserveTier1ID = info.get_roleID(interaction.guild.id, "reserveTier1Role")
                if(type(tier1ID) == type(None) or type(reserveTier1ID) == type(None)):
                    logging.error("Could not find tier 1 roles", exc_info=True)
                await interaction.send(f"<@&{tier1ID}> <@&{reserveTier1ID}>\n**Lobby is now open!**\nPlease join off <@705761570126561341>\nGamertag is - Sammie230408\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")
            case "2":
                tier2ID = info.get_roleID(interaction.guild.id, "tier2Role")
                reserveTier2ID = info.get_roleID(interaction.guild.id, "reserveTier2Role")
                if(type(tier2ID) == type(None) or type(reserveTier2ID) == type(None)):
                    logging.error("Could not find tier 2 roles", exc_info=True)
                await interaction.send(f"<@&{tier2ID}> <@&{reserveTier2ID}>\n**Lobby is now open!**\nPlease join off <@551387827942719524>\nGamertag is - SebzMB\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")
            case "3":
                tier3ID = info.get_roleID(interaction.guild.id, "tier3Role")
                reserveTier3ID = info.get_roleID(interaction.guild.id, "reserveTier3Role")
                if(type(tier3ID) == type(None) or type(reserveTier3ID) == type(None)):
                    logging.error("Could not find tier 3 roles", exc_info=True)
                await interaction.send(f"<@&{tier3ID}> <@&{reserveTier3ID}>\n**Lobby is now open!**\nPlease join off <@347469082783645697>\nGamertag is - OkayHaus\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")
            case "4":
                tier4ID = info.get_roleID(interaction.guild.id, "tier4Role")
                reserveTier4ID = info.get_roleID(interaction.guild.id, "reserveTier4Role")
                if(type(tier4ID) == type(None) or type(reserveTier4ID) == type(None)):
                    logging.error("Could not find tier 4 roles", exc_info=True)
                await interaction.send(f"<@&{tier4ID}> <@&{reserveTier4ID}>\n**Lobby is now open!**\nPlease join off <@436205062231031808>\nGamertag is - FlameTornado929\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")
            case "5":
                tier5ID = info.get_roleID(interaction.guild.id, "tier5Role")
                reserveTier5ID = info.get_roleID(interaction.guild.id, "reserveTier5Role")
                if(type(tier5ID) == type(None) or type(reserveTier5ID) == type(None)):
                    logging.error("Could not find tier 5 roles", exc_info=True)
                await interaction.send(f"<@&{tier5ID}> <@&{reserveTier5ID}>\n**Lobby is now open!**\nPlease join off <@567093257524346880>\nGamertag is - helios7892\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")
            case "M":
                tierMID = info.get_roleID(interaction.guild.id, "tierMRole")
                reserveTierMID = info.get_roleID(interaction.guild.id, "reserveTierMRole")
                if(type(tierMID) == type(None) or type(reserveTierMID) == type(None)):
                    logging.error("Could not find tier M roles", exc_info=True)
                await interaction.send(f"<@&{tierMID}> <@&{reserveTierMID}>\n**Lobby is now open!**\nPlease join off <@401204069890523137>\nGamertag is - F1AB LeMoNz\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")
            case "NA":
                tierNAID = info.get_roleID(interaction.guild.id, "tierNARole")
                reserveTierNAID = info.get_roleID(interaction.guild.id, "reserveTierNARole")
                if(type(tierNAID) == type(None) or type(reserveTierNAID) == type(None)):
                    logging.error("Could not find tier NA roles", exc_info=True)
                await interaction.send(f"<@&{tierNAID}> <@&{reserveTierNAID}>\n**Lobby is now open!**\nPlease join off <@885760237913669652>\nGamertag is - Supremecream781\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

    @nextcord.slash_command(name="lobbyf2", description="Lobby is open command", guild_ids=[int(info.f2abeezID), int(info.testServerID)])
    async def lobbyf2(self, interaction: Interaction, tierf2: str = SlashOption(name="tier", description="Select your Tier", choices={"Tier 1": "1", "Tier 2": "2"})):
        match tierf2:
            case "1":
                f2tier1ID = info.get_roleID(interaction.guild.id, "f2Tier1Role")
                f2reserveTier1ID = info.get_roleID(interaction.guild.id, "reserveF2Tier1Role")
                if(type(f2tier1ID) == type(None) or type(f2reserveTier1ID) == type(None)):
                    logging.error("Could not find tier 1 F2 roles", exc_info=True)
                await interaction.send(f"<@&{f2tier1ID}> <@&{f2reserveTier1ID}>\n**Lobby is now open!**\nPlease join off <@499568806469959691>\nGamertag is - MrJSmithy\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")
            case "2":
                f2tier2ID = info.get_roleID(interaction.guild.id, "f2Tier2Role")
                f2reserveTier2ID = info.get_roleID(interaction.guild.id, "reserveF2Tier2Role")
                if(type(f2tier2ID) == type(None) or type(f2reserveTier2ID) == type(None)):
                    logging.error("Could not find tier 2 F2 roles", exc_info=True)
                await interaction.send(f"<@&{f2tier2ID}> <@&{f2reserveTier2ID}>\n**Lobby is now open!**\nPlease join off <@499568806469959691>\nGamertag is - MrJSmithy\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

    @nextcord.slash_command(name="ready", description="Ready up command", guild_ids=[int(info.f1abeezID), int(info.testServerID)])
    async def readyf1(self, interaction: Interaction, tier: str = SlashOption(name="tier", description="Select your Tier", choices={"Tier 1": "1", "Tier 2": "2", "Tier 3": "3", "Tier 4": "4", "Tier 5": "5", "Tier M": "M", "Tier NA": "NA"})):
        match tier:
            case "1":
                tier1ID = info.get_roleID(interaction.guild.id, "tier1Role")
                reserveTier1ID = info.get_roleID(interaction.guild.id, "reserveTier1Role")
                if(type(tier1ID) == type(None) or type(reserveTier1ID) == type(None)):
                    logging.error("Could not find tier 1 roles", exc_info=True)
                await interaction.send(f"<@&{tier1ID}> <@&{reserveTier1ID}>\n**Ready up**\n\n")
            case "2":
                tier2ID = info.get_roleID(interaction.guild.id, "tier2Role")
                reserveTier2ID = info.get_roleID(interaction.guild.id, "reserveTier2Role")
                if(type(tier2ID) == type(None) or type(reserveTier2ID) == type(None)):
                    logging.error("Could not find tier 2 roles", exc_info=True)
                await interaction.send(f"<@&{tier2ID}> <@&{reserveTier2ID}>\n**Ready up**\n\n")
            case "3":
                tier3ID = info.get_roleID(interaction.guild.id, "tier3Role")
                reserveTier3ID = info.get_roleID(interaction.guild.id, "reserveTier3Role")
                if(type(tier3ID) == type(None) or type(reserveTier3ID) == type(None)):
                    logging.error("Could not find tier 3 roles", exc_info=True)
                await interaction.send(f"<@&{tier3ID}> <@&{reserveTier3ID}>\n**Ready up**\n\n")
            case "4":
                tier4ID = info.get_roleID(interaction.guild.id, "tier4Role")
                reserveTier4ID = info.get_roleID(interaction.guild.id, "reserveTier4Role")
                if(type(tier4ID) == type(None) or type(reserveTier4ID) == type(None)):
                    logging.error("Could not find tier 4 roles", exc_info=True)
                await interaction.send(f"<@&{tier4ID}> <@&{reserveTier4ID}>\n**Ready up**\n\n")
            case "5":
                tier5ID = info.get_roleID(interaction.guild.id, "tier5Role")
                reserveTier5ID = info.get_roleID(interaction.guild.id, "reserveTier5Role")
                if(type(tier5ID) == type(None) or type(reserveTier5ID) == type(None)):
                    logging.error("Could not find tier 5 roles", exc_info=True)
                await interaction.send(f"<@&{tier5ID}> <@&{reserveTier5ID}>\n**Ready up**\n\n")
            case "M":
                tierMID = info.get_roleID(interaction.guild.id, "tierMRole")
                reserveTierMID = info.get_roleID(interaction.guild.id, "reserveTierMRole")
                if(type(tierMID) == type(None) or type(reserveTierMID) == type(None)):
                    logging.error("Could not find tier M roles", exc_info=True)
                await interaction.send(f"<@&{tierMID}> <@&{reserveTierMID}>\n**Ready up**\n\n")
            case "NA":
                tierNAID = info.get_roleID(interaction.guild.id, "tierNARole")
                reserveTierNAID = info.get_roleID(interaction.guild.id, "reserveTierNARole")
                if(type(tierNAID) == type(None) or type(reserveTierNAID) == type(None)):
                    logging.error("Could not find tier NA roles", exc_info=True)
                await interaction.send(f"<@&{tierNAID}> <@&{reserveTierNAID}>\n**Ready up**\n\n")

    @nextcord.slash_command(name="readyf2", description="Ready up command", guild_ids=[int(info.f2abeezID), int(info.testServerID)])
    async def readyf2(self, interaction: Interaction, tierf2: str = SlashOption(name="tier", description="Select your Tier", choices={"Tier 1": "1", "Tier 2": "2"})):
        match tierf2:
            case "1":
                f2tier1ID = info.get_roleID(interaction.guild.id, "f2Tier1Role")
                f2reserveTier1ID = info.get_roleID(interaction.guild.id, "reserveF2Tier1Role")
                if(type(f2tier1ID) == type(None) or type(f2reserveTier1ID) == type(None)):
                    logging.error("Could not find tier 1 F2 roles", exc_info=True)
                await interaction.send(f"<@&{f2tier1ID}> <@&{f2reserveTier1ID}>\n**Ready up**\n\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")
            case "2":
                f2tier2ID = info.get_roleID(interaction.guild.id, "f2Tier2Role")
                f2reserveTier2ID = info.get_roleID(interaction.guild.id, "reserveF2Tier2Role")
                if(type(f2tier2ID) == type(None) or type(f2reserveTier2ID) == type(None)):
                    logging.error("Could not find tier 1 F2 roles", exc_info=True)
                await interaction.send(f"<@&{f2tier2ID}> <@&{f2reserveTier2ID}>\n**Ready up**\n\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

def setup(bot):
    bot.add_cog(Lobby(bot))