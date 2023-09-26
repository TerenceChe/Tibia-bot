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
level_channel = None
min_level_filter = 0
send_login_updates = False
send_last_kill_updates = False
send_level_updates = False
last_updated_utc = time.gmtime(time.time() - 14400)

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
			updates = []
			if "login" in args:
				set_login_channel(message.channel, True)
				updates.append("Login")
			if "kills" in args or "kill" in args:
				set_lask_kill_channel(message.channel, True)
				updates.append("Last Kill")
			if "levels" in args or "level" in args:
				set_level_channel(message.channel, True)
				updates.append("Level")
			if len(updates) > 0:
				update_msg = ", ".join(updates)
				update_msg += " updates will be sent here every minute"
				await message.channel.send(update_msg)

			if not send_update.is_running:
				send_update.start()
		
		elif command == "!stop":
			stops = []
			if "login" in args:
				set_login_channel(None, False)
				stops.append("Login")
			if "kills" in args or "kill" in args:
				stops.append("Last kill")
				send_last_kill_updates(None, False)
			if "levels" in args or "level" in args:
				stops.append("Level")
				set_level_channel(None, False)
			if len(stops) > 0:
				stop_msg = ", ".join(stops)
				stop_msg += " updates will no longer be sent"
				await message.channel.send(stop_msg)

			if (send_login_updates == False and send_level_updates == False and send_last_kill_updates == False):
				send_update.cancel()

		elif command == "!filter" and args[1] == "level" and args[2].isnumeric():
			set_level_channel(message.channel, send_level_updates)
			global min_level_filter
			min_level_filter = int(args[2])
			await level_channel.send(f"Level updates will only be sent for players above level {min_level_filter}")

@tasks.loop(minutes = 1)
async def send_update():

	global prev_chars
	global last_updated_utc

	curr_chars = tracker.get_curr_chars()
	print(send_login_updates, send_level_updates, send_last_kill_updates)
	if send_login_updates:
		if prev_chars:
			login_message = messageFormat.login_message(tracker.get_logged_in(prev_chars, curr_chars, min_level_filter))
			if login_message:
				await login_channel.send(login_message)
	
	if send_level_updates:
		if prev_chars:
			level_up_message = messageFormat.level_message(tracker.get_level_diff(prev_chars, curr_chars, min_level_filter))
			if level_up_message:
				await level_channel.send(level_up_message)

	if send_last_kill_updates:
		last_kill_message, last_kill_time = messageFormat.last_kill_message(*tracker.get_last_kill(last_updated_utc))
		curr_time = time.gmtime(time.time() - 14400)
		print(last_kill_time, curr_time)
		last_updated_utc = last_kill_time if last_kill_time > curr_time else curr_time
		print(last_updated_utc)
		if last_kill_message:
			await last_kill_channel.send(last_kill_message)

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

def set_level_channel(c, update):
	global level_channel
	global send_level_updates
	level_channel = c
	send_level_updates = update

client.run(TOKEN)