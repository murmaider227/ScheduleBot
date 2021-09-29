from contextlib import suppress


from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from app.utils import print_schedule
import app.keyboards as keyboard
from app.handlers.user_group import ChooseMajor



async def choose_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    text = print_schedule(callback_data["major"], callback_data["year"])
    await query.message.edit_text(text=text,
                                reply_markup=keyboard.day_keyboard())
    await ChooseMajor.save_major.set()
    await state.update_data(chosen_major=callback_data["major"],
                            chosen_year=callback_data["year"],
                            chosen_group=callback_data["id"],
                            chosen_option='option 1',
                            chosen_day='Понеділок')

async def answer_for_choosen_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    await state.update_data(chosen_day=callback_data["day"])
    user_data = await state.get_data()
    text = print_schedule(user_data['chosen_major'],
                          user_data["chosen_year"],
                          callback_data["day"],
                          user_data['chosen_option'])
    with suppress(MessageNotModified):
        await query.message.edit_text(text=text,
                                reply_markup=keyboard.day_keyboard())
    await query.answer()

async def change_option(query: types.CallbackQuery, state: FSMContext):
    user_data= await state.get_data()
    if user_data['chosen_option'] != query.data:
        await state.update_data(chosen_option=query.data)
        text = print_schedule(user_data['chosen_major'],
                              user_data["chosen_year"],
                              user_data["chosen_day"],
                              query.data)
        await query.message.edit_text(text=text,
                                reply_markup=keyboard.day_keyboard())
    else:
        await query.answer()

def register_handlers_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(choose_day, keyboard.callback_groups.filter(), state='*')
    dp.register_callback_query_handler(answer_for_choosen_day, keyboard.callback_days.filter(), state=ChooseMajor.save_major)
    dp.register_callback_query_handler(change_option, text="option 1", state=ChooseMajor.save_major)
    dp.register_callback_query_handler(change_option, text="option 2", state=ChooseMajor.save_major)

