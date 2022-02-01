from ast import If
import asyncio
import nextcord
from nextcord import client
from nextcord import message
from nextcord.colour import Color
from nextcord.ext import tasks, commands
from nextcord.ext.commands import CommandNotFound
from nextcord.ext.commands.core import check
from nextcord.ui import view
from nextcord.ui.view import View
import requests
import json
import os
import datetime
import pytz
import notion as nt
import info
import logging


logging.basicConfig(format='%(asctime)s-%(levelname)s:%(message)s')

class TierMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  
  async def handle_click(self, button, interaction):
    if(str(button.custom_id) == "Tier_1"):
      self.tierSelected = "F1 - Tier 1"
      self.stop()
    elif(str(button.custom_id) == "Tier_2"):
      self.tierSelected = "F1 - Tier 2"
      self.stop()
    elif(str(button.custom_id) == "Tier_3"):
      self.tierSelected = "F1 - Tier 3"
      self.stop()
    # elif(str(button.custom_id) == "Tier_4"):
    #   self.tierSelected = "F1 - Tier 4"
    #   self.stop()
    # elif(str(button.custom_id) == "Nations_League"):
    #   self.tierSelected = "Nations League"
    #   self.stop()
    # elif(str(button.custom_id) == "F2"):
    #   self.tierSelected = "F2"
    #   self.stop()

  @nextcord.ui.button(label="Tier 1", style=nextcord.ButtonStyle.primary, custom_id="Tier_1")
  async def tier1ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)
  
  @nextcord.ui.button(label="Tier 2", style=nextcord.ButtonStyle.primary, custom_id="Tier_2")
  async def tier2ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)

  @nextcord.ui.button(label="Tier 3", style=nextcord.ButtonStyle.primary, custom_id="Tier_3")
  async def tier3ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)

  # @nextcord.ui.button(label="Tier 4", style=nextcord.ButtonStyle.primary, custom_id="Tier_4")
  # async def tier4ButtonClicked(self, button, interaction):
  #   await self.handle_click(button, interaction)

  # @nextcord.ui.button(label="Nations League", style=nextcord.ButtonStyle.primary, custom_id="Nations_League")
  # async def tiermButtonClicked(self, button, interaction):
  #   await self.handle_click(button, interaction)

  # @nextcord.ui.button(label="F2", style=nextcord.ButtonStyle.primary, custom_id="F2")
  # async def f2ButtonClicked(self, button, interaction):
  #   await self.handle_click(button, interaction)

class SuggestionMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  
  async def handle_click(self, button, interaction):
    if(str(button.custom_id) == "Yes"):
      self.anonymous = True
      self.stop()
    elif(str(button.custom_id) == "No"):
      self.anonymous = False
      self.stop()

  @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.primary, custom_id="Yes")
  async def yesClicked(self, button, interaction):
    await self.handle_click(button, interaction)
  
  @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.primary, custom_id="No")
  async def noClicked(self, button, interaction):
    await self.handle_click(button, interaction)


class CalendarMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  
  async def handle_click(self, button, interaction):
    if(str(button.custom_id) == "F1"):
      self.tierSelected = "F1"
      self.stop()
    elif(str(button.custom_id) == "Nations_League"):
      self.tierSelected = "Nations League"
      self.stop()

  @nextcord.ui.button(label="F1", style=nextcord.ButtonStyle.primary, custom_id="F1")
  async def tier1ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)
  
  # @nextcord.ui.button(label="Nations League", style=nextcord.ButtonStyle.primary, custom_id="Nations_League")
  # async def tier2ButtonClicked(self, button, interaction):
  #   await self.handle_click(button, interaction)

class reportMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  async def handle_click(self, button, interaction):
    user = interaction.user
    channel = interaction.channel
    if(interaction.channel_id == info.incidentReportChannel):
      bst = pytz.timezone("Europe/London")
      todayInc = datetime.datetime.now(tz=bst).isoformat()
      def check(m):
        return m.author == user and m.guild is None 

      def checkRaw(u):
        return u.user_id == user.id and u.guild_id is None
      
      await interaction.response.send_message(f"Please follow the bot to your DMs to report your incident {user.mention}", ephemeral=True)

      try:
          await user.send("What is your gamertag?")
          gamertagOfUserInc = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfUserInc = gamertagOfUserInc.content
          await user.send("Please describe your incident.")
          descriptionInc = await bot.wait_for("message", check=check, timeout=180.0)
          descriptionInc = descriptionInc.content

          view = TierMenu()
          await user.send("Select in which tier did the incident occur", view=view)
          await view.wait()
          if(view.tierSelected == "F1 - Tier 1"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier 2"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier 3"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F1 - Tier 4"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "Nations League"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          elif(view.tierSelected == "F2"):
            tierOfIncidentInc = view.tierSelected
            await user.send(f"You selected {tierOfIncidentInc}")
          await user.send("Please provide video evidence (Only reply with links to gamerdvr or other services)")
          evidenceInc = await bot.wait_for("message", check=check, timeout=180.0)
          evidenceInc = evidenceInc.content
          await user.send("What lap did this incident/penalty occur on?")
          lapOfIncidentInc = await bot.wait_for("message", check=check, timeout=180.0)
          lapOfIncidentInc = lapOfIncidentInc.content
          await user.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
          gamertagOfInvolevedDriverInc = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfInvolevedDriverInc = gamertagOfInvolevedDriverInc.content
          response = nt.submitAnIncident(gamertagOfUserInc, lapOfIncidentInc, descriptionInc, tierOfIncidentInc, evidenceInc, gamertagOfInvolevedDriverInc, todayInc)
          logEmbed = nextcord.Embed(title="⚠️New Ticket has been reported!⚠️")
          logEmbed.add_field(name="Tier", value=tierOfIncidentInc, inline=False)
          logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserInc} vs {gamertagOfInvolevedDriverInc}", inline=False)
          channel = bot.get_channel(info.incidentLogChannel)
          await channel.send(embed = logEmbed)
          await user.send(response)
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("incident report:")
        print(e)
      


    if(interaction.channel.id == info.appealReportChannel):
      bst = pytz.timezone("Europe/London")
      todayApp = datetime.datetime.now(tz=bst).isoformat()
      def check(m):
        return m.author == user and m.guild is None 
        
      await interaction.response.send_message(f"Please follow the bot to your DMs to submit your appeal {user.mention}", ephemeral=True)
      try:
          await user.send("What is the case number you want to appeal (use ;gettickets in the bot channel in the server if you need to get it)")
          caseNumberApp = await bot.wait_for("message", check=check, timeout=180.0)
          caseNumberApp = caseNumberApp.content
          await user.send("What is your gamertag?")
          gamertagOfUserApp = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfUserApp = gamertagOfUserApp.content
          await user.send("Please state the reason for you appeal.")
          reasonApp = await bot.wait_for("message", check=check, timeout=180.0)
          reasonApp = reasonApp.content
          await user.send("State any additional information to support your appeal (if you don't have any, reply with N/A)")
          additionalInfoApp = await bot.wait_for("message", check=check, timeout=180.0)
          additionalInfoApp = additionalInfoApp.content
          await user.send("Please provide addition video evidence to support your appeal (Only reply with links to gamerdvr or other services)")
          evidenceApp = await bot.wait_for("message", check=check, timeout=180.0)
          evidenceApp = evidenceApp.content
          await user.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
          gamertagOfInvolevedDriverApp = await bot.wait_for("message", check=check, timeout=180.0)
          gamertagOfInvolevedDriverApp = gamertagOfInvolevedDriverApp.content
          response = nt.submitAppeal(caseNumberApp, evidenceApp, gamertagOfUserApp, gamertagOfInvolevedDriverApp, reasonApp, additionalInfoApp, todayApp)
          logEmbed = nextcord.Embed(title="⚠️New Appeal has been submitted!⚠️")
          logEmbed.add_field(name="Case Number", value=caseNumberApp, inline=False)
          logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserApp} vs {gamertagOfInvolevedDriverApp}", inline=False)
          channel = bot.get_channel(info.incidentLogChannel)
          await channel.send(embed = logEmbed)
          await user.send(response)
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is a three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("Appeal:")
        print(e)
      


    if(interaction.channel.id == info.suggestionSubmitChannel):
      def check(m):
        return m.author == user and m.guild is None 
      try:      
        await interaction.response.send_message(f"Please follow the bot to your DMs! {user.mention}", ephemeral=True)
        await user.send("Please type your suggestion here, the admins will have a look at it as soon as possible. Thank you, Admins of F1ABEEZ")
        suggestion = await bot.wait_for("message", check=check, timeout=300.0)
        suggestion = suggestion.content
        view = SuggestionMenu()
        await user.send("Do you wish to stay anonymous?", view=view)
        await view.wait()
      except asyncio.TimeoutError:
        await user.send("Unfortunately you took too long. The limit is 5 minutes per message")
      except Exception as e:
        print("suggestion:")
        print(e)

      suggestionLogEmbed = nextcord.Embed(title="🚨A new suggestion has been submitted🚨")
      if(view.anonymous == False):
        suggestionLogEmbed.add_field(name="**Submitted by:**", value=user.display_name, inline=False)
      suggestionLogEmbed.add_field(name="**Suggestion**", value=suggestion, inline=False)
      channel = bot.get_channel(info.suggestionLogChannel)
      await channel.send(embed = suggestionLogEmbed)
      await user.send("Your suggestion has been submitted to the admins!")

  @nextcord.ui.button(label="", emoji="📨", style=nextcord.ButtonStyle.primary, custom_id="id")
  async def reportButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)


def GetHelpCommand():
    embed = nextcord.Embed(title="Help", color=info.color)
    embed.add_field(name=";standings", value="This command gives you a menu to select the tier of which you want to see standings and then it returns them in the channel.", inline=False)
    embed.add_field(name=";calendar", value="This command gives you a selection of the F1 or Nations League calendar and then sends it in the channel.", inline=False)
    embed.add_field(name=";gettickets <gamertag>", value="This command is useful when you don’t know the number of your ticket. The command lists all tickets you’ve been involved (whether you reported it or someone else reported you) and gives you the number of the ticket and the direct link to the website.", inline=False)
    embed.add_field(name=";getappeals <gamertag>", value="This command gets you a list of appeals you've been involeved in (whether you appealed or someone appealed against you) and gives you the number of the appeal, a direct link to the website and the status of the appeal.")
    embed.add_field(name=";ticketdetail <number of ticket>", value="This command gets you the details of ticket you provide. It lists the status, penalty that was awarded and who was involved.", inline=False)
    embed.add_field(name=";incidentreport", value="This command allows you to submit an incident from nextcord. Please read the messages carefully and reply correctly.", inline=False)
    embed.add_field(name=";submitappeal", value="This command allows you to submit an appeal to a decision that has been made by the stewards. Please use ;gettickets before you start submitting it to make sure you know the case number of the incident you want to appeal", inline=False)
    return embed

def getStaffHelpCommand():
  embed = nextcord.Embed(title="Staff Help", color=info.color)
  embed.add_field(name=";dotd", value="Sends the DOTD vote message\nusage: ;dotd tier, driver1Name, driver1PosChange, driver2Name, driver2PosChange, driver3Name, driver3PosChange, driver4Name, driver4PosChange, driver5Name, driver5PosChange", inline=False)
  embed.add_field(name=";dotdwinner", value="Sends the winner of DOTD\nusage: ;dotdwinner tier, winnerName", inline=False)
  embed.add_field(name=";lobbytier<tierNumber>", value="Sends the lobby is open message. Enter the tier number instead of <tierNumber>", inline=False)
  embed.add_field(name=";readytier<tierNumber>", value="Sends the ready up instruction. Enter the tier number instead of <tierNumber>", inline=False)
  embed.add_field(name=";racetier<tierNumber>", value="Sends the race ready up instruction. Enter the tier number instead of <tierNumber>", inline=False)
  embed.add_field(name=";stewardsdecision <roundNumber>", value="Send the links to respective tier race reports. Enter round number instead of <roundNumber>", inline=False)
  embed.add_field(name=";academymessage", value="Send the academy info message", inline=False)
  embed.add_field(name=";warn <user> <reason>", value="(ADMIN ONLY) - allows to warn a user, sending the warning into the proper channel to keep track.")
  embed.add_field(name=";ban <user> <reason>", value="(ADMIN ONLY) - allows to ban a user, and automatically sends it into the ban channel.", inline=False)
  embed.add_field(name=";racereport <roundNumber>", value="Send the links to respective tier race reports. Enter round number instead of <roundNumber>", inline=False)
  embed.add_field(name=";channelname", value="Provide the channel name separated by - (e.g. this-is-a-channel) and the bot will return the name in the special font", inline=False)
  return embed

def dotdMessageFun(str):
  tier = str[0]
  driver1 = str[1]
  driver1PosChange = str[2]
  driver2 = str[3]
  driver2PosChange = str[4]
  driver3 = str[5]
  driver3PosChange = str[6]
  driver4 = str[7]
  driver4PosChange = str[8]
  driver5 = str[9]
  driver5PosChange = str[10]
  if(tier == "Tier 1"):
    return(f"<@&{info.tier1Role}>\n\n**Tier 1 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "Tier 2"):
    return(f"<@&{info.tier2Role}>\n\n**Tier 2 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "Tier 3"):
    return(f"<@&{info.tier3Role}>\n\n**Tier 3 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "Tier 4"):
    return(f"<@&{info.tierMRole}>\n\n**Tier 4 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  elif(tier == "NL"):
    return(f"<@&{info.nationsLeagueRole}>\n\n**Tier 4 Driver of The Day poll:**\n\n1️⃣ - {driver1} - {driver1PosChange}\n2️⃣ - {driver2} - {driver2PosChange}\n3️⃣ - {driver3} - {driver3PosChange}\n4️⃣ - {driver4} - {driver4PosChange}\n5️⃣ - {driver5} - {driver5PosChange}")
  
def dotdWinnerMsg(tier, driver):
  if(tier == "Tier 1"):
    return(f"<@&{info.tier1Role}>\n\n**Tier 1 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "Tier 2"):
    return(f"<@&{info.tier2Role}>\n\n**Tier 2 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "Tier 3"):
    return(f"<@&{info.tier3Role}>\n\n**Tier 3 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "Tier 4"):
    return(f"<@&{info.tierMRole}>\n\n**Tier 2 Driver of The Day:**\n\n{driver}\n\nCongratulations!")
  elif(tier == "NL"):
    return(f"<@&{info.nationsLeagueRole}>\n\n**Tier 2 Driver of The Day:**\n\n{driver}\n\nCongratulations!")


intents = nextcord.Intents.default()
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix=";", help_command=None, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    logging.info("We have logged in as {0.user}".format(bot))
    bot.add_view(reportMenu())
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="F1ABEEZ Server 🚀"))

@bot.command(name="help")
async def HelpCommand(ctx):
    await ctx.send(embed = GetHelpCommand())

@bot.command(name="staffhelp")
@commands.has_any_role("Staff")
async def StaffHelpCommand(ctx):
  embed = getStaffHelpCommand()
  await ctx.send(embed=embed)

@bot.command(name="gettickets")
async def GetTickets(ctx, *, arg):
    await ctx.send(embed=nt.queryTickets(arg))

@bot.command(name="getprofile")
async def GetProfile(ctx, *, arg):
    await ctx.send(embed=nt.getProfileInfo(arg))    

@bot.command(name="getappeals")
async def GetAppeals(ctx, *, arg):
  await ctx.send(embed = nt.queryAppeals(arg))

@bot.command(name="ticketdetail")
async def TicketDetail(ctx, ticketNum):
    await ctx.send(embed = nt.TicketDetailQuery(ticketNum))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found")
    logging.error(error)

@bot.command(name="lobbytier1")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier1(ctx):
  tier1ID = info.get_roleID(ctx.guild.id, "tier1Role")
  reserveTier1ID = info.get_roleID(ctx.guild.id, "reserveTier1Role")
  if(type(tier1ID) == type(None) or type(reserveTier1ID) == type(None)):
    logging.error("Could not find tier 1 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier1ID}> <@&{reserveTier1ID}>\n**Lobby is now open!**\nPlease join off <@705761570126561341>\nGamertag is - Sammie230408\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier2")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier2(ctx):
  tier2ID = info.get_roleID(ctx.guild.id, "tier2Role")
  reserveTier2ID = info.get_roleID(ctx.guild.id, "reserveTier2Role")
  if(type(tier2ID) == type(None) or type(reserveTier2ID) == type(None)):
    logging.error("Could not find tier 2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier2ID}> <@&{reserveTier2ID}>\n**Lobby is now open!**\nPlease join off <@483678704749510677>\nGamertag is - thxharvey\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier3")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier3(ctx):
  tier3ID = info.get_roleID(ctx.guild.id, "tier3Role")
  reserveTier3ID = info.get_roleID(ctx.guild.id, "reserveTier3Role")
  if(type(tier3ID) == type(None) or type(reserveTier3ID) == type(None)):
    logging.error("Could not find tier 3 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier3ID}> <@&{reserveTier3ID}>\n**Lobby is now open!**\nPlease join off <@401204069890523137>\nGamertag is - OwningLeMoNz\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier4")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier4(ctx):
  tier4ID = info.get_roleID(ctx.guild.id, "tier4Role")
  reserveTier4ID = info.get_roleID(ctx.guild.id, "reserveTier4Role")
  if(type(tier4ID) == type(None) or type(reserveTier4ID) == type(None)):
    logging.error("Could not find tier 4 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier4ID}> <@&{reserveTier4ID}>\n**Lobby is now open!**\nPlease join off <@559096129816363010>\nGamertag is - Razznyk\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier5")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier4(ctx):
  tier5ID = info.get_roleID(ctx.guild.id, "tier5Role")
  reserveTier5ID = info.get_roleID(ctx.guild.id, "reserveTier5Role")
  if(type(tier5ID) == type(None) or type(reserveTier5ID) == type(None)):
    logging.error("Could not find tier 5 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier5ID}> <@&{reserveTier5ID}>\n**Lobby is now open!**\nPlease join off <@559096129816363010>\nGamertag is - Razznyk\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytierM")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier4(ctx):
  tierMID = info.get_roleID(ctx.guild.id, "tierMRole")
  reserveTierMID = info.get_roleID(ctx.guild.id, "reserveTierMRole")
  if(type(tierMID) == type(None) or type(reserveTierMID) == type(None)):
    logging.error("Could not find tier M roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tierMID}> <@&{reserveTierMID}>\n**Lobby is now open!**\nPlease join off <@559096129816363010>\nGamertag is - Razznyk\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytierNA")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier4(ctx):
  tierNAID = info.get_roleID(ctx.guild.id, "tierNARole")
  reserveTierNAID = info.get_roleID(ctx.guild.id, "reserveTierNARole")
  if(type(tierNAID) == type(None) or type(reserveTierNAID) == type(None)):
    logging.error("Could not find tier NA roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tierNAID}> <@&{reserveTierNAID}>\n**Lobby is now open!**\nPlease join off <@559096129816363010>\nGamertag is - Razznyk\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbyf2tier1")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGf2Tier1(ctx):
  f2tier1ID = info.get_roleID(ctx.guild.id, "f2Tier1Role")
  f2reserveTier1ID = info.get_roleID(ctx.guild.id, "reserveF2Tier1Role")
  if(type(f2tier1ID) == type(None) or type(f2reserveTier1ID) == type(None)):
    logging.error("Could not find tier 1 F2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{f2tier1ID}> <@&{f2reserveTier1ID}>\n**Lobby is now open!**\nPlease join off <@499568806469959691>\nGamertag is - MrJSmithy\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbyf2tier2")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGf2Tier2(ctx):
  f2tier2ID = info.get_roleID(ctx.guild.id, "f2Tier2Role")
  f2reserveTier2ID = info.get_roleID(ctx.guild.id, "reserveF2Tier2Role")
  if(type(f2tier2ID) == type(None) or type(f2reserveTier2ID) == type(None)):
    logging.error("Could not find tier 2 F2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{f2tier2ID}> <@&{f2reserveTier2ID}>\n**Lobby is now open!**\nPlease join off <@499568806469959691>\nGamertag is - MrJSmithy\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="readytier1")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier1(ctx):
  tier1ID = info.get_roleID(ctx.guild.id, "tier1Role")
  reserveTier1ID = info.get_roleID(ctx.guild.id, "reserveTier1Role")
  if(type(tier1ID) == type(None) or type(reserveTier1ID) == type(None)):
    logging.error("Could not find tier 1 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier1ID}> <@&{reserveTier1ID}>\n**Ready up**\n\n")

@bot.command(name="readytier2")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier2(ctx):
  tier2ID = info.get_roleID(ctx.guild.id, "tier2Role")
  reserveTier2ID = info.get_roleID(ctx.guild.id, "reserveTier2Role")
  if(type(tier2ID) == type(None) or type(reserveTier2ID) == type(None)):
    logging.error("Could not find tier 2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier2ID}> <@&{reserveTier2ID}>\n**Ready up**\n\n")

@bot.command(name="readytier3")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier3(ctx):
  tier3ID = info.get_roleID(ctx.guild.id, "tier3Role")
  reserveTier3ID = info.get_roleID(ctx.guild.id, "reserveTier3Role")
  if(type(tier3ID) == type(None) or type(reserveTier3ID) == type(None)):
    logging.error("Could not find tier 3 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier3ID}> <@&{reserveTier3ID}>\n**Ready up**\n\n")

@bot.command(name="readytier4")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier4(ctx):
  tier4ID = info.get_roleID(ctx.guild.id, "tier4Role")
  reserveTier4ID = info.get_roleID(ctx.guild.id, "reserveTier4Role")
  if(type(tier4ID) == type(None) or type(reserveTier4ID) == type(None)):
    logging.error("Could not find tier 4 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier4ID}> <@&{reserveTier4ID}>\n**Ready up**\n\n")

@bot.command(name="readytier5")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier5(ctx):
  tier5ID = info.get_roleID(ctx.guild.id, "tier5Role")
  reserveTier5ID = info.get_roleID(ctx.guild.id, "reserveTier5Role")
  if(type(tier5ID) == type(None) or type(reserveTier5ID) == type(None)):
    logging.error("Could not find tier 5 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier5ID}> <@&{reserveTier5ID}>\n**Ready up**\n\n")

@bot.command(name="readytierM")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtierM(ctx):
  tierMID = info.get_roleID(ctx.guild.id, "tierMRole")
  reserveTierMID = info.get_roleID(ctx.guild.id, "reserveTierMRole")
  if(type(tierMID) == type(None) or type(reserveTierMID) == type(None)):
    logging.error("Could not find tier M roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tierMID}> <@&{reserveTierMID}>\n**Ready up**\n\n")

@bot.command(name="readytierNA")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtierNA(ctx):
  tierNAID = info.get_roleID(ctx.guild.id, "tierNARole")
  reserveTierNAID = info.get_roleID(ctx.guild.id, "reserveTierNARole")
  if(type(tierNAID) == type(None) or type(reserveTierNAID) == type(None)):
    logging.error("Could not find tier NA roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tierNAID}> <@&{reserveTierNAID}>\n**Ready up**\n\n")

@bot.command(name="readyf2tier1")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGf2tier1(ctx):
  f2tier1ID = info.get_roleID(ctx.guild.id, "f2Tier1Role")
  f2reserveTier1ID = info.get_roleID(ctx.guild.id, "reserveF2Tier1Role")
  if(type(f2tier1ID) == type(None) or type(f2reserveTier1ID) == type(None)):
    logging.error("Could not find tier 1 F2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{f2tier1ID}> <@&{f2reserveTier1ID}>\n**Ready up**\n\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

@bot.command(name="readyf2tier2")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGf2tier2(ctx):
  f2tier2ID = info.get_roleID(ctx.guild.id, "f2Tier2Role")
  f2reserveTier2ID = info.get_roleID(ctx.guild.id, "reserveF2Tier2Role")
  if(type(f2tier2ID) == type(None) or type(f2reserveTier2ID) == type(None)):
    logging.error("Could not find tier 1 F2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{f2tier2ID}> <@&{f2reserveTier2ID}>\n**Ready up**\n\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

@bot.command(name="racetier1")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier1(ctx):
  tier1ID = info.get_roleID(ctx.guild.id, "tier1Role")
  reserveTier1ID = info.get_roleID(ctx.guild.id, "reserveTier1Role")
  if(type(tier1ID) == type(None) or type(reserveTier1ID) == type(None)):
    logging.error("Could not find tier 1 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier1ID}> <@&{reserveTier1ID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier2")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier2(ctx):
  tier2ID = info.get_roleID(ctx.guild.id, "tier2Role")
  reserveTier2ID = info.get_roleID(ctx.guild.id, "reserveTier2Role")
  if(type(tier2ID) == type(None) or type(reserveTier2ID) == type(None)):
    logging.error("Could not find tier 2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier2ID}> <@&{reserveTier2ID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier3")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier3(ctx):
  tier3ID = info.get_roleID(ctx.guild.id, "tier3Role")
  reserveTier3ID = info.get_roleID(ctx.guild.id, "reserveTier3Role")
  if(type(tier3ID) == type(None) or type(reserveTier3ID) == type(None)):
    logging.error("Could not find tier 3 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier3ID}> <@&{reserveTier3ID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier4")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier4(ctx):
  tier4ID = info.get_roleID(ctx.guild.id, "tier4Role")
  reserveTier4ID = info.get_roleID(ctx.guild.id, "reserveTier4Role")
  if(type(tier4ID) == type(None) or type(reserveTier4ID) == type(None)):
    logging.error("Could not find tier 4 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier4ID}> <@&{reserveTier4ID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier5")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier5(ctx):
  tier5ID = info.get_roleID(ctx.guild.id, "tier5Role")
  reserveTier5ID = info.get_roleID(ctx.guild.id, "reserveTier5Role")
  if(type(tier5ID) == type(None) or type(reserveTier5ID) == type(None)):
    logging.error("Could not find tier 5 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tier5ID}> <@&{reserveTier5ID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetierM")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtierM(ctx):
  tierMID = info.get_roleID(ctx.guild.id, "tierMRole")
  reserveTierMID = info.get_roleID(ctx.guild.id, "reserveTierMRole")
  if(type(tierMID) == type(None) or type(reserveTierMID) == type(None)):
    logging.error("Could not find tier M roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tierMID}> <@&{reserveTierMID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetierNA")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtierNA(ctx):
  tierNAID = info.get_roleID(ctx.guild.id, "tierNARole")
  reserveTierNAID = info.get_roleID(ctx.guild.id, "reserveTierNARole")
  if(type(tierNAID) == type(None) or type(reserveTierNAID) == type(None)):
    logging.error("Could not find tier NA roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{tierNAID}> <@&{reserveTierNAID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racef2tier1")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGf2tier1(ctx):
  f2tier1ID = info.get_roleID(ctx.guild.id, "f2Tier1Role")
  f2reserveTier1ID = info.get_roleID(ctx.guild.id, "reserveF2Tier1Role")
  if(type(f2tier1ID) == type(None) or type(f2reserveTier1ID) == type(None)):
    logging.error("Could not find tier 1 F2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{f2tier1ID}> <@&{f2reserveTier1ID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racef2tier2")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGf2tier2(ctx):
  f2tier2ID = info.get_roleID(ctx.guild.id, "f2Tier2Role")
  f2reserveTier2ID = info.get_roleID(ctx.guild.id, "reserveF2Tier2Role")
  if(type(f2tier2ID) == type(None) or type(f2reserveTier2ID) == type(None)):
    logging.error("Could not find tier 1 F2 roles", exc_info=True)
  await ctx.message.delete()
  await ctx.send(f"<@&{f2tier2ID}> <@&{f2reserveTier2ID}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="academymessage")
@commands.has_any_role("Admin", "Moderator", "Trialist Manager")
async def academyMSG(ctx):
  academyID = info.get_roleID(ctx.guild.id, "academyRole")
  await ctx.message.delete()
  msg =  await ctx.send(f"<@&{academyID}>\n**TRIAL RACE BRIEFING:**\nWelcome to the F1ABEEZ trial race! I would just like to run through what is expected of you from your trial:\n- Please drive clean - we are a clean racing league, show respect to your fellow drivers! dirty driving will not be tolerated\n- Drive fast! It's still a race after all, we would like to see a true reflection of your pace\n- Do not use medium tyres in Qualifying for this trial race, as this lets us compare your quali pace!\n- Have fun! That's what we're all here for\n\nThe format is short qualifying, 25% race\nAfter the race is completed, one of the trialist leaders will DM you individually with their decision\nPlease react with a thumbs up once you have read this, good luck!")
  await msg.add_reaction("👍")


@bot.command(name="warn")
@commands.has_any_role("Admin")
async def warn(ctx, user=None, *, reason=None):
  if(user is None):
    await ctx.send("You didn't mention the user")
    return
  if(reason is None):
    await ctx.send("You didn't provide a reason")
    return
  
  try: 
    member = ctx.message.mentions[0]
    membername = ctx.message.mentions[0].name
  except IndexError:
    print(user)
    member = await ctx.guild.fetch_member(int(user))
    print(member)
    membername = member.name
  except Exception as e:
    print("warn:")
    print(e)

  embed = nextcord.Embed(title="A Warning has been issued", color=info.color)
  embed.add_field(name="User", value=membername, inline=False)
  embed.add_field(name="Reason", value=reason, inline=False)
  channel = bot.get_channel(info.get_channelID(ctx.guild.id, "warningChannel"))
  await channel.send(embed = embed)
  await ctx.send(embed = embed)   

@bot.command(name="ban")
@commands.has_any_role("Admin")
async def ban(ctx, user=None, *, reason=None):
  if(user is None):
    await ctx.send("You didn't mention the user")
    return
  if(reason is None):
    await ctx.send("You didn't provide a reason")
    return

  try: 
    member = ctx.message.mentions[0]
    membername = ctx.message.mentions[0].name
  except IndexError:
    print(user)
    member = await ctx.guild.fetch_member(int(user))
    print(member)
    membername = member.name
  except Exception as e:
    print("ban:")
    print(e)

  embed = nextcord.Embed(title="A Ban has been issued", color=info.color)
  embed.add_field(name="User", value=membername, inline=False)
  embed.add_field(name="Reason", value=reason, inline=False)
  channel = bot.get_channel(info.get_channelID(ctx.guild.id, "banChannel"))
  await channel.send(embed = embed)
  await member.ban(reason = reason)
  await ctx.send(embed = embed)   
    
@bot.event
async def on_member_join(member):
  serverID = member.guild.id
  role = nextcord.utils.get(member.guild.roles, name="Academy Driver")
  await member.add_roles(role)
  channel = bot.get_channel(info.get_channelID(serverID, "welcomeChannel"))
  if(type(channel) != type(None)):
    await channel.send(f"**Welcome <@{member.id}>**\n\nPlease use this chat if you have any questions and someone will be on hand.\n\nAll the information you need is on <#865379267977412618>")
  else:
    logging.error("welcomeChannel not found")

@bot.event
async def on_member_remove(member):
  memberName = member.name
  channel = bot.get_channel(info.leavingChannel)
  await channel.send(f"**{memberName}** has left the server.")

@bot.command(name="stewardsdecisions")
@commands.has_any_role("Admin", "Moderator", "Steward")
async def stewardsDecision(ctx, round):
  channel = bot.get_channel(info.stewardsAnnoucementChannel)
  roundNO = int(round)
  # f2RoundNO = roundNO - 1
  # f2round = f"R{f2RoundNO}"
  round = f"r{roundNO}"
  tier1URL = f"<https://f1abeez.com/race-reports/t1/{round}>"
  tier2URL = f"<https://f1abeez.com/race-reports/t2/{round}>"
  tier3URL = f"<https://f1abeez.com/race-reports/t3/{round}>"
  # tier4URL = f"<https://f1abeez.com/race-reports/t4/{round}>"
  # if(roundNO - 1 == 0):
  #   f2URL = "F2 did not race"
  # else:
  #   f2URL = f"<https://f1abeez.com/race-reports/F2-{f2round}>"
  
  await channel.send(f"🦺 @everyone\n\n**All Stewards decisions are finalised**\nPlease check this week's race-report for all the incidents reported and decisions made.\n\n**F1 - Tier 1** - {tier1URL}\n**F1 - Tier 2** - {tier2URL}\n**F1 - Tier 3** - {tier3URL}\n\nPlease file your appeals with the correct case number **in the next 24 hours**, and standings will be posted after all appeals are finalised \nFollow the instructions in <#864999507238322186> to submit your appeals \n\nThank you,\nStewards of F1ABEEZ")

@bot.command(name="racereport")
@commands.has_any_role("Admin", "Moderator")
async def raceResults(ctx, round):
  channel = bot.get_channel(info.generalAnnoucementChannel)
  roundNO = int(round)
  # f2RoundNO = roundNO - 1
  # f2round = f"R{f2RoundNO}"
  round = f"r{roundNO}"
  tier1URL = f"<https://f1abeez.com/race-reports/t1/{round}>"
  tier2URL = f"<https://f1abeez.com/race-reports/t2/{round}>"
  tier3URL = f"<https://f1abeez.com/race-reports/t3/{round}>"
  # tier4URL = f"<https://f1abeez.com/race-reports/t4/{round}>"
  # if(roundNO - 1 == 0):
  #   f2URL = "F2 did not race"
  # else:
  #   f2URL = f"<https://f1abeez.com/race-reports/F2-{f2round}>"
  await channel.send(f"@everyone\n\n**Race Reports have now been published**\n\n**F1 - Tier 1** - {tier1URL}\n**F1 - Tier 2** - {tier2URL}\n**F1 - Tier 3** - {tier3URL}")

@bot.command(name="incidentchannel")
@commands.has_any_role("Admin", "Moderator")
async def incidentChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Report an incident",description="React to this message to report an incident by clicking the 📨 button", color=info.color)
  await ctx.send(embed=embed, view=reportMenu())
  # msg = await ctx.send(embed = embed)
  # await msg.add_reaction("📨")

@bot.command(name="appealchannel")
@commands.has_any_role("Admin", "Moderator")
async def appealChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Submit an appeal",description="React to this message to submit an appeal by clicking the 📨 button", color=info.color)
  await ctx.send(embed=embed, view=reportMenu())

@bot.command(name="suggestionchannel")
@commands.has_any_role("Admin", "Moderator")
async def suggestionChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Submit a suggestion",description="React to this message to submit a suggestion by clicking the 📨 button", color=info.color)
  await ctx.send(embed=embed, view=reportMenu())

@bot.command(name="calendar")
async def getCalendar(ctx):
  await ctx.message.delete()
  view = CalendarMenu()
  selectMSG = await ctx.send("For which tier do you want to see standings?", view=view)
  await view.wait()
  if(view.tierSelected == "F1"):
    msg = await ctx.send("Getting the F1 calendar...")
    try:
      await selectMSG.delete()
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=2%3A138&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      if(r):
        await msg.delete()
      img = r["images"]["2:138"]
      embed1 = nextcord.Embed(color=info.color) 
      embed1.set_image(url=img) 
      await ctx.send(embed=embed1)
    except Exception as e:
      await ctx.send(f"There was an error getting the calendar, please report this issue to the admins.")
      print("calendar:")
      print(e)
  elif(view.tierSelected == "Nations League"):
    msg = await ctx.send("Getting the Nations League calendar...")
    try:
      await selectMSG.delete()
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=15%3A2&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      if(r):
        await msg.delete()
      img = r["images"]["15:2"]
      print(img)
      embed2 = nextcord.Embed(color=info.color) 
      embed2.set_image(url=img) 
      await ctx.send(embed=embed2)
    except Exception as e:
      await ctx.send(f"There was an error getting the calendar, please report this issue to the admins.")
      print("calendar:")
      print(e)


@bot.command(name="standings")
async def getStandings(ctx):
  await ctx.message.delete()
  view = TierMenu()
  selectMSG = await ctx.send("For which tier do you want to see standings?", view=view)
  await view.wait()
  try:
    if(view.tierSelected == "F1 - Tier 1"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 1 Standings")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 2"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 2 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A446&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:446"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 3"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 3 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A265&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:265"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 4"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 4 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A351&format=png", headers={"X-Figma-Token": info.figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:351"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "Nations League"):
      await ctx.send("Graphics for Nations League standings are currently not available")
  except KeyError:
    await ctx.send("There was an error while getting the standings. Please report this issue to the admins")
    print(KeyError)
  except Exception as e:
    print("standings:")
    print(e)

@bot.command(name="changelog")
async def sendChangesAnnouncement(ctx):
  await ctx.message.delete()
  await ctx.send("@everyone")
  e = nextcord.Embed(title="F1ABEEZ Bot Updates!",description="To add to the tally of new stuff introduced on the stream I have an announcement on some new things our bot can do, **as well as some improvements to those that it already does!**" , color=info.color)
  e.add_field(name="Ticket commands", value="First things first there is an improvement to the all the commands regarding tickets (;gettickets, ;ticketdetail, ;getappeals) - all these commands now **include a link directly to the website** so you can view them quicker and in full!", inline=False)
  e.add_field(name="Reporting incidents", value="Secondly there are changes to the way you report incidents and submit appeals, instead of a reaction** there is now a button!** Similar buttons are then used inside reporting the ticket to select the tier for which you want to report the incident.", inline=False)
  e.add_field(name="New command 1: ;standings", value="This command will get you our brand new standings graphics for every single tier so you can see where you are in the drivers and how your team is doing in the constructors!", inline=False)
  e.add_field(name="New command 2: ;calendar", value="This command gets you our calendar graphic that you saw on the stream at any given point in the server, shall you forget which race is next!", inline=False)
  e.add_field(name="Status", value="The bot now has a brand new status! (peep the sidebar)", inline=False)
  e.add_field(name="Suggestions", value="If you have any suggestion on how to make the bot more useful, don't be afraid to DM <@468685270296952842>, and we'll see what I can do.")
  e.add_field(name="Issues", value="If you experience any issues during the use of the bot, please DM <@468685270296952842> or any of the admins!")
  await ctx.send(embed=e)

@bot.command("lineup")
async def getLineupLink(ctx):
  await ctx.reply("<https://www.f1abeez.com/line-ups>")

@bot.command("dotd")
@commands.has_any_role("Admin", "Moderator")
async def dotdMessage(ctx, *, args):
  await ctx.message.delete()
  try:
    arguments = str(args)
    splitStr = arguments.split(",")
    if(splitStr.__len__() == 11):
      msg = dotdMessageFun(splitStr)
      dcMSG = await ctx.send(msg)
      await dcMSG.add_reaction("1️⃣")
      await dcMSG.add_reaction("2️⃣")
      await dcMSG.add_reaction("3️⃣")   
      await dcMSG.add_reaction("4️⃣")
      await dcMSG.add_reaction("5️⃣")
    elif(splitStr.__len__() > 11):
      await ctx.author.send("Too many arguments provided, please try again")
    elif(splitStr.__len__() < 11):
      await ctx.author.send("Too few arguments provided, please try again")
  except Exception as e:
    print("dotd")
    print(e)

@bot.command("dotdwinner")
@commands.has_any_role("Admin", "Moderator")
async def dotdWinner(ctx, *, args):
  await ctx.message.delete()
  try:
    arguments = str(args)
    arguments = arguments.split(",")
    if(arguments.__len__() == 2):
      tier = arguments[0]
      driver = arguments[1]
      msg = dotdWinnerMsg(tier, driver)
      await ctx.send(msg)
    elif(arguments.__len__() > 2):
        await ctx.author.send("Too many arguments provided, please try again")
    elif(arguments.__len__() < 2):
      await ctx.author.send("Too few arguments provided, please try again")
  except Exception as e:
    print("dotdwinner:")
    print(e)
  

@bot.command("youtube")
async def youtube(ctx):
  await ctx.message.delete()
  try:
    channel = bot.get_channel(info.socialMediaAnnouncementChannel)
    await channel.send("@everyone\n\n**All race replays have now been uploaded to our YouTube Channel!**\n\n Check them out at: <https://www.youtube.com/channel/UCHh_JjzcjQktvEGNVq96_QA>")
  except Exception as e:
    print("youtube")
    print(e)

@bot.command("channelname")
@commands.has_any_role("Admin", "Moderator")
async def channelName(ctx, name):
  nameDic = {"a": "ᴀ","b": "ʙ", "c": "ᴄ", "d":  "ᴅ", "e": "ᴇ", "f":"ꜰ", "g": "ɢ", "h":"ʜ", "i":"ɪ", "j":"ᴊ", "k":"ᴋ", "l":"ʟ", "m":"ᴍ", "n": "ɴ", "o": "ᴏ", "p":"ᴘ", "q":"Q", "r":"ʀ", "s":"ꜱ", "t":"ᴛ", "u":"ᴜ", "v":"ᴠ", "w":"ᴡ", "x":"x", "y":"ʏ", "z":"ᴢ", "-":"-", "0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"}
  returnName = ""
  for i in range(len(name)):
    char = name[i].lower()
    returnName += nameDic.get(char)

  await ctx.reply("︱" + returnName)

## currently unsused, but saved if needed in the future

# @bot.event
# async def on_raw_reaction_add(payload):
#   emoji, user, member, channel = payload.emoji.name, await bot.fetch_user(payload.user_id), payload.member, bot.get_channel(payload.channel_id)
#   message = await channel.fetch_message(payload.message_id)
#   if (emoji == "📨" and user.id != bot.user.id and (channel.id == info.incidentReportChannel or channel.id == info.appealReportChannel or channel.id == suggestionSubmitChannel)):
#     await message.remove_reaction(emoji, member)
#     if(channel.id == info.incidentReportChannel):
#       bst = pytz.timezone("Europe/London")
#       todayInc = datetime.datetime.now(tz=bst).isoformat()
#       def check(m):
#         return m.author == user and m.guild is None 

#       def checkRaw(u):
#         return u.user_id == user.id and u.guild_id is None
      
#       await channel.send(f"Please follow the bot to your DMs to report your incident <@{user.id}>", delete_after=60)

#       try:
#           await user.send("What is your gamertag?")
#           gamertagOfUserInc = await bot.wait_for("message", check=check, timeout=180.0)
#           gamertagOfUserInc = gamertagOfUserInc.content
#           await user.send("Please describe your incident.")
#           descriptionInc = await bot.wait_for("message", check=check, timeout=180.0)
#           descriptionInc = descriptionInc.content
#           tierOfIncidentMSG =  await user.send("What is the tier or division this incident/penalty occured in? \n1️⃣ = F1 - Tier 1\n2️⃣ = F1 - Tier 2\n3️⃣ = F1 - Tier 3\n4️⃣ = F1 - Tier Mixed\n5️⃣ = F2\nPlease react with the corresponding tier")
#           await tierOfIncidentMSG.add_reaction("1️⃣")
#           await tierOfIncidentMSG.add_reaction("2️⃣")
#           await tierOfIncidentMSG.add_reaction("3️⃣")
#           await tierOfIncidentMSG.add_reaction("4️⃣")
#           await tierOfIncidentMSG.add_reaction("5️⃣")
#           tierOfIncidentReaction = await bot.wait_for("raw_reaction_add", check=checkRaw, timeout=180.0)
#           if(str(tierOfIncidentReaction.emoji) == "1️⃣"):
#             tierOfIncidentInc = "F1 - Tier 1"
#             await user.send("You chose "+tierOfIncidentInc)
#           elif(str(tierOfIncidentReaction.emoji) == "2️⃣"):
#             tierOfIncidentInc = "F1 - Tier 2"
#             await user.send("You chose "+tierOfIncidentInc)
#           elif(str(tierOfIncidentReaction.emoji) == "3️⃣"):
#             tierOfIncidentInc = "F1 - Tier 3"
#             await user.send("You chose "+tierOfIncidentInc)
#           elif(str(tierOfIncidentReaction.emoji) == "4️⃣"):
#             tierOfIncidentInc = "F1 - Tier Mixed"
#             await user.send("You chose "+tierOfIncidentInc)
#           elif(str(tierOfIncidentReaction.emoji) == "5️⃣"):
#             tierOfIncidentInc = "F2"
#             await user.send("You chose "+tierOfIncidentInc)
#           await user.send("Please provide video evidence (Only reply with links to gamerdvr or other services)")
#           evidenceInc = await bot.wait_for("message", check=check, timeout=180.0)
#           evidenceInc = evidenceInc.content
#           await user.send("What lap did this incident/penalty occur on?")
#           lapOfIncidentInc = await bot.wait_for("message", check=check, timeout=180.0)
#           lapOfIncidentInc = lapOfIncidentInc.content
#           await user.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
#           gamertagOfInvolevedDriverInc = await bot.wait_for("message", check=check, timeout=180.0)
#           gamertagOfInvolevedDriverInc = gamertagOfInvolevedDriverInc.content
#       except asyncio.TimeoutError:
#           await user.send("Unfortunately you took too long to reply (Limit is three minutes per message). Please start a new incident if you want to proceed.")
#       response = submitAnIncident(gamertagOfUserInc, lapOfIncidentInc, descriptionInc, tierOfIncidentInc, evidenceInc, gamertagOfInvolevedDriverInc, todayInc)
#       logEmbed = nextcord.Embed(title="⚠️New Ticket has been reported!⚠️")
#       logEmbed.add_field(name="Tier", value=tierOfIncidentInc, inline=False)
#       logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserInc} vs {gamertagOfInvolevedDriverInc}", inline=False)
#       channel = bot.get_channel(info.incidentLogChannel)
#       await channel.send(embed = logEmbed)
#       await user.send(response)
    
#     if(channel.id == info.appealReportChannel):
#       bst = pytz.timezone("Europe/London")
#       todayApp = datetime.datetime.now(tz=bst).isoformat()
#       def check(m):
#         return m.author == user and m.guild is None 
        
#       await channel.send(f"Please follow the bot to your DMs to submit your appeal <@{user.id}>", delete_after=60)
#       try:
#           await user.send("What is the case number you want to appeal (use ;querytickets in the bot channel in the server if you need to get it)")
#           caseNumberApp = await bot.wait_for("message", check=check, timeout=180.0)
#           caseNumberApp = caseNumberApp.content
#           await user.send("What is your gamertag?")
#           gamertagOfUserApp = await bot.wait_for("message", check=check, timeout=180.0)
#           gamertagOfUserApp = gamertagOfUserApp.content
#           await user.send("Please state the reason for you appeal.")
#           reasonApp = await bot.wait_for("message", check=check, timeout=180.0)
#           reasonApp = reasonApp.content
#           await user.send("State any additional information to support your appeal (if you don't have any, reply with N/A)")
#           additionalInfoApp = await bot.wait_for("message", check=check, timeout=180.0)
#           additionalInfoApp = additionalInfoApp.content
#           await user.send("Please provide addition video evidence to support your appeal (Only reply with links to gamerdvr or other services)")
#           evidenceApp = await bot.wait_for("message", check=check, timeout=180.0)
#           evidenceApp = evidenceApp.content
#           await user.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
#           gamertagOfInvolevedDriverApp = await bot.wait_for("message", check=check, timeout=180.0)
#           gamertagOfInvolevedDriverApp = gamertagOfInvolevedDriverApp.content
#       except asyncio.TimeoutError:
#           await user.send("Unfortunately you took too long to reply (Limit is a three minutes per message). Please start a new incident if you want to proceed.")
#       response = submitAppeal(caseNumberApp, evidenceApp, gamertagOfUserApp, gamertagOfInvolevedDriverApp, reasonApp, additionalInfoApp, todayApp)
#       logEmbed = nextcord.Embed(title="⚠️New Appeal has been submitted!⚠️")
#       logEmbed.add_field(name="Case Number", value=caseNumberApp, inline=False)
#       logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserApp} vs {gamertagOfInvolevedDriverApp}", inline=False)
#       channel = bot.get_channel(info.incidentLogChannel)
#       await channel.send(embed = logEmbed)
#       await user.send(response)
#     if(channel.id == suggestionSubmitChannel):
#       await channel.send(f"Please follow the bot to your DMs to submit your suggestion <@{user.id}>", delete_after=60)
#       def check(m):
#         return m.author == user and m.guild is None 
#       try:
#         await user.send("Please type your suggestion here, the admins will have a look at it as soon as possible. Thank you, Admins of F1ABEEZ")
#         suggestion = await bot.wait_for("message", check=check, timeout=300.0)
#         suggestion = suggestion.content
#       except asyncio.TimeoutError:
#         await user.send("Unfortunately you took too long. The limit is 5 minutes per message")

#       suggestionLogEmbed = nextcord.Embed(title="🚨A new suggestion has been submitted🚨")
#       suggestionLogEmbed.add_field(name="**Submitted by:**", value=user.display_name, inline=False)
#       suggestionLogEmbed.add_field(name="**Suggestion**", value=suggestion, inline=False)
#       channel = bot.get_channel(suggestionLogChannel)
#       await channel.send(embed = suggestionLogEmbed)
#       await user.send("Your suggestion has been submitted to the admins!")

bot.run(info.discord_token)