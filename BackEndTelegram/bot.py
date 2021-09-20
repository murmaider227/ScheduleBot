from aiogram import Bot, Dispatcher, executor, types
import logging
import os


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_cmd(message: types.Message):
    await message.answer('hello')



if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
