from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import os

from utils import print_schedule

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

class ChooseMajor(StatesGroup):
    choose_faculty = State()
    choose_major = State()
    choosen_major = State()
    choose_year = State()
    choose_option = State()

def start_keyboard():
    keyboard_mark = types.InlineKeyboardMarkup(row_width=2)

    text_and_data=(
            ('Маркетинг','Маркетинг'),
            ('Менеджмент','Менеджмент'),
            )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    row_2= types.InlineKeyboardButton('Настройка', callback_data='setting')

    keyboard_mark.row(*row_btns)
    keyboard_mark.row(row_2)
    return keyboard_mark


@dp.message_handler(commands='start', state='*')
async def start_cmd(message: types.Message):
    await message.reply('Вибери спеціальність', reply_markup=start_keyboard())
    await ChooseMajor.choose_major.set() 

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

@dp.callback_query_handler(text='Маркетинг', state=ChooseMajor.choose_major)
@dp.callback_query_handler(text='Менеджмент')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    logging.info(f'{query.message.chat.username}: {query.data}')
    text = print_schedule(query.data)
    await bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text=text,
                                reply_markup=day_keyboard())
    await state.update_data(chosen_major=query.data)
    await ChooseMajor.next()

@dp.callback_query_handler(state=ChooseMajor.choosen_major)
async def inline_kb_answer_callback_handler1(query: types.CallbackQuery, state: FSMContext):
    logging.info(f'{query.message.chat.username}: {query.data}')
    user_data = await state.get_data()
    text = print_schedule(user_data['chosen_major'], query.data)
    await bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text=text,
                                reply_markup=day_keyboard())

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
