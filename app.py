import asyncio
from time import sleep
import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound
import requests
import datetime
import pytz
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import utils.notion as nt
import utils.info as info
import utils.utilities as utils
import logging
from nextcord import Interaction, Member

logging.basicConfig(format='%(asctime)s-%(levelname)s:%(message)s', level=logging.INFO)


class TierDropdown(nextcord.ui.Select):
  def __init__(self):
    options = [
      nextcord.SelectOption(label="Tier 1",description="F1 - Tier 1" ,value="Tier 1"),
      nextcord.SelectOption(label="Tier 2",description="F1 - Tier 2" ,value="Tier 2"),
      nextcord.SelectOption(label="Tier 3",description="F1 - Tier 3" ,value="Tier 3"),
      nextcord.SelectOption(label="Tier 4",description="F1 - Tier 4" ,value="Tier 4"),
      nextcord.SelectOption(label="Tier 5",description="F1 - Tier 5" ,value="Tier 5"),
      nextcord.SelectOption(label="Tier M",description="F1 - Tier M" ,value="Tier M"),
      nextcord.SelectOption(label="Tier H",description="F1 - Tier H" ,value="Tier H"),
      nextcord.SelectOption(label="F2 - Tier 1",description="F2 - Tier 1" ,value="F2 - Tier 1"),
      nextcord.SelectOption(label="F2 - Tier 2",description="F2 - Tier 2" ,value="F2 - Tier 2"),
    ]
    super().__init__(placeholder="Select your tier...", min_values=1, max_values=1, options=options)

  async def callback(self, interaction: nextcord.Interaction):
    self.tierSelected = self.values[0]
class DropdownTierView(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.dropdown = TierDropdown()
    self.add_item(self.dropdown)

  @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green, row=1)
  async def confirm(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.tierSelected = self.dropdown.tierSelected
    self.stop()

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

class highlightMenu(nextcord.ui.View):
  def __init__(self):
      super().__init__(timeout=None)

  async def handle_highlight(self, button, interaction):
    bst = pytz.timezone("Europe/London")
    todayInc = datetime.datetime.now(tz=bst).isoformat()
    user = interaction.user
    await interaction.response.send_message(f"Follow the bot to your DMs! {user.mention}", ephemeral=True)
    def check(m):
      return m.author == user and m.guild is None 

    try:
      await user.send("What round did this highlight occur in?")
      rnd = await bot.wait_for('message', check=check, timeout=180.0)
      rnd = rnd.content
      await user.send("What is the link to your highlight?")
      link = await bot.wait_for("message", check=check, timeout=180.0)
      link = link.content
      await user.send("If this is a clip enter \"Clip\" othervise enter the timestamp or the lap of the highlight")
      time = await bot.wait_for("message", check=check, timeout=180.0)
      time = time.content
      await user.send("Give us a brief description of the highlight")
      desc = await bot.wait_for("message", check=check, timeout=180.0)
      desc = desc.content
      view = DropdownTierView()
      await user.send("In which tier did this highlight occur?", view=view)
      await view.wait()
      tier = view.tierSelected
      await user.send(f"You selected {tier}")
      response = nt.submitHighlight(rnd, link, time, desc, tier, todayInc, user.name)
      await user.send(response)
    except asyncio.TimeoutError:
      await user.send("You took too long to respond. Try again.")

  @nextcord.ui.button(label="", emoji="📸", style=nextcord.ButtonStyle.primary, custom_id="highlightButton")
  async def highlightButtonClicked(self, button, interaction):
    await self.handle_highlight(button, interaction)


class reportMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  async def handle_click(self, button, interaction):
    user = interaction.user
    channel = interaction.channel
    if(interaction.channel_id == info.get_channelID(interaction.guild_id, "incidentReportChannel")):
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

          view = DropdownTierView()
          await user.send("Select in which tier did the incident occur", view=view)
          await view.wait()
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
          channel = bot.get_channel(info.get_channelID(interaction.guild_id, "incidentLogChannel"))
          await channel.send(embed = logEmbed)
          await user.send(response)
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("incident report:")
        print(e)
      


    if(interaction.channel.id == info.get_channelID(interaction.guild_id, "appealReportChannel")):
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
          channel = bot.get_channel(info.get_channelID(interaction.guild_id, "incidentLogChannel"))
          await channel.send(embed = logEmbed)
          await user.send(response)
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is a three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("Appeal:")
        print(e)
      


    if(interaction.channel.id == info.get_channelID(interaction.guild_id, "suggestionSubmitChannel")):
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
      channel = bot.get_channel(info.get_channelID(interaction.guild_id, "suggestionLogChannel"))
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
bot.allowed_mentions = nextcord.AllowedMentions(everyone=True, users=True, roles=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    logging.info("We have logged in as {0.user}".format(bot))
    bot.add_view(reportMenu())
    bot.add_view(highlightMenu())
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="The F1AB Family 🚀"))

@bot.slash_command(name="help", description="Shows the help menu", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def HelpCommand(interaction: Interaction):
    await interaction.send(embed = GetHelpCommand())

@bot.slash_command(name="staffhelp", description="Shows the staff help menu", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def StaffHelpCommand(interaction: Interaction):
  await interaction.response.defer()
  if(utils.check_roles(interaction.user.roles, ["Staff"])):
    await interaction.send(embed = getStaffHelpCommand())
  else:
    await interaction.send("You do not have permission to use this command!")

@bot.slash_command(name="gettickets", description="Gets the tickets for the gamertag", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def GetTickets(interaction: Interaction, gamertag: str = SlashOption(name="gamertag", description="The gamertag to get the tickets for", required=True)):
    await interaction.response.defer()
    await interaction.send(embed=nt.queryTickets(gamertag))

@bot.slash_command(name="getprofile", description="Gets profile info from the database", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def GetProfile(interaction: Interaction, gamertag: str = SlashOption(name="gamertag", description="The gamertag to get the tickets for", required=True)):
    await interaction.response.defer()
    await interaction.send(embed=nt.getProfileInfo(gamertag))    

@bot.slash_command(name="getappeals", description="Gets the appeals for the gamertag", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def GetAppeals(interaction: Interaction, gamertag: str = SlashOption(name="gamertag", description="The gamertag to get the tickets for", required=True)):
  await interaction.response.defer()
  await interaction.send(embed = nt.queryAppeals(gamertag))

@bot.slash_command(name="ticketdetail", description="Gets the details for the ticket", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def TicketDetail(interaction: Interaction, ticketID: str = SlashOption(name="ticketid", description="The ticket ID to get the details for", required=True)):
    await interaction.response.defer()
    await interaction.send(embed = nt.TicketDetailQuery(ticketID))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found")
    logging.error(error)

@bot.slash_command(name="warn", description="Warns a user", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
@commands.has_any_role("Admin")
async def warn(interaction: Interaction, user: Member = SlashOption(name="user", description="The user to warn", required=True), reason: str = SlashOption(name="reason", description="The reason for the warning", required=True)):
  await interaction.response.defer()
  if(utils.check_roles(interaction.user.roles, ["Admin"])):
    member = await interaction.guild.fetch_member(user.id)
    embed = nextcord.Embed(title="A Warning has been issued", color=info.color)
    embed.add_field(name="User", value=member.name, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    channel = bot.get_channel(info.get_channelID(interaction.guild.id, "warningChannel"))
    await channel.send(embed = embed)
    await interaction.send(embed = embed)   
  else:
    await interaction.send("You do not have permission to use this command!")

@bot.slash_command(name="ban", description="Bans a user", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
@commands.has_any_role("Admin")
async def ban(interaction: Interaction, user: Member = SlashOption(name="user", description="The user to ban", required=True), reason: str = SlashOption(name="reason", description="The reason for the ban", required=True)):
  await interaction.response.defer()
  if(utils.check_roles(interaction.user.roles, ["Admin"])):
    member = await interaction.guild.fetch_member(user.id)
    embed = nextcord.Embed(title="A Ban has been issued", color=info.color)
    embed.add_field(name="User", value=member.name, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    channel = bot.get_channel(info.get_channelID(interaction.guild.id, "banChannel"))
    await channel.send(embed = embed)
    await member.ban(reason = reason)
    await interaction.send(embed = embed)   
  else:
    await interaction.send("You do not have permission to use this command!")
    
@bot.event
async def on_member_join(member):
  serverID = member.guild.id
  if(member.guild.id == int(info.f1abeezID)):
    role = nextcord.utils.get(member.guild.roles, name="Academy Driver")
    await member.add_roles(role)
  elif(member.guild.id == int(info.f2abeezID)):
    role = nextcord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(role)
  channel = bot.get_channel(info.get_channelID(serverID, "welcomeChannel"))
  if(type(channel) != type(None)):
    if(member.guild.id == int(info.f1abeezID)):
      await channel.send(f"**Welcome {member.mention}**\n\nPlease use this chat if you have any questions and someone will be on hand.\n\nAll the information you need is on <#865379267977412618>")
    elif(member.guild.id == int(info.f2abeezID)):
      await channel.send(f"Welcome to F2ABEEZ!{member.mention}\n\nYour dedicated F2 racing discord community. Please read <#937998062842957824> to get equated with our brand and information then, head over to <#937997355737833482> to get a seat in the next race that suits your pace! Please **put your gamertag into brackets behind your discord name**, thank you!")
  else:
    logging.error("welcomeChannel not found")

@bot.event
async def on_member_remove(member):
  memberName = member.name
  memberRole = member.roles
  channel = bot.get_channel(info.get_channelID(member.guild.id, "leavingChannel"))
  profilesChannel = bot.get_channel(info.get_channelID(member.guild.id, "profilesChannel"))
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

@bot.command(name="highlightchannel")
@commands.has_any_role("Admin", "Moderator")
async def highlightChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Submit a highlight",description="React to this message to submit a highlight by clicking the 📸 button", color=info.color)
  await ctx.send(embed=embed, view=highlightMenu())

@bot.slash_command(name="calendar", description="Shows the current calendar", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
async def getCalendar(interaction):
  await interaction.response.defer()
  if(int(info.f1abeezID) == interaction.guild.id):
    try:
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=102%3A367&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      img = r["images"]["102:367"]
      embed1 = nextcord.Embed(color=info.color) 
      embed1.set_image(url=img) 
      await interaction.send(embed=embed1)
    except Exception as e:
      await interaction.send(f"There was an error getting the calendar, please report this issue to the admins.")
      print("calendar:")
      print(e)
  elif(int(info.f2abeezID) == interaction.guild.id):
    try:
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=125%3A2&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      img = r["images"]["125:2"]
      embed2 = nextcord.Embed(color=info.color) 
      embed2.set_image(url=img) 
      await interaction.send(embed=embed2)
    except Exception as e:
      await interaction.send(f"There was an error getting the calendar, please report this issue to the admins.")
      print("calendar:")
      print(e)


@bot.slash_command(name="standings", description="Shows the current standings", guild_ids=[int(info.testServerID), int(info.f1abeezID)])
async def getStandings(interaction: Interaction, tier: str = SlashOption(name="tier", description="The tier to get the standings for", choices={"Tier 1": "1", "Tier 2": "2", "Tier 3": "3", "Tier 4": "4", "Tier M": "M", "Tier H": "H", "Team Standings": "team", "F2 - Tier 1": "f21", "F2 - Tier 2": "f22"})):
  await interaction.response.defer()
  try:
    if(tier == "1"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["2:16"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "2"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=406%3A667&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["406:667"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "3"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A265&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["4:265"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "4"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=406%3A999&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["406:999"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "M"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=406%3A1251&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["406:1251"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "H"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=436%3A2&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["436:2"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "team"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=16%3A1142&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["16:1142"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "f21"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=421%3A168&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["421:168"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
    elif(tier == "f22"):
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
      r = r.json()
      url = r["images"]["2:16"]
      e = nextcord.Embed(color=info.color) 
      e.set_image(url=url) 
      await interaction.send(embed=e)
  except KeyError:
    await interaction.send("There was an error while getting the standings. Please report this issue to the admins")
    print(KeyError)
  except Exception as e:
    print("standings:")
    print(e)

@bot.slash_command(name="lineup", description="Get the current lineup", guild_ids=[int(info.f1abeezID),  int(info.f2abeezID), int(info.testServerID)])
async def getLineupLink(interaction: Interaction):
  await interaction.response.send_message("<https://www.f1abeez.com/line-ups>")

@bot.slash_command(name="channelname", description="Gets the channel name in correct font", guild_ids=[int(info.f1abeezID),  int(info.f2abeezID), int(info.testServerID), int(info.f1abeezEsportsID)])
async def channelName(interaction: Interaction, channelName: str = SlashOption(name="channelname", description="The channel name", required=True)):
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

@bot.slash_command(name="clearchannel", description="Clears a channel without the pinned messages", guild_ids=[int(info.f1abeezID),  int(info.f2abeezID), int(info.testServerID), int(info.f1abeezEsportsID)])
async def clearChannel(interaction: Interaction):
  if(utils.check_roles(interaction.user.roles, ["Admin", "Moderator"])):
    await interaction.response.defer()
    def check(m: nextcord.Message):
      return m.pinned == False
    await interaction.channel.purge(check=check)
  else:
    await interaction.send("You do not have permission to use this command!")

@bot.slash_command(name="sendacademydm", description="Sends a DM to the academy", guild_ids=[int(info.f1abeezID),  int(info.f2abeezID), int(info.testServerID), int(info.f1abeezEsportsID)])
async def sendAcademyDM(interaction: Interaction):
  if(utils.check_roles(interaction.user.roles, ["Admin", "Moderator"])):
    await interaction.response.defer()
    role: nextcord.Role = interaction.guild.get_role(info.get_roleID(interaction.guild_id, "academyRole"))
    inboxChannel: nextcord.TextChannel = bot.get_channel(870004492639301692)
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


for fn in os.listdir("./cogs"):
  if fn.endswith(".py"):
    logging.info("Loading %s", fn)
    bot.load_extension(f"cogs.{fn[:-3]}")

bot.run(info.discord_token)