import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

curse_words = ["amcık", "soktuğum", "salak", "kodumun", "sokarım", "siktiğim"]

default_reacts = [
  "Oğlum küfür etme lan",
  "Sus *mim belanı.",
  "Sussanaaaa!"
]

# if there is no any attribute that checks bot's responding, creates one
if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)



#region BOT REACT
# This part is related to the answer that bot's react to the curse words
def update_reacts(react_message):
  if "reacts" in db.keys():
    reacts = db["reacts"]
    reacts.append(react_message)
    db["reacts"] = reacts
  else:
    db["reacts"] = [react_message]

def delete_reacts(index):
  reacts = db["reacts"]
  if len(reacts) > index:
    del reacts[index]
    db["reacts"] = reacts
#endregion

#region BOT REACT TO
# This part is related to the curse words that bot's react to 
def update_curses(new_curse):
  if "curses" in db.keys():
    curses = db["curses"]
    curses.append(new_curse)
    db["curses"] = curses
  else:
    db["curses"] = [new_curse]

def delete_curses(index):
  curses = db["curses"]
  if len(curses) > index:
    del curses[index]
    db["curses"] = curses
#endregion

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

# this line uses the get_quote method to type random 
# inspiration message that returned from api
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

# If bot's responding mode is activated those lines work
  if db["responding"]:
    options = default_reacts
    if "reacts" in db.keys():
      options = options + db["reacts"]

    if any(word in msg for word in curse_words):
      await message.channel.send(random.choice(options))

#region ADDING, DELETING and LISTING REACTS
  if msg.startswith("$newreact"):
    react_message = msg.split("$newreact ",1)[1]
    update_reacts(react_message)
    await message.channel.send("New react message added.")

  if msg.startswith("$delreact"):
    reacts = []
    if "reacts" in db.keys():
      index = int(msg.split("$delreact",1)[1])
      delete_reacts(index)
      reacts = db["reacts"]
    await message.channel.send(reacts)

  if msg.startswith("$listreacts"):
    reacts = []
    if "reacts" in db.keys():
      reacts = db["reacts"]
    await message.channel.send(reacts)
#endregion

#region ADDING, DELETING and LISTING CURSES
  if msg.startswith("$newcurse"):
    curse_message = msg.split("$newcurse ",1)[1]
    update_curses(curse_message)
    await message.channel.send("New curse message added.")

  if msg.startswith("$delcurse"):
    curses = []
    if "curses" in db.keys():
      index = int(msg.split("$delcurse",1)[1])
      delete_curses(index)
      curses = db["curses"]
    await message.channel.send(curses)

  if msg.startswith("$listcurses"):
    curses = []
    if "curses" in db.keys():
      curses = db["curses"]
    await message.channel.send(curses)
#endregion

#region ACTIVATING AND DEACTIVATING THE RESPONDING OF BOT
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
#endregion

keep_alive()
client.run(os.getenv('TOKEN'))