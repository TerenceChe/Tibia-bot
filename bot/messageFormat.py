from table2ascii import table2ascii as t2a, PresetStyle

def login_message(chars: dict[str, dict[str, str]]) -> str:
    message = ""
    if len(chars) > 0:
        message += "New player logins:\n"
    for char in chars:
        message += f"{char} {chars.get(char).get('level')} {chars.get(char).get('vocation')}\n"
    return message

def level_message(chars: dict[str, dict[str, str]]):
    message = ""
    if len(chars) > 0:
        message += "Player level up:\n"
    for char in chars:
        message += f"{char}: {chars.get(char).get('prev_lvl')} -> {chars.get(char).get('curr_lvl')}\n"
    return message