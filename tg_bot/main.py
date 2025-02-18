import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config_bot import token, my_id

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()


async def send_message():
    await bot.send_message(chat_id=my_id, text='Пора проверить МедРокет!')


async def check_file():
    while True:
        try:
            with open('status_indicator.txt', mode='r', encoding='utf-8') as file:
                check = file.read().strip()
        except:
            ...

        if check == '1':
            logging.info("Отправили сообщение.")
            await send_message()
            sys.exit()
        await asyncio.sleep(10)


async def main():
    check_task = asyncio.create_task(check_file())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())