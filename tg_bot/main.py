import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config_bot import token, my_id

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()


async def check_file():
    while True:
        s = ''
        try:
            with (open('status_indicator.txt', mode='r', encoding='utf-8')
                  as file):
                check = file.read()
        except Exception as e:
            logging.info(f"Ошибка: {e}", exc_info=None)

        if check:
            logging.info("Отправили сообщение.")
            await send_message(check)
            sys.exit()

        await asyncio.sleep(10)


async def send_message(s: str):
    await bot.send_message(chat_id=my_id, text=f'Пора проверить МедРокет! {s}')


@dp.message(Command('check'))
async def check_work(message: types.Message):
    await bot.send_message(chat_id=my_id, text='Подход, подход, еще подход.')


async def main():
    check_task = asyncio.create_task(check_file())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())