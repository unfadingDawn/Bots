import asyncio
import time
from random import randint
from time import sleep
import database

import telethon
from telethon import TelegramClient

import utils


class Parser:
    def __init__(self, config):
        self.id = config['telegram_api_id']
        self.api_hash = config['telegram_api_hash']
        self.name = 'user_session'
        self.channel_id = config['telegram_channel']
        self.client = TelegramClient(self.name, self.id, self.api_hash)

    async def parse_message_signal(self):
        messages = await self.client.get_messages(self.channel_id, 1000)
        time.sleep(randint(1,5))
        pair = ''
        mes = ''
        for message in messages:
            if '🎯 Targets:' in message.message:
                mes += message.message
                break
        return mes

    async def parse_message_succ_message(self, pair: str):
        messages = await self.client.get_messages(self.channel_id, 1000)
        temp = 0
        for i in range(0, len(messages)):
            if pair in messages[i].message:
                temp = i
        for i in range(0, len(messages)):
            if ('TARGET #4 DONE' in messages[i].message or 'TARGET #3 DONE' in messages[i].message) and pair in messages[i].message and temp < i:
                return messages[i].message
        return None
    async def parse_signal_with_adding(self, id: int, date: str):
        message = await self.parse_message_signal()
        pair = ''
        for i in range(0, len(message.split('\n')[0])):
            if i == 0:
                continue
            else:
                pair += message.split('\n')[0][i]
        database.insert_signal(id, pair, date)
        return message



    async def auth(self):
        await self.client.connect()


a = Parser(utils.get_info_from_config('config.json', 'telegram_settings'))
async def main():
    await a.auth()
    print(await a.parse_message_signal())

if __name__ == '__main__':
    asyncio.run(main())