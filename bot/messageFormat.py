from table2ascii import table2ascii as t2a, PresetStyle
from typing import List

def login_message(chars: dict[str, dict[str, str]]) -> str:
    message = ""
    if len(chars) > 0:
        message += "New player logins:\n"
        header = ["Name", "Level", "Vocation"]
        body = []
        for char in chars:
            vocation = chars.get(char).get('vocation')
            vocation = simplify_vocation(vocation)
            level = chars.get(char).get('level')
            body.append([char, level, vocation])

        table = t2a(header = header, body = body, style = PresetStyle.thin_compact)
        message += f"```ansi\n{table}```"
        message = colour(message)
    return message

def level_message(chars: dict[str, dict[str, str]]):
    message = ""
    if len(chars) > 0:
        message += "Player level change:\n"
        header = ["Name", "Level", "Vocation"]
        body = []
        for char in chars:
            level = f"{chars.get(char).get('prev_lvl')} -> {chars.get(char).get('curr_lvl')}"
            vocation = chars.get(char).get('vocation')
            vocation = simplify_vocation(vocation)
            body.append([char, level, vocation])
            
        table = t2a(header = header, body = body, style = PresetStyle.thin_compact)
        message += f"```ansi\n{table}```"
        message = colour(message)
    return message

def last_kill_msg(msg: List[str]) -> str:
    return '\n'.join(msg)

def simplify_vocation(message:str) -> str:
    name_map = {
        "Elder Druid" : "Druid",
        "Royal Paladin" : "Paladin",
        "Master Sorcerer" : "Sorcerer",
        "Elite Knight" : "Knight"
    }

    for vocation in name_map:
        message = message.replace(vocation, name_map.get(vocation))
    return message

def colour(message: str) -> str:
    colour_map = {
    "Druid" : "\u001b[0;32mDruid\u001b[0;0m",
    "Paladin" : "\u001b[0;33mPaladin\u001b[0;0m",
    "Sorcerer" : "\u001b[0;34mSorcerer\u001b[0;0m",
    "Knight" : "\u001b[0;31mKnight\u001b[0;0m",
    }

    for vocation in colour_map:
        message = message.replace(vocation, colour_map.get(vocation))
    return message

if __name__ == "__main__":
    print(last_kill_msg(
        ['lave Of The Law killed at level 209 by Rick Muttley and by Snaike.', 
         'icsocer died at level 114 by a dragon lord and by Vicsocer.', 
         'Magicice died at level 216 by a dragon lord, by Davion God and by Earthbeam.', 
         'Raczidian died at level 236 by a hydra, by Cares, by Davion God and by Slave Of The Law.',
        'Pwe killed at level 260 by Earthbeam, by Nomb and by Moonbeam.',
        'Davion God died at level 302 by a dark hunter, by a mythra guardian, by Slave Of The Law, by a mythra worshipper and by a dagger wasp.',
        'Arthur Morgan killed at level 212 by Earthbeam, by Cares and by Davion God.',
        'Kowaalski killed at level 216 by Earthbeam, by Nivek Of Rivia, by Carding Fisico Nevermoore and by Davion God.',
        'El Forest killed at level 233 by Earthbeam, by Nivek Of Rivia, by Carding Fisico Nevermoore, by Davion God and by an illusion rat.', 
        'Linda Danis killed at level 194 by Earthbeam, by Davion God, by Nivek Of Rivia and by an illusion rat.']))