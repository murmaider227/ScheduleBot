from contextlib import suppress


from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified

from app.utils import print_schedule, save_user_group
from app.keyboards import faculty_keyboard, day_keyboard, callback_days, major_keyboard, callback_facultys, callback_majors, group_keyboard, callback_groups, year_keyboard, callback_years


class ChooseMajor(StatesGroup):
    save_group = State()
    save_major = State()


async def choose_group(message: types.Message):
    await message.answer("Вибери групу", reply_markup=group_keyboard())

async def choose_faculty(query: types.CallbackQuery):
        await query.message.edit_text("Выберите факультет", reply_markup=faculty_keyboard())

async def choose_major(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await ChooseMajor.save_group.set()
    await query.message.edit_text('Вибери спеціальність', reply_markup=major_keyboard(callback_data["faculty"]))

async def choose_year(query: types.CallbackQuery, callback_data: dict, state:FSMContext):
    await state.update_data(chosen_major=callback_data["major"])
    await query.message.edit_text(text='Вибери рык', reply_markup=year_keyboard())

async def user_save_group(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_data = await state.get_data()
    save_user_group(query.from_user.id, user_data['chosen_major'], callback_data["year"])
    await query.message.edit_text('Успешно')

async def choose_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    text = print_schedule(callback_data["major"])
    await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())
    await ChooseMajor.save_major.set()
    await state.update_data(chosen_major=callback_data["major"])

async def answer_for_choosen_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    user_data = await state.get_data()
    text = print_schedule(user_data['chosen_major'], callback_data["day"])
    with suppress(MessageNotModified):
        await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())
    await query.answer()


def register_handlers_schedule(dp: Dispatcher):
    dp.register_message_handler(choose_group, text="Розклад занять", state='*')
    dp.register_callback_query_handler(choose_faculty, text="add group", state='*')
    dp.register_callback_query_handler(choose_major, callback_facultys.filter(), state='*')
    dp.register_callback_query_handler(choose_year, callback_majors.filter(), state=ChooseMajor.save_group)
    dp.register_callback_query_handler(user_save_group, callback_years.filter(), state=ChooseMajor.save_group)
    dp.register_callback_query_handler(answer_for_choosen_day, callback_days.filter(), state=ChooseMajor.save_major)