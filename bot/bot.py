import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import tracker
import messageFormat

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

prev_chars = {}
channel = None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	guild_count = 0

	for guild in client.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("Rage Room is in " + str(guild_count) + " guilds.")

@client.event
async def on_message(message):
	if message.content.startswith("!"):
		if message.content == "!update":
			global channel 
			channel = message.channel
			await channel.send("Updates will be sent here every minute")
			send_update.start()
		
		if message.content == "stop":
			await channel.send("Updates will no longer be sent")
			send_update.cancel()

@tasks.loop(minutes = 1)
async def send_update():

	global prev_chars

	curr_chars = tracker.get_curr_chars()
	if len(prev_chars) > 0:
		level_up_message = messageFormat.level_message(tracker.get_level_diff(prev_chars, curr_chars))
		login_message = messageFormat.login_message(tracker.get_logged_in(prev_chars, curr_chars))
		if len(level_up_message) > 0 or len(login_message) > 0:
			final_message = login_message + level_up_message
			await channel.send(final_message)

	prev_chars = curr_chars
	

client.run(TOKEN)