import asyncio
import logging
import sys
import fileinput
from operator import truediv

import aiogram.types.inline_keyboard_markup
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils import keyboard

import json


def init(config_path: str) -> (str):
    try:
        config = json.load(open(config_path))
        token = config["token"]
        return token

    except FileNotFoundError as e:
        print(f"bad filepath {config_path}")
        sys.exit(1)

    except json.decoder.JSONDecodeError as e:
        print(f"json parsing failed {e}")
        sys.exit(2)

    except Exception as e:
        print(f"unexpected error while parsing config {e}")
        sys.exit(-1)


TOKEN = init("config.json")
dp = Dispatcher()
MESSAGE = None

builder = keyboard.ReplyKeyboardBuilder()
builder.button(text='''📖What's included in PREMIUM subscription?''')
builder.button(text='❓How does it work?')
builder.button(text='💳Price')
builder.button(text='📢Reviews')
builder.button(text='📊Stats')
builder.max_buttons = 2
builder.max_width = 2
builder.adjust(2,1,2)
markup = builder.as_markup()
markup.resize_keyboard = True


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("a", reply_markup=markup)


@dp.message(F.text == '''📖What's included in PREMIUM subscription?''')
async def what_is_subscribe(message: Message) -> None:
    try:
        await message.answer("Дерево", reply_markup=markup)
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")

@dp.message(F.text == '''❓How does it work?''')
async def how_subscribe_work_handler(message: Message) -> None:
    try:
        await message.answer("Дерево", reply_markup=markup)
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")


@dp.message(F.text == '''📢Reviews''')
async def reviews_handler(message: Message) -> None:
    try:
        await message.answer("Дерево", reply_markup=markup)
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")


@dp.message(F.text == '''📊Stats''')
async def stats_handler(message: Message) -> None:
    try:
        await message.answer_photo(photo=FSInputFile(path="img.png"), reply_markup=markup)
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")


@dp.message(F.text == '''💳Price''')
async def price_handler(message: Message) -> None:
    try:
        inline_builder = keyboard.InlineKeyboardBuilder()
        inline_builder.button(text="1 month", callback_data="1")
        inline_builder.button(text="3 month", callback_data="2")
        inline_builder.button(text="LIFE", callback_data="3")
        await message.answer(text="Дерево", reply_markup=inline_builder.as_markup())
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")

@dp.callback_query(F.data == "1")
async def adsdkalsd(call: CallbackQuery):
    await call.message.edit_text("meow --- 300$ ")
    keyboard_new = keyboard.InlineKeyboardBuilder()
    keyboard_new.button(text="BUY", url="vk.com")
    await call.message.edit_reply_markup(reply_markup=keyboard_new.as_markup())

@dp.callback_query(F.data == "2")
async def adsdkalsd(call: CallbackQuery):
    await call.message.edit_text("meow --- 900$ ")
    keyboard_new = keyboard.InlineKeyboardBuilder()
    keyboard_new.button(text="BUY", url="vk.com")
    await call.message.edit_reply_markup(reply_markup=keyboard_new.as_markup())

@dp.callback_query(F.data == "3")
async def adsdkalsd(call: CallbackQuery):
    await call.message.edit_text("meow --- 1400$ ")
    keyboard_new = keyboard.InlineKeyboardBuilder()
    keyboard_new.button(text="BUY", url="vk.com")
    await call.message.edit_reply_markup(reply_markup=keyboard_new.as_markup())



# мы получили параметры для бота с помощью init(), а затем запустили опрос, используя dispatcher,
# тогда для любого сообщения у нас есть несколько обработчиков для их обработки
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())