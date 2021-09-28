from contextlib import suppress


from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified

from app.utils import print_schedule, save_user_group
import app.keyboards as keyboard 
from app.db import delete_user_from_group


class ChooseMajor(StatesGroup):
    save_group = State() # для сохранения групы
    save_major = State() # для сохранения специальности при выборе другого дня


async def choose_group(message: types.Message):
    await message.answer("Вибери групу", reply_markup=keyboard.group_keyboard(message.from_user.id))

async def choose_faculty(query: types.CallbackQuery):
        await query.message.edit_text("Выберите факультет", reply_markup=keyboard.faculty_keyboard())

async def choose_major(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await ChooseMajor.save_group.set()
    await query.message.edit_text('Вибери спеціальність', reply_markup=keyboard.major_keyboard(callback_data["faculty"]))

async def choose_year(query: types.CallbackQuery, callback_data: dict, state:FSMContext):
    await state.update_data(chosen_major=callback_data["major"])
    await query.message.edit_text(text='Вибери рык', reply_markup=keyboard.year_keyboard())

async def user_save_group(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ''' Сохранение групы в бд '''
    user_data = await state.get_data()
    save_user_group(query.from_user.id, user_data['chosen_major'], callback_data["year"])
    await query.message.edit_text('Успешно')

async def choose_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    text = print_schedule(callback_data["major"], callback_data["year"])
    await query.message.edit_text(text=text,
                                reply_markup=keyboard.day_keyboard())
    await ChooseMajor.save_major.set()
    await state.update_data(chosen_major=callback_data["major"], chosen_year=callback_data["year"], chosen_group=callback_data["id"], chosen_option='option 1', chosen_day='Понеділок')

async def answer_for_choosen_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    await state.update_data(chosen_day=callback_data["day"])
    user_data = await state.get_data()
    text = print_schedule(user_data['chosen_major'], user_data["chosen_year"], callback_data["day"], user_data['chosen_option'])
    with suppress(MessageNotModified):
        await query.message.edit_text(text=text,
                                reply_markup=keyboard.day_keyboard())
    await query.answer()

async def change_option(query: types.CallbackQuery, state: FSMContext):
    user_data= await state.get_data()
    if user_data['chosen_option'] != query.data:
        await state.update_data(chosen_option=query.data)
        text = print_schedule(user_data['chosen_major'], user_data["chosen_year"], user_data["chosen_day"], query.data)
        await query.message.edit_text(text=text,
                                reply_markup=keyboard.day_keyboard())
    else:
        await query.answer()

async def delete_from_group(query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    delete_user_from_group(query.from_user.id, user_data['chosen_group'])
    await query.answer('Група успешно удалена', show_alert=True)
    await query.message.edit_text('Вибери групу', reply_markup=keyboard.group_keyboard(query.from_user.id))


def register_handlers_schedule(dp: Dispatcher):
    dp.register_message_handler(choose_group, text="Розклад занять", state='*')
    dp.register_callback_query_handler(delete_from_group, text="delete", state=ChooseMajor.save_major)
    dp.register_callback_query_handler(choose_faculty, text="add group", state='*')
    dp.register_callback_query_handler(change_option, text="option 1", state=ChooseMajor.save_major)
    dp.register_callback_query_handler(change_option, text="option 2", state=ChooseMajor.save_major)
    dp.register_callback_query_handler(choose_major, keyboard.callback_facultys.filter(), state='*')
    dp.register_callback_query_handler(choose_year, keyboard.callback_majors.filter(), state=ChooseMajor.save_group)
    dp.register_callback_query_handler(user_save_group, keyboard.callback_years.filter(), state=ChooseMajor.save_group)
    dp.register_callback_query_handler(choose_day, keyboard.callback_groups.filter(), state='*')
    dp.register_callback_query_handler(answer_for_choosen_day, keyboard.callback_days.filter(), state=ChooseMajor.save_major)
