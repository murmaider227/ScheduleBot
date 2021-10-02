from app.db import DataBase

db = DataBase()


def save_user_group(user, major: str, year: int) -> None:
    group_id = db.get_group_id(year, major)
    db.save_group(user, group_id)

def print_schedule(major: str, year: int, day='Понеділок', option='option 1') -> str:
    """Generate schedule by given major, year, day and option. """
    try:
        text=db.get_schedule(major, year, day, option[-1])
    except IndexError:
        return 'В данных день пар нету'
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

