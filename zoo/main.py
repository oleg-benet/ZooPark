import asyncio
import logging
from aiogram.methods import DeleteWebhook

from handlers.custody_handlers_1 import router_cust
from handlers.questions_handlers_1 import router_quest
from handlers.enter_handlers_1 import router_enter
from create_bot import dp, bot
from handlers.menu_handlers import router_options



async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    dp.include_routers(router_quest, router_enter, router_cust, router_options)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
