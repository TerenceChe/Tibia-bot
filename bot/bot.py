"""
The `bot` module contains the main Discord bot functionality for the Rage Room server.

The bot listens for commands from users and sends updates about player logins, level ups, and last kills.

Functions:
- set_login_channel(channel, update): Sets the login channel and update status.
- set_last_kill_channel(channel, update): Sets the last kill channel and update status.
- set_level_channel(channel, update): Sets the level channel and update status.
- get_bot_status_message(channel): Gets the bot status message.
"""
import os
import time

import discord
from discord.ext import tasks

from dotenv import load_dotenv

import tracker
import bot.message_format as message_format

# Load the environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Define a class to store the bot state
class BotState:
    def __init__(self):
        self.prev_chars = {}
        self.login_channel = None
        self.last_kill_channel = None
        self.level_channel = None
        self.min_level_filter = 0
        self.send_login_updates = False
        self.send_last_kill_updates = False
        self.send_level_updates = False
        self.last_updated_utc = time.gmtime(time.time() - 14400)

bot_state = BotState()

# Define a function to set the login channel and update status
def set_login_channel(channel, update):
    bot_state.login_channel = channel
    bot_state.send_login_updates = update

# Define a function to set the last kill channel and update status
def set_last_kill_channel(channel, update):
    bot_state.last_kill_channel = channel
    bot_state.send_last_kill_updates = update

# Define a function to set the level channel and update status
def set_level_channel(channel, update):
    bot_state.level_channel = channel
    bot_state.send_level_updates = update

# Define a function to get the bot status message
async def get_bot_status_message(channel):
    status_message = []
    if bot_state.send_level_updates:
        status_message.append("Levels being sent in " + bot_state.level_channel.name)
    if bot_state.send_login_updates:
        status_message.append("Logins being sent in " + bot_state.login_channel.name)
    if bot_state.send_last_kill_updates:
        status_message.append("Kills being sent in " + bot_state.last_kill_channel.name)
    if status_message:
        await channel.send("\n".join(status_message))

# Define the on_ready event handler
@client.event
async def on_ready():
    guild_count = 0
    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1
    print("Rage Room is in " + str(guild_count) + " guilds.")
    send_update.start()

# Define the on_message event handler
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
                set_last_kill_channel(message.channel, True)
                updates.append("Last Kill")
            if "levels" in args or "level" in args:
                set_level_channel(message.channel, True)
                updates.append("Level")
            if len(updates) > 0:
                update_msg = ", ".join(updates)
                update_msg += " updates will be sent here every minute"
                await message.channel.send(update_msg)
            if not send_update.is_running():
                send_update.start()
        elif command == "!stop":
            stops = []
            if "login" in args and bot_state.send_login_updates:
                set_login_channel(None, False)
                stops.append("Login")
            if "kills" in args or "kill" in args and bot_state.send_last_kill_updates:
                stops.append("Last kill")
                set_last_kill_channel(None, False)
            if "levels" in args or "level" in args:
                stops.append("Level")
                set_level_channel(None, False)
            if len(stops) > 0:
                stop_msg = ", ".join(stops)
                stop_msg += " updates will no longer be sent"
                await message.channel.send(stop_msg)
            if (bot_state.send_login_updates == False and 
                bot_state.send_level_updates == False and 
                bot_state.send_last_kill_updates == False):
                send_update.cancel()
        elif command == "!filter" and args[1] == "level" and args[2].isnumeric():
            bot_state.min_level_filter = int(args[2])
            await message.channel.send(f"Level updates will only be sent for players above level \
                                       {bot_state.min_level_filter}")
        elif command == "!status":
            await get_bot_status_message(message.channel)

# Define the send_update task
@tasks.loop(minutes = 1)
async def send_update():
    curr_chars = tracker.get_curr_chars()
    if bot_state.send_login_updates:
        if bot_state.prev_chars:
            login_message = message_format.login_message(tracker.get_logged_in(
                bot_state.prev_chars, curr_chars, bot_state.min_level_filter))
            if login_message:
                await bot_state.login_channel.send(login_message)
    if bot_state.send_level_updates:
        if bot_state.prev_chars:
            level_up_message = message_format.level_message(tracker.get_level_diff(
                bot_state.prev_chars, curr_chars, bot_state.min_level_filter))
            if level_up_message:
                await bot_state.level_channel.send(level_up_message)
    if bot_state.send_last_kill_updates:
        last_kill_message, last_kill_time = message_format.last_kill_message(
            *tracker.get_last_kill(bot_state.last_updated_utc))
        curr_time = time.gmtime(time.time() - 14400)
        bot_state.last_updated_utc = last_kill_time if last_kill_time > curr_time else curr_time
        if last_kill_message:
            await bot_state.last_kill_channel.send(last_kill_message)
    bot_state.prev_chars = curr_chars

# Run the client
client.run(TOKEN)