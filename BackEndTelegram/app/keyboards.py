from aiogram import types
from aiogram.utils.callback_data import CallbackData
from app.db import DataBase

db = DataBase()

callback_groups = CallbackData("group", "major", "year", "id")

def group_keyboard(user):
    """Клавиатура сохраненных пользователем груп."""
    groups = db.get_user_group(user)
    buttons = (
            types.InlineKeyboardButton(
                text=str(item[0]) + str(item[1]), 
                callback_data=callback_groups.new(
                    major=item[0],
                    year=item[1],
                    id=item[2]))
                for item in groups)   
    add = types.InlineKeyboardButton(text="Додати групу", callback_data="add group")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    keyboard.row(add)
    return keyboard

callback_days = CallbackData("week","day")

def day_keyboard(day='Понеділок', option='option 1'):
    options={'option 1':'1 вариант','option 2':'2 вариант'}
    options[option] = '➡️ ' + options[option]
    row_2=[
        types.InlineKeyboardButton(
            text=options['option 1'],
            callback_data="option 1"),
        types.InlineKeyboardButton(
            text=options['option 2'],
            callback_data="option 2")
        ]
    row_3=types.InlineKeyboardButton(
            text='Видалити групу',
            callback_data='delete')
    row_4= types.InlineKeyboardButton(
            text='Настройка',
            callback_data='setting')
    days={'Понеділок':'Пн','Вівторок':'Вт','Середа':'Ср',
          'Четвер':'Чт','Пятниця':'Пт'}
    days[day] = '➡️ ' + days[day]
    buttons = [
            types.InlineKeyboardButton(
                text=days['Понеділок'],
                callback_data=callback_days.new(day="Понеділок")),
            types.InlineKeyboardButton(
                text=days['Вівторок'],
                callback_data=callback_days.new(day="Вівторок")),
            types.InlineKeyboardButton(
                text=days['Середа'],
                callback_data=callback_days.new(day="Середа")),
            types.InlineKeyboardButton(
                text=days['Четвер'],
                callback_data=callback_days.new(day="Четвер")),
            types.InlineKeyboardButton(
                text=days['Пятниця'],
                callback_data=callback_days.new(day="Пятниця")),
            ]


    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(*buttons)
    keyboard.row(*row_2)
    keyboard.row(row_3)
    keyboard.row(row_4)
    
    return keyboard


callback_facultys = CallbackData("user","faculty")

def faculty_keyboard():
    faculty = db.get_faculty()
    buttons = (
            types.InlineKeyboardButton(
                item[0],
                callback_data=callback_facultys.new(faculty=item[0]))
            for item in faculty)   
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard

callback_majors = CallbackData("users","major")

def major_keyboard(faculty):
    major = db.get_major(faculty)
    buttons = (
            types.InlineKeyboardButton(
                item[0],
                callback_data=callback_majors.new(major=item[0])) 
            for item in major)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard
callback_years = CallbackData("us","year")

def year_keyboard():
    buttons=(
            types.InlineKeyboardButton(
                item,
                callback_data=callback_years.new(year=item)) 
            for item in range (1,5))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

