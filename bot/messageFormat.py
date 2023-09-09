from table2ascii import table2ascii as t2a, PresetStyle

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
        message += "Player level up:\n"
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