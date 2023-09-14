import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import time
import tracker
import messageFormat

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

prev_chars = {}
login_channel = None
last_kill_channel = None
min_level_filter = 0
send_login_updates = False
send_last_kill_updates = False
last_updated_utc = time.gmtime()

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
	send_update.start()

@client.event
async def on_message(message):
	if message.content.startswith("!"):
		args = message.content.split()
		command = args[0]
		if command == "!update":
			set_login_channel(message.channel, True)
			await login_channel.send("Updates will be sent here every minute")
			# send_update.start()
		
		elif command == "!stop":
			set_login_channel(message.channel, False)
			await login_channel.send("Updates will no longer be sent")
			# send_update.cancel()

		elif command == "!filter" and args[1] == "level" and args[2].isnumeric():
			set_login_channel(message.channel, send_login_updates)
			global min_level_filter
			min_level_filter = int(args[2])
			await login_channel.send(f"Updates will only be sent for players above level {min_level_filter}")

@tasks.loop(minutes = 1)
async def send_update():

	global prev_chars

	curr_chars = tracker.get_curr_chars()
	if send_login_updates:
		if len(prev_chars) > 0:
			level_up_message = messageFormat.level_message(tracker.get_level_diff(prev_chars, curr_chars, min_level_filter))
			login_message = messageFormat.login_message(tracker.get_logged_in(prev_chars, curr_chars, min_level_filter))
			if len(level_up_message) > 0 or len(login_message) > 0:
				final_message = login_message + level_up_message
				await login_channel.send(final_message)

	if send_last_kill_updates:
		last_kill_message = messageFormat.last_kill_message(tracker.get_last_kill(last_updated_utc))
		if len(last_kill_message) > 0:
			await last_kill_message.send(last_kill_message)

	prev_chars = curr_chars

def set_login_channel(c, update):
	global login_channel
	global send_login_updates
	login_channel = c
	send_login_updates = update
	
def set_lask_kill_channel(c, update):
	global last_kill_channel
	global send_last_kill_updates
	last_kill_channel = c
	send_last_kill_updates = update

client.run(TOKEN)