import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# In a real project, use environment variables (e.g., python-dotenv)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
# The URL where your Mini App (index.html) is hosted
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-mini-app-url.com")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Handler for the /start command.
    Sends a welcoming message with a button to launch the Mini App.
    """
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Открыть Тунец 🐟", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    ))

    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n\n"
        "Добро пожаловать в приложение **Тунец**. "
        "Нажми на кнопку ниже, чтобы запустить Mini App.",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

async def main():
    logger.info("Starting bot...")
    # Skip updates that accumulated while the bot was offline
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
