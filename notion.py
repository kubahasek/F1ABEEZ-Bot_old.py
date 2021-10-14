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
import info



def queryTickets(gamertag):
    zprava = ""
    header = {"Authorization": info.token, "Notion-Version": "2021-05-13"}
    r = requests.post(info.incidentDatabaseURL, json = {
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

    embed = nextcord.Embed(title=f"Tickets where {gamertag} was involved", color=info.color)

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
    header = {"Authorization": info.token,  "Notion-Version": "2021-05-13"}
    req = requests.post(info.incidentDatabaseURL, json = {
        "filter": {
        "property": "Case Number",
        "title": {
            "contains": ticketNumber
        }
        }
        }
        , headers=header).text

    c = json.loads(req)
    embed=nextcord.Embed(title="Incident Detail", color=info.color)
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
  header = {"Authorization": info.token, "Notion-Version": "2021-05-13"}
  r = requests.post(info.appealsDatabaseURL, json = {
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
  

  embed = nextcord.Embed(title=f"Appeals where {gamertag} was involved", color=info.color)

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
  header = {"Authorization": info.token, "Notion-Version": "2021-05-13"}
  r = requests.post(url, headers=header, json={
  "parent": {
    "database_id": info.appealsDatabaseId
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

def submitAnIncident(gamertag, lap, description, tier, evidence, driverInvolved, date):
    url = "https://api.notion.com/v1/pages/"
    header = header = {"Authorization": info.token, "Notion-Version": "2021-05-13"}
    r = requests.post(url, headers=header, json={
  "parent": {
    "database_id": info.incidentDatabaseId
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