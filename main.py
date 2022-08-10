from typing import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import aiogram.utils.markdown as fmt
import os
import asyncio
import wether_api
import math
from datetime import datetime

load_dotenv()

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start",
                         description="В начало"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=os.environ['TOKEN'])
    dp = Dispatcher(bot, storage=MemoryStorage())

    @dp.message_handler(commands="start")
    async def start(message: types.Message):
        wether_api.set_user(message.chat.id)
        await message.answer('Привет! \nОтправь свою геолокацию')

    @dp.message_handler(content_types=['location'])
    async def handle_location(message: types.Message):
        latitude, longitude = message.location
        data = wether_api.get(latitude,longitude)


        sun_rise = datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
        sun_set = datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')

        await message.answer("Сейчас: <b>{0}</b>\nТемпература: <b>{1}</b> Ощущается как: <b>{2}</b>\nВосход: <b>{3}</b> Закат: <b>{4}</b>".format(
            data["weather"][0]["description"],
            math.floor(int(data["main"]["temp"])-274),
            math.floor(int(data["main"]["feels_like"])-274),
            sun_rise,
            sun_set
        ),parse_mode=types.ParseMode.HTML)

    await set_commands(bot)
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)

