import logging
import telegram
import utils
import bot
import chat_gpt
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
tg = telegram.Parser(utils.get_info_from_config('config.json', 'telegram_settings'))
ai_indo = chat_gpt.CryptoAi(utils.get_info_from_config('config.json', 'openai_indo'))
ai_hindi = chat_gpt.CryptoAi(utils.get_info_from_config('config.json', 'openai_hindi'))
ai_arab = chat_gpt.CryptoAi(utils.get_info_from_config('config.json', 'openai_arab'))
# ai_eng = chat_gpt.CryptoAi(utils.get_info_from_config('config.json', 'openai_eng'))


# inst1 = bot.CryptoInst(utils.get_info_from_config('config.json', 'instagram_accounts')[0], ai=ai_eng)
inst1 = bot.CryptoInst(utils.get_info_from_config('config.json', 'instagram_accounts')[3], ai=ai_arab)
inst2 = bot.CryptoInst(utils.get_info_from_config('config.json', 'instagram_accounts')[1], ai=ai_indo)
inst3 = bot.CryptoInst(utils.get_info_from_config('config.json', 'instagram_accounts')[2], ai=ai_hindi)


async def main():
    await tg.auth()
    await asyncio.gather(inst1.start(tg=tg), inst2.start(tg=tg) ,inst3.start(tg=tg),
                         inst1.process_signals(tg=tg), inst2.process_signals(tg=tg), inst3.process_signals(tg=tg))
    # await inst2.start(tg=tg)
if __name__ == '__main__':
    asyncio.run(main())