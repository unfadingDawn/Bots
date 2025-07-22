import asyncio
from pathlib import Path

import instagrapi
import random
import time

import database
import database as db
import datetime
import telegram
import utils


class CryptoInst:

    @staticmethod
    def challenge_code_handler(username, choice):
        a = input('write code: ')
        return a


    def __init__(self, config, ai):
        self.ai = ai
        self.client = instagrapi.Client()
        self.login = config["username"]
        self.password = config["password"]
        self.enabled = config["enabled"]
        if not config["proxy"] == '0':
            self.proxy = config["proxy"]
            self.client.set_proxy(dsn=self.proxy)
        self.session = config["session"]
        self.two_factor = config["2FA"]
        self.prod_count = 0
        self.d_count = 0
        self.comm_count = 0
        time.sleep(random.randint(1, 5))
        self.client.load_settings(Path(self.session))
        self.client.challenge_code_handler = self.challenge_code_handler
        if self.two_factor:
            seed = config['seed']
            self.client.login(self.login, self.password, verification_code=self.client.totp_generate_code(seed))
        else:
            self.client.login(self.login, self.password)
        self.client.dump_settings(Path(self.session))
        time.sleep(random.randint(1, 5))


    async def process_reels(self,  tg: telegram.Parser,
                            config=utils.get_info_from_config('config.json', 'bot_settings')):
        limits = utils.get_info_from_config('config.json', 'safe_limits')
        temp_comment = 0
        temp_direct = 0
        temp_pdirect = 0
        reels = self.client.user_clips(f"{self.client.user_id}", amount=config['reels_fetch_count'])
        await asyncio.sleep(random.randint(10, 15))
        if self.comm_count < limits['comments']['per_day']:
            for reel in reels:
                time.sleep(random.randint(4, 7))
                if temp_comment < limits['comments']['per_hour']:
                    if self.comm_count < limits['comments']['per_day']:
                        num_comments = reel.comment_count
                        if num_comments != 0:
                            comments = self.client.media_comments(media_id=f'{reel.id}', amount=0)
                            await asyncio.sleep(random.randint(3, 5))
                            for i in range(0, num_comments):
                                if temp_comment < limits['comments']['per_hour']:
                                    break
                                if self.comm_count < limits['comments']['per_day']:
                                    break
                                if (datetime.date.today() - comments[i].created_at_utc.date()).days > 2:
                                    continue
                                if not db.comment_exists(comments[i].created_at_utc.isoformat()):
                                    if comments[i].replied_to_comment_id is not None:
                                        continue
                                    if comments[i].user.username == self.client.username:
                                        continue
                                    if "coin" == comments[i].text.lower():
                                        if self.d_count < limits['direct']['per_day']:
                                            if temp_direct < limits['direct']['per_hour']:
                                                ans = self.ai.get_response("coin")
                                                ans += '\n'
                                                ans += tg.parse_signal_with_adding(int(comments[i].user.pk), datetime.date.today().isoformat())
                                                self.client.direct_send(text=ans, user_ids=[int(comments[i].user.pk)])
                                                db.insert_comment(int(comments[i].pk), comments[i].created_at_utc.isoformat())
                                                temp_direct += 1
                                                self.d_count += 1
                                    else:
                                        self.client.media_comment(media_id=reel.pk, text=self.ai.get_response(f'Комментарий: {comments[i].text}'),
                                                  replied_to_comment_id=int(comments[i].pk))
                                        await asyncio.sleep(random.randint(config['comment_processing_interval'][0],
                                                  config['comment_processing_interval'][1]))
                                        db.insert_comment(int(comments[i].pk), comments[i].created_at_utc.isoformat())
                                        self.comm_count += 1
                                        temp_comment += 1
                else:
                    break

        if self.prod_count < limits['proactive_direct']['per_day']:
            for reel in reels:
                if self.prod_count < limits['proactive_direct']['per_day']:
                    if temp_pdirect < limits['proactive_direct']['per_hour']:
                        likers = self.client.media_likers(reel.pk)
                        await asyncio.sleep(random.randint(config['likers_fetch_delay'][0], config['likers_fetch_delay'][1]))
                        for liker in likers:
                            if not db.like_exists(liker.username):
                                if self.prod_count < limits['proactive_direct']['per_day']:
                                    if temp_pdirect < limits['proactive_direct']['per_hour']:
                                        ans = ''
                                        text = await tg.parse_message_signal()
                                        ans += self.ai.get_response(request='Напиши приветственное сообщение пользователя в директ')
                                        ans += '\n\n'
                                        ans += text
                                        self.client.direct_send(ans, user_ids=[int(liker.pk)])
                                        db.insert_like(liker.username)
                                        await asyncio.sleep(random.randint(config['proactive_dm_interval'][0], config['proactive_dm_interval'][1]))
                                        self.prod_count += 1
                                        temp_pdirect += 1
                else:
                    break

    async def process_direct(self, tg: telegram.Parser,
                             config=utils.get_info_from_config('config.json', 'bot_settings')):
        limits = utils.get_info_from_config('config.json', 'safe_limits')
        temp_direct = 0
        direct = self.client.direct_threads(amount=20, selected_filter="unread")
        time.sleep(random.randint(10, 15))
        for thread in direct:
            time.sleep(random.randint(4, 7))
            if self.d_count < limits['direct']['per_day']:
                if temp_direct < limits['direct']['per_hour']:
                    try:
                        if not database.signal_exists(int(thread.pk)):
                            ans = self.ai.get_response(thread.messages[0].text)
                            ans += '\n\n'
                            ans += await tg.parse_signal_with_adding(int(thread.pk), datetime.date.today().isoformat())
                            self.client.direct_send(text=ans, thread_ids=[int(thread.pk)])
                            self.d_count += 1
                            temp_direct += 1
                            await asyncio.sleep(random.randint(config['dm_processing_interval'][0], config['dm_processing_interval'][1]))
                        else:
                            ans = self.ai.get_response(thread.messages[0].text)
                            self.client.direct_send(text=ans, thread_ids=[int(thread.pk)])
                            self.d_count += 1
                            temp_direct += 1
                            await asyncio.sleep(random.randint(config['dm_processing_interval'][0],
                                                               config['dm_processing_interval'][1]))


                    except Exception as e:
                        print(e)
                        await asyncio.sleep(random.randint(config['error_retry_interval'][0], config['error_retry_interval'][1]))
                else:
                    break

    async def start(self, tg: telegram.Parser):
        while True:
            for i in range(0, 24):
                try:
                    await self.process_reels(tg=tg)
                    await self.process_direct(tg=tg)
                    await asyncio.sleep(random.randint(3600, 3605))
                except Exception as e:
                    print(e)
            self.d_count = 0
            self.comm_count = 0
            self.prod_count = 0


    async def process_signals(self, tg: telegram.Parser):
        while True:
            users = database.get_signals()
            limits = utils.get_info_from_config('config.json', 'safe_limits')
            temp_d = 0
            for user in users:
                ans = await tg.parse_message_succ_message(user[1])
                if ans is not None:
                    if self.d_count < limits['direct']['per_day']:
                        if temp_d < limits['direct']['per_hour']:
                            self.client.direct_send(text=ans, thread_ids=[int(user[0])])
                            database.insert_succsignal(int(user[0]), user[1], user[2])
                            database.delete_signal(int(user[0]))
                            self.d_count += 1
                else:
                    if (datetime.date.today() - datetime.date.fromisoformat(user[2])).days > 9:
                        ids = int(user[0])
                        database.delete_signal(int(user[0]))
                        ans = await tg.parse_signal_with_adding(ids, datetime.date.today().isoformat())
                        self.client.direct_send(text=ans, thread_ids=[ids])
            succ = database.get_succsignals()
            for sig in succ:
                ids = int(sig[0])
                database.delete_succsignal(int(sig[0]))
                ans = await tg.parse_message_signal()
                self.client.direct_send(text=ans, thread_ids=[ids])
            await asyncio.sleep(random.randint(43200, 43206))