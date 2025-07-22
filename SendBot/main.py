import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ChatMemberUpdated
from aiogram.utils import keyboard

import json
from aiogram.utils.keyboard import InlineKeyboardBuilder

import utils
from utils import add_link_to_file

mode = 0


def init(config_path: str) -> str:
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

builder = keyboard.ReplyKeyboardBuilder()
builder.button(text='Добавить рефку')
builder.button(text='Добавить бонусную ссылку')
builder.button(text='Добавить кнопку')
builder.button(text='Сгенерировать мегу')
builder.button(text='Запостить мегу')
builder.adjust(2,2,1)


@dp.my_chat_member()
async def check_channel(chat_upd: ChatMemberUpdated):
    try:
        if chat_upd.new_chat_member.status != "kicked":
            with (open("waiting_channels.txt", "a") as myfile):
                if chat_upd.new_chat_member.can_post_messages:
                    link = await chat_upd.chat.create_invite_link("new")
                    myfile.write(f'"{link.invite_link}"_"{chat_upd.chat.full_name}"_"{chat_upd.chat.id}"\n')
                    inline = InlineKeyboardBuilder()
                    inline.button(text="Подтвердить", callback_data=f"1_{link.invite_link}")
                    inline.button(text="Отклонить", callback_data=f'0_{link.invite_link}')
                    await chat_upd.bot.send_message(chat_id=852042889, text=f"Бот имеет достаточные права в канале {link.invite_link}", reply_markup=inline.as_markup())
                    await chat_upd.bot.send_message(chat_id=747083355,
                                                    text=f"Бот имеет достаточные права в канале {link.invite_link}",
                                                    reply_markup=inline.as_markup())
        else:
            utils.delete_link("approved_channels.txt", name = chat_upd.chat.full_name)
    except Exception as e:
        await chat_upd.bot.send_message(chat_id=852042889,text=f"Что-то пошло не так ({e})")
        await chat_upd.bot.send_message(chat_id=747083355, text=f"Что-то пошло не так ({e})")



@dp.callback_query()
async def approve_channel(callback_data):
    try:
        link: str
        flag, data_link = int(callback_data.data.split("_")[0]), callback_data.data.split("_")[1]
        if flag:
            with open("waiting_channels.txt", "r") as file:
                link = utils.find_link(file.read(), data_link)
                if link is not None:
                    with open("approved_channels.txt", "a") as apr:
                        apr.write(f"{link}\n")
                        utils.delete_link("waiting_channels.txt", data_link)
        else:
            with open("waiting_channels.txt", "r") as file:
                utils.delete_link("waiting_channels.txt", data_link)#!!!
    except Exception as e:
        await callback_data.bot.send_message(chat_id=852042889, text=f"Что-то пошло не так ({e})")
        await callback_data.bot.send_message(chat_id=747083355, text=f"Что-то пошло не так ({e})")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.chat.id == 852042889 or message.chat.id == 747083355:
        await message.answer("Выбери кнопку ниже!", reply_markup=builder.as_markup())


@dp.message(F.text.lower() == 'добавить рефку')
async def add_ref(message: Message) -> None:
    try:
        if message.chat.id == 852042889 or message.chat.id == 747083355:
            await message.answer('Введите ссылки с названием для них в формате: "ссылка"_"называние"')
            global mode
            mode = 1
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")

@dp.message(F.text.lower() == 'добавить кнопку')
async def add_button(message: Message) -> None:
    try:
        if message.chat.id == 852042889 or message.chat.id == 747083355:
            await message.answer('Введите ссылки с названием для них в формате: "ссылка"_"название"')
            global mode
            mode = 3
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")


@dp.message(F.text.lower() == 'запостить мегу')
async def post_mega(message: Message) -> None:
    try:
        mega: str
        inline_keyboard = InlineKeyboardBuilder()
        with open("buttons.txt") as file:
            line = file.readline()
            while len(line) != 0:
                link, name = utils.parse_button(line)
                inline_keyboard.button(text=name, url=link)
                line = file.readline()
        inline_keyboard.adjust(1)
        with open("mega.txt", 'r') as file:
            mega = file.read()
        with open("approved_channels.txt", "r") as file:
            line = file.readline()
            while len(line) != 0:
                await message.bot.send_message(chat_id=utils.parse_chat_id(line), text=mega, reply_markup=inline_keyboard.as_markup())
                line = file.readline()
    except Exception as e:
        await message.answer(f"Somthing wrong: {e}")


@dp.message(F.text.lower() == 'сгенерировать мегу')
async def add_button(message: Message) -> None:
    try:
        if message.chat.id == 852042889 or message.chat.id == 747083355:
            answer: str = ''
            first_level = ''
            second_level = ''
            third_level = ''
            #decompose!!!
            with open("refs.txt") as file:
                line = file.readline()
                while len(line) != 0:
                    answer += utils.parse_link(line)
                    line = file.readline()
            with open("approved_channels.txt", "r") as file:
                line = file.readline()
                while len(line) != 0:
                    quantity_subs = await message.bot.get_chat_member_count(utils.parse_chat_id(line))
                    if quantity_subs <= 5000:
                        first_level += utils.parse_link(line)
                    elif 5000 < quantity_subs <= 10000:
                        second_level += utils.parse_link(line)
                    else:
                        third_level += utils.parse_link(line)
                    line = file.readline()
            answer += "5k subscribers"
            parts = first_level.split('\n')
            for i in range(0, len(parts)):
                answer += f'{parts[i]}\n'
            answer += "10k subscribers"
            parts = second_level.split('\n')
            for i in range(0, len(parts)):
                answer += f'{parts[i]}\n'
            answer += "10k+ subscribers"
            parts = third_level.split('\n')
            for i in range(0, len(parts)):
                answer += f'{parts[i]}\n'
            with open("bonus.txt") as file:
                line = file.readline()
                while len(line) != 0:
                    answer += utils.parse_link(line)
                    line = file.readline()
            inline_keyboard = InlineKeyboardBuilder()
            with open("buttons.txt") as file:
                line = file.readline()
                while len(line) != 0:
                    link, name = utils.parse_button(line)
                    inline_keyboard.button(text=name, url=link)
                    line = file.readline()
            inline_keyboard.adjust(1)
            with open("mega.txt", "w") as file:
                file.write(answer)
            await message.answer(text=answer, reply_markup=inline_keyboard.as_markup(), parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")



@dp.message(F.text.lower() == 'добавить бонусную ссылку')
async def add_bonus(message: Message) -> None:
    try:
        if message.chat.id == 852042889 or message.chat.id == 747083355:
            await message.answer('Введите ссылки с названием для них в формате: "ссылка"_"называние"')
            global mode
            mode = 2
    except Exception as e:
        await message.answer(f"Что-то пошло не так ({e})")


@dp.message()
async def text_handler(message: Message) -> None:
    try:
        if message.chat.id == 852042889 or message.chat.id == 747083355:
            if mode == 1:
                if add_link_to_file('refs.txt', message.text):
                    await message.answer(text='Ссылка успешно добавлена')
                else:
                    await message.answer(text='Ссылка для рефки имеет некорректный вид')
            elif mode == 2:
                if add_link_to_file('bonus.txt', message.text):
                    await message.answer(text='Ссылка успешно добавлена')
                else:
                    await message.answer(text='Ссылка для бонуса имеет некорректный вид')
            elif mode == 3:
                if add_link_to_file('buttons.txt', message.text):
                    await message.answer(text='Ссылка успешно добавлена')
                else:
                    await message.answer(text='Ссылка для кнопки имеет некорректный вид')
    except Exception as e:
        await message.answer(f"Что-то не так ({e.with_traceback(None)})")




async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
