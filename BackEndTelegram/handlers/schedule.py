from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils import print_schedule

class ChooseMajor(StatesGroup):
    choose_faculty = State()
    choose_major = State()
    choosen_major = State()
    choose_year = State()
    choose_option = State()

def day_keyboard():
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)

    text_and_data=(
            ('Пн','Понеділок'),
            ('Вт','Вівторок'),
            ('Ср','Середа'),
            ('Чт','Четвер'),
            ('Пт','Пятниця'),
            )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    row_2= types.InlineKeyboardButton('Настройка', callback_data='setting')

    keyboard_markup.row(*row_btns)
    keyboard_markup.row(row_2)
    return keyboard_markup 

async def answer_for_choosen_major(query: types.CallbackQuery, state: FSMContext):
    #logging.info(f'{query.message.chat.username}: {query.data}')
    text = print_schedule(query.data)
    await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())
    await ChooseMajor.choosen_major.set()
    await state.update_data(chosen_major=query.data)

async def answer_for_choosen_day(query: types.CallbackQuery, state: FSMContext):
    #logging.info(f'{query.message.chat.username}: {query.data}')
    user_data = await state.get_data()
    text = print_schedule(user_data['chosen_major'], query.data)

    await query.message.edit_text(text=text,
                                reply_markup=day_keyboard())

def register_handlers_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(answer_for_choosen_major, text="Маркетинг", state='*')
    dp.register_callback_query_handler(answer_for_choosen_day, state=ChooseMajor.choosen_major)
