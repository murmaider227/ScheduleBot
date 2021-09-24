from contextlib import suppress


from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified

from app.utils import print_schedule
from app.keyboards import day_keyboard, callback_days, major_keyboard, callback_facultys, callback_majors


class ChooseMajor(StatesGroup):
    choose_major = State()
    choosen_major = State()

async def answer_for_choosen_faculty(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.message.edit_text('Вибери спеціальність', reply_markup=major_keyboard(callback_data["faculty"]))
 
async def answer_for_choosen_major(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    text = print_schedule(callback_data["major"])
    await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())
    await ChooseMajor.choosen_major.set()
    await state.update_data(chosen_major=callback_data["major"])

async def answer_for_choosen_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    user_data = await state.get_data()
    text = print_schedule(user_data['chosen_major'], callback_data["day"])
    with suppress(MessageNotModified):
        await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())
    await query.answer()


def register_handlers_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(answer_for_choosen_faculty, callback_facultys.filter(), state='*')
    dp.register_callback_query_handler(answer_for_choosen_major, callback_majors.filter(), state='*')
    dp.register_callback_query_handler(answer_for_choosen_day, callback_days.filter(), state=ChooseMajor.choosen_major)
