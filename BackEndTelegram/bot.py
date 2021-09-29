from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import os
import asyncio

from app.utils import print_schedule
from app.handlers.common import register_handlers_common
from app.handlers.schedule import register_handlers_schedule
from app.handlers.user_group import register_handlers_user_group

logger = logging.getLogger(__name__)

async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot") 

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_common(dp)
    register_handlers_schedule(dp)
    register_handlers_user_group(dp)

    await dp.start_polling(dp)

if __name__=='__main__':
    asyncio.run(main())

