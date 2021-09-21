from db import get_schedule


def print_schedule():
    text=get_schedule()
    data=''
    if text[5]:
        data += f"~~~~~~~~~~~~~ \n 1 {text[5]}\n"\
            f"{text[6]}\n"
    if text[7]:
        data += f"~~~~~~~~~~~~~ \n 2 {text[7]}\n"\
            f"{text[8]}\n"
    if text[9]:
        data += f"~~~~~~~~~~~~~ \n 3 {text[9]}\n"\
            f"{text[10]}\n"
 

    return data
