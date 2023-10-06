"""
The `bot` module contains the Discord bot functionality for the Rage Room server.

Functions:
- set_channel(channel, update, channel_type): Sets the channel and update status.
- get_bot_status_message(channel): Gets the current status of the bot.
"""
import os
import time

import discord
from discord.ext import tasks

from dotenv import load_dotenv

import tracker
import message_format

# Load the environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Define a class to store the bot state
class BotState:
    """
    The `BotState` class stores the state of the Discord bot.

    Attributes:
    - prev_chars (dict): A dictionary of characters from the previous update.
    - channels (dict): A dictionary of channels to send updates to.
    - send_updates (dict): A dictionary of update statuses.
    - min_level_filter (int): The minimum level for players to send level updates for.
    - last_updated_utc (time.struct_time): The time of the last update in UTC.
    """
    def __init__(self):
        self.prev_chars = {}
        self.channels = {"login" : None,
                         "last_kill" : None,
                         "level" : None}
        self.send_updates = {"login" : False,
                             "last_kill" : False,
                             "level" : False}
        self.min_level_filter = 0
        self.last_updated_utc = time.gmtime(time.time() - 14400)

bot_state = BotState()

def set_channel(channel, update, channel_type):
    """
    Sets the channel and update status.
    """
    bot_state.channels[channel_type] = channel
    bot_state.send_updates[channel_type] = update

async def get_bot_status_message(channel):
    """
    Gets the bots status
    """
    status_message = []
    if bot_state.send_updates.get("level"):
        status_message.append("Levels being sent in " + bot_state.channels.get("level").name)
    if bot_state.send_updates.get("login"):
        status_message.append("Logins being sent in " + bot_state.channels.get("login").name)
    if bot_state.send_updates.get("last_kill"):
        status_message.append("Kills being sent in " + bot_state.channels.get("last_kill").name)
    if status_message:
        await channel.send("\n".join(status_message))

async def handle_update_command(args, channel):
    """
    Handles the !update command.
    """
    updates = []
    if "login" in args:
        set_channel(channel, True, "login")
        updates.append("Login")
    if "kills" in args or "kill" in args:
        set_channel(channel, True, "last_kill")
        updates.append("Last Kill")
    if "levels" in args or "level" in args:
        set_channel(channel, True, "level")
        updates.append("Level")
    if len(updates) > 0:
        update_msg = ", ".join(updates)
        update_msg += " updates will be sent here every minute"
        await channel.send(update_msg)
    if not send_update.is_running():
        send_update.start()

async def handle_stop_command(args, channel):
    """
    Handles the !stop command.
    """
    stops = []
    if "login" in args and bot_state.send_updates.get("login"):
        set_channel(None, False, "login")
        stops.append("Login")
    if "kills" in args or "kill" in args and bot_state.send_updates.get("last_kill"):
        stops.append("Last kill")
        set_channel(None, False, "last_kill")
    if "levels" in args or "level" in args:
        stops.append("Level")
        set_channel(None, False, "level")
    if len(stops) > 0:
        stop_msg = ", ".join(stops)
        stop_msg += " updates will no longer be sent"
        await channel.send(stop_msg)
    if (bot_state.send_updates.get("login") is False and
        bot_state.send_updates.get("level") is False and
        bot_state.send_updates.get("last_kill") is False):
        send_update.cancel()

@client.event
async def on_ready():
    """
    The `on_ready` event handler is called when the bot is ready.
    """
    guild_count = 0
    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1
    print("Rage Room is in " + str(guild_count) + " guilds.")
    send_update.start()

@client.event
async def on_message(message):
    """
    The `on_message` event handler is called when a message is sent in a channel the bot is in.
    """
    if message.content.startswith("!"):
        args = message.content.split()
        command = args[0]
        if command == "!update":
            await handle_update_command(args, message.channel)
        elif command == "!stop":
            await handle_stop_command(args, message.channel)
        elif command == "!filter" and args[1] == "level" and args[2].isnumeric():
            bot_state.min_level_filter = int(args[2])
            await message.channel.send(f"Level updates will only be sent for players above level \
                                       {bot_state.min_level_filter}")
        elif command == "!status":
            await get_bot_status_message(message.channel)

@tasks.loop(minutes = 1)
async def send_update():
    """
    The `send_update` task is called every minute to send updates to the Discord channels.
    """
    curr_chars = tracker.get_curr_chars()
    if bot_state.send_updates.get("login"):
        if bot_state.prev_chars:
            login_message = message_format.login_message(tracker.get_logged_in(
                bot_state.prev_chars, curr_chars, bot_state.min_level_filter))
            if login_message:
                await bot_state.channels.get("level").send(login_message)
    if bot_state.send_updates.get("level"):
        if bot_state.prev_chars:
            level_up_message = message_format.level_message(tracker.get_level_diff(
                bot_state.prev_chars, curr_chars, bot_state.min_level_filter))
            if level_up_message:
                await bot_state.channels.get("level").send(level_up_message)
    if bot_state.send_updates.get("last_kill"):
        last_kill_message, last_kill_time = message_format.last_kill_message(
            *tracker.get_last_kill(bot_state.last_updated_utc))
        curr_time = time.gmtime(time.time() - 14400)
        bot_state.last_updated_utc = last_kill_time if last_kill_time > curr_time else curr_time
        if last_kill_message:
            await bot_state.channels.get("last_kill").send(last_kill_message)
    bot_state.prev_chars = curr_chars

# Run the client
client.run(TOKEN)
