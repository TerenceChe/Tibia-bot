import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	guild_count = 0

	for guild in client.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

@client.event
async def on_message(message):
	if message.content == "hello":
		await message.channel.send("hey dirtbag")

client.run(TOKEN)