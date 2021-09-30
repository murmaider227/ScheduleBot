from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.utils import print_schedule, save_user_group
import app.keyboards as keyboard 
from app.db import DataBase


db = DataBase()

class ChooseMajor(StatesGroup):
    save_group = State() # для сохранения групы
    save_major = State() # для сохранения специальности при выборе другого дня


async def choose_group(message: types.Message):
    await message.answer("Вибери групу", reply_markup=keyboard.group_keyboard(message.from_user.id))

async def back_button(query: types.CallbackQuery):
    await query.message.edit_text("Вибери групу", reply_markup=keyboard.group_keyboard(query.from_user.id))

async def choose_faculty(query: types.CallbackQuery):
        await query.message.edit_text("Выберите факультет", reply_markup=keyboard.faculty_keyboard())

async def choose_major(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await ChooseMajor.save_group.set()
    await query.message.edit_text('Вибери спеціальність', reply_markup=keyboard.major_keyboard(callback_data["faculty"]))

async def choose_year(query: types.CallbackQuery, callback_data: dict, state:FSMContext):
    await state.update_data(chosen_major=callback_data["major"])
    await query.message.edit_text(text='Вибери рiк', reply_markup=keyboard.year_keyboard())

async def user_save_group(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ''' Сохранение групы в бд. '''
    user_data = await state.get_data()
    save_user_group(query.from_user.id, user_data['chosen_major'], callback_data["year"])
    await query.message.edit_text('Успешно')

async def delete_from_group(query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    db.delete_user_from_group(query.from_user.id, user_data['chosen_group'])
    await query.answer('Група успешно удалена', show_alert=True)
    await query.message.edit_text('Вибери групу', reply_markup=keyboard.group_keyboard(query.from_user.id))


def register_handlers_user_group(dp: Dispatcher):
    dp.register_message_handler(choose_group, text="Розклад занять", state='*')
    dp.register_callback_query_handler(back_button, text="back", state='*')
    dp.register_callback_query_handler(delete_from_group, text="delete", state=ChooseMajor.save_major)
    dp.register_callback_query_handler(choose_faculty, text="add group", state='*')
    dp.register_callback_query_handler(choose_major, keyboard.callback_facultys.filter(), state='*')
    dp.register_callback_query_handler(choose_year, keyboard.callback_majors.filter(), state=ChooseMajor.save_group)
    dp.register_callback_query_handler(user_save_group, keyboard.callback_years.filter(), state=ChooseMajor.save_group)

