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

discord_token = os.environ.get("discord_token")
token = os.environ.get("token")
incidentDatabaseURL = os.environ.get("incidentDatabaseURL")
profileDatabaseURL = os.environ.get("profileDatabaseURL")
incidentDatabaseId = os.environ.get("incidentDatabaseId")
appealsDatabaseURL = os.environ.get("appealsDatabaseURL")
appealsDatabaseId = os.environ.get("appealsDatabaseId")
mongoDBConnSTR = os.environ.get("mongoDBConnSTR")
figmaToken = os.environ.get("figma_token")
    
color = 16236412
warningChannel = 853679513406013460
welcomeChannel = 838841316519313408
stewardsAnnoucementChannel = 864564506368933888
generalAnnoucementChannel = 774696889424805891
incidentReportChannel = 871334405359144970
appealReportChannel = 871334445716766800
suggestionSubmitChannel = 877977932914651176
incidentLogChannel = 861939856481189908
suggestionLogChannel = 877979327273246772
leavingChannel = 774605933661257729

tier1Role = 795227294766727169
reserveTier1Role = 813715392031752223
tier2Role = 795227317684928546
reserveTier2Role = 813715709292838942
tier3Role = 813703851349245965
reserveTier3Role = 813715758793228319
tierMRole = 840694396990521364
reserveTierMRole = 850433806246871102
academyRole = 774740889557270539

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
  
  @nextcord.ui.button(label="Nations League", style=nextcord.ButtonStyle.primary, custom_id="Nations_League")
  async def tier2ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)

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
    elif(str(button.custom_id) == "Tier_M"):
      self.tierSelected = "F1 - Tier Mixed"
      self.stop()
    elif(str(button.custom_id) == "F2"):
      self.tierSelected = "F2"
      self.stop()

  @nextcord.ui.button(label="Tier 1", style=nextcord.ButtonStyle.primary, custom_id="Tier_1")
  async def tier1ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)
  
  @nextcord.ui.button(label="Tier 2", style=nextcord.ButtonStyle.primary, custom_id="Tier_2")
  async def tier2ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)

  @nextcord.ui.button(label="Tier 3", style=nextcord.ButtonStyle.primary, custom_id="Tier_3")
  async def tier3ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)

  @nextcord.ui.button(label="Tier Mixed", style=nextcord.ButtonStyle.primary, custom_id="Tier_M")
  async def tiermButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)

  @nextcord.ui.button(label="F2", style=nextcord.ButtonStyle.primary, custom_id="F2", disabled=True)
  async def f2ButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)

class reportMenu(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  async def handle_click(self, button, interaction):
    user = interaction.user
    channel = interaction.channel
    if(interaction.channel_id == incidentReportChannel):
      bst = pytz.timezone("Europe/London")
      todayInc = datetime.datetime.now(tz=bst).isoformat()
      def check(m):
        return m.author == user and m.guild is None 

      def checkRaw(u):
        return u.user_id == user.id and u.guild_id is None
      
      await interaction.response.send_message(f"Please follow the bot to your DMs to report your incident <@{user.id}>")

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
          elif(view.tierSelected == "F1 - Tier Mixed"):
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
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("incident report:")
        print(e)
      response = submitAnIncident(gamertagOfUserInc, lapOfIncidentInc, descriptionInc, tierOfIncidentInc, evidenceInc, gamertagOfInvolevedDriverInc, todayInc)
      logEmbed = nextcord.Embed(title="⚠️New Ticket has been reported!⚠️")
      logEmbed.add_field(name="Tier", value=tierOfIncidentInc, inline=False)
      logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserInc} vs {gamertagOfInvolevedDriverInc}", inline=False)
      channel = bot.get_channel(incidentLogChannel)
      await channel.send(embed = logEmbed)
      await user.send(response)
      await interaction.delete_original_message()


    if(interaction.channel.id == appealReportChannel):
      bst = pytz.timezone("Europe/London")
      todayApp = datetime.datetime.now(tz=bst).isoformat()
      def check(m):
        return m.author == user and m.guild is None 
        
      await interaction.response.send_message(f"Please follow the bot to your DMs to submit your appeal <@{user.id}>")
      try:
          await user.send("What is the case number you want to appeal (use ;querytickets in the bot channel in the server if you need to get it)")
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
      except asyncio.TimeoutError:
          await user.send("Unfortunately you took too long to reply (Limit is a three minutes per message). Please start a new incident if you want to proceed.")
      except Exception as e:
        print("Appeal:")
        print(e)
      response = submitAppeal(caseNumberApp, evidenceApp, gamertagOfUserApp, gamertagOfInvolevedDriverApp, reasonApp, additionalInfoApp, todayApp)
      logEmbed = nextcord.Embed(title="⚠️New Appeal has been submitted!⚠️")
      logEmbed.add_field(name="Case Number", value=caseNumberApp, inline=False)
      logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUserApp} vs {gamertagOfInvolevedDriverApp}", inline=False)
      channel = bot.get_channel(incidentLogChannel)
      await channel.send(embed = logEmbed)
      await user.send(response)
      await interaction.delete_original_message()


    if(interaction.channel.id == suggestionSubmitChannel):
      await interaction.response.send_message(f"Please follow the bot to your DMs to submit your suggestion <@{user.id}>")
      def check(m):
        return m.author == user and m.guild is None 
      try:
        await user.send("Please type your suggestion here, the admins will have a look at it as soon as possible. Thank you, Admins of F1ABEEZ")
        suggestion = await bot.wait_for("message", check=check, timeout=300.0)
        suggestion = suggestion.content
      except asyncio.TimeoutError:
        await user.send("Unfortunately you took too long. The limit is 5 minutes per message")
      except Exception as e:
        print("suggestion:")
        print(e)

      suggestionLogEmbed = nextcord.Embed(title="🚨A new suggestion has been submitted🚨")
      suggestionLogEmbed.add_field(name="**Submitted by:**", value=user.display_name, inline=False)
      suggestionLogEmbed.add_field(name="**Suggestion**", value=suggestion, inline=False)
      channel = bot.get_channel(suggestionLogChannel)
      await channel.send(embed = suggestionLogEmbed)
      await user.send("Your suggestion has been submitted to the admins!")
      await interaction.delete_original_message()

  @nextcord.ui.button(label="", emoji="📨", style=nextcord.ButtonStyle.primary, custom_id="id")
  async def reportButtonClicked(self, button, interaction):
    await self.handle_click(button, interaction)


def queryTickets(gamertag):
    zprava = ""
    header = {"Authorization": token, "Notion-Version": "2021-05-13"}
    r = requests.post(incidentDatabaseURL, json = {
      "filter": {
  "or": [
    {
      "property": "Reported By",
      "rich_text": {
        "contains": gamertag
      }
    },
    {
      "property": "GamerTag(s) of Driver(s) involved incident (N/A for penalties)",
      "rich_text": {
        "contains": gamertag
      }
    }
  ]
      },
  "sorts": [{ "property": "Case Number", "direction": "ascending" }]}

    , headers=header).text

    embed = nextcord.Embed(title=f"Tickets where {gamertag} was involved", color=color)

    b = json.loads(r)

    if (len(b["results"]) == 0):
        embed.add_field(name="Error", value="Gamertag is incorrect, please try again.")
        return embed

    for i in range(len(b["results"])):
        url = b["results"][i]["url"]
        url = "https://f1abeez.com/" + url[22:]
        url = f"[LINK]({url})"
        try: 
            caseNumber = b["results"][i]["properties"]["Case Number"]["title"][0]["plain_text"]
        except IndexError:
            caseNumber = "Case number hasn't been assigned yet (you cannot get this ticket with the bot until it has a case number)"
        except Exception as e:
          print("appeal method:")
          print(e)
        driversInvolved = (f'{b["results"][i]["properties"]["Reported By"]["rich_text"][0]["text"]["content"]} vs {b["results"][i]["properties"]["GamerTag(s) of Driver(s) involved incident (N/A for penalties)"]["rich_text"][0]["text"]["content"]} {url}\n')
        embed.add_field(name=caseNumber, value=driversInvolved, inline=False)

    return embed

def TicketDetailQuery(ticketNumber):
    header = {"Authorization": token,  "Notion-Version": "2021-05-13"}
    req = requests.post(incidentDatabaseURL, json = {
        "filter": {
        "property": "Case Number",
        "title": {
            "contains": ticketNumber
        }
        }
        }
        , headers=header).text

    c = json.loads(req)
    embed=nextcord.Embed(title="Incident Detail", color=color)
    try:
        ticketNumber = c["results"][0]["properties"]["Case Number"]["title"][0]["text"]["content"]
    except IndexError:
        embed.add_field(name="Error", value="This ticket does not exist in our database.")
        return embed
    except Exception as e:
      print("ticket detail query:")
      print(e)
    try: 
      actionTaken = c["results"][0]["properties"]["Action(s) Taken"]["rich_text"][0]["plain_text"]
    except IndexError:
      actionTaken = "Not specified"
    except Exception as e:
      print("ticket detail query:")
      print(e)
    driversInvolved = f'{c["results"][0]["properties"]["Reported By"]["rich_text"][0]["text"]["content"]} vs {c["results"][0]["properties"]["GamerTag(s) of Driver(s) involved incident (N/A for penalties)"]["rich_text"][0]["text"]["content"]}'
    status = c["results"][0]["properties"]["Status"]["select"]["name"]
    url = c["results"][0]["url"]
    url = "https://f1abeez.com/" + url[22:]
    description = c["results"][0]["properties"]["Description"]["rich_text"][0]["text"]["content"]

    embed.add_field(name="Status", value=str(status), inline=False)
    embed.add_field(name="Ticket Number", value=str(ticketNumber), inline=True)
    embed.add_field(name="Drivers Involved", value=str(driversInvolved), inline=True)
    embed.add_field(name="Description", value=str(description), inline=False)
    embed.add_field(name="Action Taken", value=str(actionTaken), inline=False)
    embed.add_field(name="Link", value=str(url), inline=False)


    return embed    

def queryAppeals(gamertag):
  header = {"Authorization": token, "Notion-Version": "2021-05-13"}
  r = requests.post(appealsDatabaseURL, json = {
      "filter": {
  "or": [
    {
      "property": "Appealed By",
      "rich_text": {
        "contains": gamertag
      }
    },
    {
      "property": "GamerTag(s) involved",
      "rich_text": {
        "contains": gamertag
      }
    }
  ]
      },
  "sorts": [{ "property": "AP-Case Number", "direction": "ascending" }]}

    , headers=header).text
  

  embed = nextcord.Embed(title=f"Appeals where {gamertag} was involved", color=color)

  b = json.loads(r)
  if (len(b["results"]) == 0):
      embed.add_field(name="Error", value="Gamertag is incorrect, please try again.")
      return embed

  for i in range(len(b["results"])):
      url = b["results"][i]["url"]
      url = "https://f1abeez.com/" + url[22:]
      url = f"[LINK]({url})"
      try: 
          caseNumberAndStatus = f'{b["results"][i]["properties"]["AP-Case Number"]["title"][0]["text"]["content"]} - {b["results"][i]["properties"]["Status"]["select"]["name"]}'
      except IndexError:
          caseNumberAndStatus = "Case number hasn't been assigned yet (you cannot get this ticket with the bot until it has a case number)"
      except KeyError:
          caseNumberAndStatus = "The stewards haven't got to the appeal yet, please check back later"
      except Exception as e:
        print("appeal query:")
        print(e)
      driversInvolved = (f'{b["results"][i]["properties"]["Appealed By"]["rich_text"][0]["text"]["content"]} vs {b["results"][i]["properties"]["GamerTag(s) involved"]["rich_text"][0]["text"]["content"]} {url}\n')
      embed.add_field(name=caseNumberAndStatus, value=driversInvolved, inline=False)
  
  return embed  

def submitAppeal(caseNumber, evidence, gamertag, gamertagInvolved, reason, additionalInfo, date):
  url = "https://api.notion.com/v1/pages/"
  header = {"Authorization": token, "Notion-Version": "2021-05-13"}
  r = requests.post(url, headers=header, json={
  "parent": {
    "database_id": appealsDatabaseId
  },
  "properties": {
    "Case Number": {
      "rich_text": [
        {
          "text": {
            "content": caseNumber
          }
        }
      ]
    },
  "Status": {
    "select": {
      "name": "In Progress",
      "color": "pink"
    }
  },
  "Additional Evidence": {
    "rich_text": [
      {
        "text": {
          "content": evidence
        }
      }
    ]
  },
  "Appealed By": {
    "rich_text": [
      {
        "text": {
          "content": gamertag
        }
      }
    ]
  },
  "GamerTag(s) involved": {
    "rich_text": [
      {
        "text": {
          "content": gamertagInvolved
        }
      }
    ]
  },
  "Reason": {
    "rich_text": [
      {
        "text": {
          "content": reason
        }
      }
    ]
  },
  "Additional Info": {
    "rich_text": [
      {
        "text": {
          "content": additionalInfo
        }
      }
    ]
  },
    "Time Reported": {
        "date": {
                "start": date
            }
    },
    "Submitted Through": {
      "select": {
        "name": "F1ABEEZ Bot",
        "color": "pink"
      }
    }
  }
}
)
  if(r.status_code == 200):
    return "Your appeal was successfully submitted!"
  else:
    print(r.text)
    return "There was an error submitting your appeal, please reach out to the admin team"


def GetHelpCommand():
    embed = nextcord.Embed(title="Help", color=color)
    embed.add_field(name=";standings", value="This command gives you a menu to select the tier of which you want to see standings and then it returns them in the channel.", inline=False)
    embed.add_field(name=";calendar", value="This command gives you a selection of the F1 or Nations League calendar and then sends it in the channel.", inline=False)
    embed.add_field(name=";gettickets <gamertag>", value="This command is useful when you don’t know the number of your ticket. The command lists all tickets you’ve been involved (whether you reported it or someone else reported you) and gives you the number of the ticket and the direct link to the website.", inline=False)
    embed.add_field(name=";getappeals <gamertag>", value="This command gets you a list of appeals you've been involeved in (whether you appealed or someone appealed against you) and gives you the number of the appeal, a direct link to the website and the status of the appeal.")
    embed.add_field(name=";ticketdetail <number of ticket>", value="This command gets you the details of ticket you provide. It lists the status, penalty that was awarded and who was involved.", inline=False)
    embed.add_field(name=";incidentreport", value="This command allows you to submit an incident from nextcord. Please read the messages carefully and reply correctly.", inline=False)
    embed.add_field(name=";submitappeal", value="This command allows you to submit an appeal to a decision that has been made by the stewards. Please use ;gettickets before you start submitting it to make sure you know the case number of the incident you want to appeal", inline=False)
    return embed

def submitAnIncident(gamertag, lap, description, tier, evidence, driverInvolved, date):
    url = "https://api.notion.com/v1/pages/"
    header = header = {"Authorization": token, "Notion-Version": "2021-05-13"}
    r = requests.post(url, headers=header, json={
  "parent": {
    "database_id": incidentDatabaseId
  },
  "properties": {
    "Description": {
      "rich_text": [
        {
          "text": {
            "content": description
          }
        }
      ]
    },
    "Status": {
      "select": {
        "name": "In Progress",
        "color": "red"
      }
    },
    "Tier/Division": {
      "select": {
        "name": tier
      }
    },
    "Video Evidence (other video sources are allowed)": {
      "rich_text": [
        {
          "text": {
            "content": evidence
          }
        }
      ]
    },
    "Lap of incident/penalty": {
      "rich_text": [
        {
          "text": {
            "content": lap
          }
        }
      ]
    },
    "Reported By": {
      "rich_text": [
        {
          "text": {
            "content": gamertag
          }
        }
      ]
    },
    "GamerTag(s) of Driver(s) involved incident (N/A for penalties)": {
      "rich_text": [
        {
          "text": {
            "content": driverInvolved
          }
        }
      ]
    },
    "Time Reported": {
        "date": {
                "start": date
            }
    },
    "Submitted through": {
      "select": {
        "name": "F1ABEEZ Bot",
        "color": "pink"
      }
    }
  }
}
)
    if(r.status_code == 200):
        return "Your ticket was successfully submitted!"
    else:
        print(r.text)
        return "There was an error submitting your ticket, please reach out to the admin team"

intents = nextcord.Intents.default()
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix=";", help_command=None, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    bot.add_view(reportMenu())
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="F1ABEEZ Server 🚀"))

@bot.command(name="help")
async def HelpCommand(ctx):
    await ctx.send(embed = GetHelpCommand())

@bot.command(name="gettickets")
async def GetTickets(ctx, *, arg):
    await ctx.send(embed=queryTickets(arg))

@bot.command(name="getappeals")
async def GetAppeals(ctx, *, arg):
  await ctx.send(embed = queryAppeals(arg))

@bot.command(name="ticketdetail")
async def TicketDetail(ctx, ticketNum):
    await ctx.send(embed = TicketDetailQuery(ticketNum))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found")
    print(error)

@bot.command(name="lobbytier1")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier1(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier1Role}> <@&{reserveTier1Role}>\n**Lobby is now open!**\nPlease join off <@805472151914283079>\nGamertag is - Playzz769\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier2")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier2(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier2Role}> <@&{reserveTier2Role}>\n**Lobby is now open!**\nPlease join off <@483678704749510677>\nGamertag is - VRA Harveyy\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier3")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier3(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier3Role}> <@&{reserveTier3Role}>\n**Lobby is now open!**\nPlease join off <@401204069890523137>\nGamertag is - OwningLeMoNz\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier4")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier4(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tierMRole}> <@&{reserveTierMRole}>\n**Lobby is now open!**\nPlease join off <@705761570126561341>\nGamertag is - Sammie230408\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbyf2")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGf2(ctx):
  await ctx.message.delete()
  await ctx.send("**Lobby is now open!**\nPlease join off <@499568806469959691>\nGamertag is - MrJSmithy\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="readytier1")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier1(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier1Role}> <@&{reserveTier1Role}>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

@bot.command(name="readytier2")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier2(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier2Role}> <@&{reserveTier2Role}>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

@bot.command(name="readytier3")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier3(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier3Role}> <@&{reserveTier3Role}>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

@bot.command(name="readytier4")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier4(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tierMRole}> <@&{reserveTierMRole}>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

@bot.command(name="readyf2")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGf2(ctx):
  await ctx.message.delete()
  await ctx.send("**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.\nDon't forget to not use wet tyres in qualifying as this will results in a quali ban")

@bot.command(name="racetier1")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier1(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier1Role}> <@&{reserveTier1Role}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier2")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier2(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier2Role}> <@&{reserveTier2Role}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier3")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier3(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tier3Role}> <@&{reserveTier3Role}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier4")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier4(ctx):
  await ctx.message.delete()
  await ctx.send(f"<@&{tierMRole}> <@&{reserveTierMRole}>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racef2")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGf2(ctx):
  await ctx.message.delete()
  await ctx.send("Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="academymessage")
@commands.has_any_role("Admin", "Moderator", "Trialist Manager")
async def academyMSG(ctx):
  await ctx.message.delete()
  msg =  await ctx.send(f"<@&{academyRole}>\n**TRIAL RACE BRIEFING:**\nWelcome to the F1ABEEZ trial race! I would just like to run through what is expected of you from your trial:\n- Please drive clean - we are a clean racing league, show respect to your fellow drivers! dirty driving will not be tolerated\n- Drive fast! It's still a race after all, we would like to see a true reflection of your pace\n- Do not use medium tyres in Qualifying for this trial race, as this lets us compare your quali pace!\n- Have fun! That's what we're all here for\n\nThe format is short qualifying, 25% race\nAfter the race is completed, <@401204069890523137> will DM you individually with our decision\nPlease react with a thumbs up once you have read this, good luck!")
  await msg.add_reaction("👍")

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

  embed = nextcord.Embed(title="A Ban has been issued", color=color)
  embed.add_field(name="User", value=membername, inline=False)
  embed.add_field(name="Reason", value=reason, inline=False)
  channel = bot.get_channel(warningChannel)
  await channel.send(embed = embed)
  await member.ban(reason = reason)
  await ctx.send(embed = embed)   
    
@bot.event
async def on_member_join(member):
  role = nextcord.utils.get(member.guild.roles, name="Academy Driver")
  await member.add_roles(role)
  channel = bot.get_channel(welcomeChannel)
  await channel.send(f"**Welcome <@{member.id}>**\n\nPlease use this chat if you have any questions and someone will be on hand.\n\nAll the information you need is on <#865379267977412618>")

@bot.event
async def on_member_remove(member):
  memberName = member.name
  channel = bot.get_channel(leavingChannel)
  await channel.send(f"**{memberName}** has left the server.")

@bot.command(name="stewardsdecisions")
async def stewardsDecision(ctx, round):
  channel = bot.get_channel(stewardsAnnoucementChannel)
  roundNO = int(round)
  # f2RoundNO = roundNO - 1
  # f2round = f"R{f2RoundNO}"
  round = f"R{roundNO}"
  tier1URL = f"<https://f1abeez.com/race-reports/F1-Tier-1-{round}>"
  tier2URL = f"<https://f1abeez.com/race-reports/F1-Tier-2-{round}>"
  tier3URL = f"<https://f1abeez.com/race-reports/F1-Tier-3-{round}>"
  tier4URL = f"<https://f1abeez.com/race-reports/F1-Tier-M-{round}>"
  # if(roundNO - 1 == 0):
  #   f2URL = "F2 did not race"
  # else:
  #   f2URL = f"<https://f1abeez.com/race-reports/F2-{f2round}>"
  
  await channel.send(f"🦺 @everyone\n\n**All Stewards decisions are finalised**\nPlease check this week's race-report for all the incidents reported and decisions made.\n\n**F1 - Tier 1** - {tier1URL}\n**F1 - Tier 2** - {tier2URL}\n**F1 - Tier 3** - {tier3URL}\n**F1 - Tier Mixed** - {tier4URL}\n\nPlease file your appeals with the correct case number **in the next 24 hours**, and standings will be posted after all appeals are finalised \nFollow the instructions in <#864999507238322186> to submit your appeals \n\nThank you,\nStewards of F1ABEEZ")

@bot.command(name="racereport")
async def raceResults(ctx, round):
  channel = bot.get_channel(generalAnnoucementChannel)
  roundNO = int(round)
  # f2RoundNO = roundNO - 1
  # f2round = f"R{f2RoundNO}"
  round = f"R{roundNO}"
  tier1URL = f"<https://f1abeez.com/race-reports/F1-Tier-1-{round}>"
  tier2URL = f"<https://f1abeez.com/race-reports/F1-Tier-2-{round}>"
  tier3URL = f"<https://f1abeez.com/race-reports/F1-Tier-3-{round}>"
  tier4URL = f"<https://f1abeez.com/race-reports/F1-Tier-M-{round}>"
  # if(roundNO - 1 == 0):
  #   f2URL = "F2 did not race"
  # else:
  #   f2URL = f"<https://f1abeez.com/race-reports/F2-{f2round}>"
  await channel.send(f"@everyone\n\n**Race Reports have now been published**\n\n**F1 - Tier 1** - {tier1URL}\n**F1 - Tier 2** - {tier2URL}\n**F1 - Tier 3** - {tier3URL}\n**F1 - Tier Mixed** - {tier4URL}\n\nThank you,\nKuba")

@bot.command(name="incidentchannel")
async def incidentChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Report an incident",description="React to this message to report an incident by clicking the 📨 button", color=color)
  await ctx.send(embed=embed, view=reportMenu())
  # msg = await ctx.send(embed = embed)
  # await msg.add_reaction("📨")

@bot.command(name="appealchannel")
async def appealChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Submit an appeal",description="React to this message to submit an appeal by clicking the 📨 button", color=color)
  await ctx.send(embed=embed, view=reportMenu())

@bot.command(name="suggestionchannel")
async def suggestionChannel(ctx):
  await ctx.message.delete()
  embed = nextcord.Embed(title="Submit a suggestion",description="React to this message to submit a suggestion by clicking the 📨 button", color=color)
  await ctx.send(embed=embed, view=reportMenu())

@bot.command(name="calendar")
async def getCalendar(ctx):
  await ctx.message.delete()
  view = CalendarMenu()
  selectMSG = await ctx.send("For which division do you want to see the calendar?", view=view)
  await view.wait()
  if(view.tierSelected == "F1"):
    msg = await ctx.send("Getting the F1 calendar...")
    try:
      await selectMSG.delete()
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=2%3A138&format=png", headers={"X-Figma-Token": figmaToken})
      r = r.json()
      if(r):
        await msg.delete()
      url = r["images"]["2:138"]
      e = nextcord.Embed(color=color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    except Exception as e:
      await ctx.send(f"There was an error getting the calendar, please report this issue to the admins.")
      print("calendar:")
      print(e)
  elif(view.tierSelected == "Nations League"):
    msg = await ctx.send("Getting the Nations League calendar...")
    try:
      await selectMSG.delete()
      r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=15%3A2&format=png", headers={"X-Figma-Token": figmaToken})
      r = r.json()
      if(r):
        await msg.delete()
      url = r["images"]["15:2"]
      e = nextcord.Embed(color=color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
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
      msg = await ctx.send("Getting Tier 1 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["2:16"]
      e = nextcord.Embed(color=color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 2"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 2 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A446&format=png", headers={"X-Figma-Token": figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:446"]
      e = nextcord.Embed(color=color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier 3"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier 3 Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A265&format=png", headers={"X-Figma-Token": figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:265"]
      e = nextcord.Embed(color=color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F1 - Tier Mixed"):
      await selectMSG.delete()
      msg = await ctx.send("Getting Tier M Standings...")
      r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A351&format=png", headers={"X-Figma-Token": figmaToken})
      if(r):
        await msg.delete()
      r = r.json()
      url = r["images"]["4:351"]
      e = nextcord.Embed(color=color) 
      e.set_image(url=url) 
      await ctx.send(embed=e)
    elif(view.tierSelected == "F2"):
      await ctx.send("F2 standings are currently not available")
  except KeyError:
    await ctx.send("There was an error while getting the standings. Please report this issue to the admins")
  except Exception as e:
    print("standings:")
    print(e)

@bot.command(name="changelog")
async def sendChangesAnnouncement(ctx):
  await ctx.message.delete()
  await ctx.send("@everyone")
  e = nextcord.Embed(title="F1ABEEZ Bot Updates!",description="To add to the tally of new stuff introduced on the stream I have an announcement on some new things our bot can do, **as well as some improvements to those that it already does!**" , color=color)
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
  await ctx.reply("<https://www.f1abeez.com/line-up>")

## currently unsused, but saved if needed in the future

# @bot.event
# async def on_raw_reaction_add(payload):
#   emoji, user, member, channel = payload.emoji.name, await bot.fetch_user(payload.user_id), payload.member, bot.get_channel(payload.channel_id)
#   message = await channel.fetch_message(payload.message_id)
#   if (emoji == "📨" and user.id != bot.user.id and (channel.id == incidentReportChannel or channel.id == appealReportChannel or channel.id == suggestionSubmitChannel)):
#     await message.remove_reaction(emoji, member)
#     if(channel.id == incidentReportChannel):
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
#       channel = bot.get_channel(incidentLogChannel)
#       await channel.send(embed = logEmbed)
#       await user.send(response)
    
#     if(channel.id == appealReportChannel):
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
#       channel = bot.get_channel(incidentLogChannel)
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

bot.run(discord_token)