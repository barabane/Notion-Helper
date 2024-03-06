import os
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher, F, types

from utils import add_link, add_page, get_shopping_list

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN_TEST'), parse_mode="HTML")
dp = Dispatcher()

scheduler = AsyncIOScheduler()
scheduler.add_job(func=get_shopping_list, trigger='cron', hour=18, minute=30, start_date=datetime.now(), args=(bot,))


@dp.message(F.forward_from_chat)
async def forward_handler(msg: types.Message):
    response = add_link(user_id=msg.from_user.id,
                        text=f"https://t.me/{msg.forward_from_chat.username}/{msg.forward_from_message_id}")
    if response.status_code == 200:
        await msg.answer(f"<a href='{response.json()['url']}'>Ссылка</a> на пост сохранена ✅")
    else:
        await msg.answer("Что-то пошло не так 🥵")


@dp.message(F.text.regexp("^https?:\\/\\/", search=True))
async def link_handler(msg: types.Message):
    response = add_link(user_id=msg.from_user.id, text=msg.text)
    if response.status_code == 200:
        await msg.answer(f"<a href='{response.json()['url']}'>Ссылка</a> добавлена ✅")
    else:
        await msg.answer("Что-то пошло не так 🥵")


@dp.message(F.text)
async def text_handler(msg: types.Message):
    response = add_page(user_id=msg.from_user.id, text=msg.text)
    if response.status_code == 200:
        await msg.answer(f"<a href='{response.json()['url']}'>Заметка</a> создана ✅")
    else:
        await msg.answer("Что-то пошло не так 🥵")


async def main():
    logger.info("polling started")
    scheduler.start()
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main=main())
