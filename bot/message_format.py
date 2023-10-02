"""
The `message_format` module contains functions for formatting messages to send to Discord channels.

Functions:
- login_message(char_map): Formats a message about player logins.
- level_message(char_map): Formats a message about player level ups.
- last_kill_message(killer, victim, weapon): Formats a message about the last kill.
"""
from table2ascii import table2ascii as t2a, PresetStyle
from typing import List
import time

def login_message(chars: dict[str, dict[str, str]]) -> str:
    message = ""
    if chars:
        message += "New player logins:\n"
        header = ["Name", "Level", "Vocation"]
        body = [[char, chars[char]['level'], 
                 simplify_vocation(chars[char]['vocation'])] for char in chars]
        table = t2a(header=header, body=body, style=PresetStyle.thin_compact)
        message += f"```ansi\n{table}```"
        message = colour(message)
    return message

def level_message(chars: dict[str, dict[str, str]]) -> str:
    message = ""
    if chars:
        message += "Player level change:\n"
        header = ["Name", "Level", "Vocation"]
        body = [[char, f"{chars[char]['prev_lvl']} -> {chars[char]['curr_lvl']}", 
                 simplify_vocation(chars[char]['vocation'])] for char in chars]
        table = t2a(header=header, body=body, style=PresetStyle.thin_compact)
        message += f"```ansi\n{table}```"
        message = colour(message)
    return message

def last_kill_message(kill_data: List[str], 
                      last_updated: time.struct_time) -> tuple[str, time.struct_time]:
    message = ""
    if kill_data:
        message += "Last Kills:\n"
        header = ["Date", "Name", "Killers"]
        body = [[kill[0], kill[1], ", ".join(kill[2])] for kill in kill_data]
        table = t2a(header=header, body=body, style=PresetStyle.thin_compact)
        message += f"```ansi\n{table}```"
    return message, last_updated

def simplify_vocation(message: str) -> str:
    name_map = {
        "Elder Druid": "Druid",
        "Royal Paladin": "Paladin",
        "Master Sorcerer": "Sorcerer",
        "Elite Knight": "Knight"
    }
    return reduce_string(message, name_map)

def colour(message: str) -> str:
    colour_map = {
        "Druid": "\u001b[0;32mDruid\u001b[0;0m",
        "Paladin": "\u001b[0;33mPaladin\u001b[0;0m",
        "Sorcerer": "\u001b[0;34mSorcerer\u001b[0;0m",
        "Knight": "\u001b[0;31mKnight\u001b[0;0m",
    }
    return reduce_string(message, colour_map)

def reduce_string(message: str, string_map: dict[str, str]) -> str:
    for key, value in string_map.items():
        message = message.replace(key, value)
    return message