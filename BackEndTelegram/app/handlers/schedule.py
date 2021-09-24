from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from app.utils import print_schedule
from app.keyboards import day_keyboard, callback_days


class ChooseMajor(StatesGroup):
    choose_faculty = State()
    choose_major = State()
    choosen_major = State()
    choose_year = State()
    choose_option = State()


 
async def answer_for_choosen_major(query: types.CallbackQuery, state: FSMContext):
    #logging.info(f'{query.message.chat.username}: {query.data}')
    text = print_schedule(query.data)
    await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())
    await ChooseMajor.choosen_major.set()
    await state.update_data(chosen_major=query.data)

async def answer_for_choosen_day(query: types.CallbackQuery, callback_data : dict, state: FSMContext):
    #logging.info(f'{query.message.chat.username}: {query.data}')
    user_data = await state.get_data()
    text = print_schedule(user_data['chosen_major'], callback_data["day"])

    await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())

def register_handlers_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(answer_for_choosen_major, text="Маркетинг", state='*')
    dp.register_callback_query_handler(answer_for_choosen_day, callback_days.filter(), state=ChooseMajor.choosen_major)
