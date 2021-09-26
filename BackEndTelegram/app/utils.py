from app.db import get_schedule, get_group_id, save_group

def save_user_group(user, major, year):
    group_id = get_group_id(year, major)
    save_group(user, group_id)

def print_schedule(major, year, day='Понеділок'):
    text=get_schedule(major, year, day)
    data=''
    if text[5]:
        data += f"~~~~~~~~~~~~~ \n 1 {text[5]}\n"\
            f"🎓{text[6]}\n📍{text[7]} \n"\
            f"🕓 8:00 − 9:35 \n"
    if text[8]:
        data += f"~~~~~~~~~~~~~ \n 2 {text[8]}\n"\
            f"🎓{text[9]}\n📍{text[10]} \n"\
            f"🕓 9:55 − 11:30 \n"
    if text[11]:
        data += f"~~~~~~~~~~~~~ \n 3 {text[11]}\n"\
            f"🎓{text[12]}\n📍{text[13]} \n"\
            f"🕓 12:00 − 13:35 \n"
    if text[14]:
        data += f"~~~~~~~~~~~~~ \n 3 {text[14]}\n"\
            f"🎓{text[15]}\n📍{text[16]} \n"\
            f"🕓 13:55 − 15:15 \n" 

    return data

