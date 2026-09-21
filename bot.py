import asyncio
import os
from groq import Groq
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

client = Groq(api_key=GROQ_KEY)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

history = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    history[message.from_user.id] = []
    await message.answer("Привет! Я бот с нейросетью. Напиши мне что-нибудь.")

@dp.message(Command("reset"))
async def reset(message: types.Message):
    history[message.from_user.id] = []
    await message.answer("История очищена.")

@dp.message()
async def chat(message: types.Message):
    user_id = message.from_user.id
    if user_id not in history:
        history[user_id] = []
    history[user_id].append({"role": "user", "content": message.text})
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=history[user_id]
        )
        answer = response.choices[0].message.content
        history[user_id].append({"role": "assistant", "content": answer})
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
