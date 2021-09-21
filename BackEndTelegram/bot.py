from aiogram import Bot, Dispatcher, executor, types
import logging
import os

from utils import print_schedule

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_cmd(message: types.Message):
    await message.answer('hello')

@dp.message_handler(commands='test')
async def schedule(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)

    text_and_data=(
            ('Пн','monday'),
            ('Вт','tuesday'),
            ('Ср','wednesday'),
            ('Чт','thursday'),
            ('Пт','friday'),
            )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    row_2= types.InlineKeyboardButton('Настройка', callback_data='setting')

    keyboard_markup.row(*row_btns)
    keyboard_markup.row(row_2)
    text=print_schedule()
    await message.reply(text, reply_markup=keyboard_markup)
    

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
