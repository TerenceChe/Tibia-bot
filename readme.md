# Tibia Bot

This python bot allows users to track new logins and level ups in Tibia

### Requirements

1. [Python3](https://www.python.org/downloads/)

### Installation

Clone the repo:

```bash
$ git clone git@github.com:TerenceChe/Tibia-bot.git
$ cd Tibia-bot
```

Install Virtual Env & install dependencies

```bash
$ pip install virtualenv
$ py -m venv env
$ .\env\Scripts\activate
$ pip install -r requirements.txt
```

Create and populate .env<br />
Note: replace {token} with a discord bot token

```bash
echo DISCORD_TOKEN = {token} > .env
```

Running the bot

```bash
$ cd bot
$ py bot.py
```

If everything was done correctly, the bot should now be running :)
