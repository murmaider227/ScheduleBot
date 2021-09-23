from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def start_cmd(message: types.Message):
    keyboard_mark = types.InlineKeyboardMarkup(row_width=2)

    text_and_data=(
            ('Маркетинг','Маркетинг'),
            ('Менеджмент','Менеджмент'),
            )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    row_2= types.InlineKeyboardButton('Настройка', callback_data='setting')

    keyboard_mark.row(*row_btns)
    keyboard_mark.row(row_2)

    await message.reply('Вибери спеціальність', reply_markup=keyboard_mark)

def register_handlers_common(dp: Dispatcher):
        dp.register_message_handler(start_cmd, commands="start", state="*")
