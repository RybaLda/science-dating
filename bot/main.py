import os
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonWebApp, WebAppInfo
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from fastapi import FastAPI, Request
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://science-dating-web.onrender.com')
PUBLIC_URL = os.getenv('PUBLIC_URL')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# FastAPI app for webhook
app = FastAPI(title="Science Dating Bot")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔬 Открыть Science Dating",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(
        "🔬 Добро пожаловать в Science Dating!\n\n"
        "Найди свою научную половинку среди единомышленников. "
        "Нажмите кнопку ниже, чтобы открыть приложение.",
        reply_markup=keyboard
    )

@dp.message(Command("demo"))
async def cmd_demo(message: types.Message):
    """Handle /demo command"""
    demo_url = f"{WEBAPP_URL}?demo=1"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 Быстрый демо-режим",
            web_app=WebAppInfo(url=demo_url)
        )]
    ])
    
    await message.answer(
        "🚀 Демо-режим Science Dating\n\n"
        "Попробуйте приложение в демо-режиме с готовыми профилями. "
        "Нажмите кнопку ниже, чтобы начать.",
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Handle /help command"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔬 Открыть приложение",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(
        "❓ Помощь по Science Dating\n\n"
        "🔬 <b>Science Dating</b> - это приложение для знакомств среди ученых и исследователей.\n\n"
        "📱 <b>Основные функции:</b>\n"
        "• Свайпы профилей с фильтрацией\n"
        "• Система матчей и чатов\n"
        "• Создание профиля с фото\n"
        "• Панель управления персонажами\n\n"
        "🚀 <b>Команды:</b>\n"
        "/start - Главное меню\n"
        "/demo - Демо-режим\n"
        "/help - Эта справка\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message()
async def handle_message(message: types.Message):
    """Handle all other messages"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔬 Открыть Science Dating",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(
        "Привет! Я бот Science Dating. "
        "Используйте команды /start, /demo или /help для навигации.",
        reply_markup=keyboard
    )

async def on_startup():
    """Bot startup actions"""
    logger.info("Bot is starting up...")
    
    # Set bot commands
    commands = [
        types.BotCommand(command="start", description="🚀 Главное меню"),
        types.BotCommand(command="demo", description="🔬 Демо-режим"),
        types.BotCommand(command="help", description="❓ Помощь")
    ]
    await bot.set_my_commands(commands)
    
    # Set menu button
    menu_button = MenuButtonWebApp(text="Science Dating", web_app=WebAppInfo(url=WEBAPP_URL))
    await bot.set_chat_menu_button(menu_button=menu_button)
    
    # Set webhook if PUBLIC_URL is provided
    if PUBLIC_URL:
        webhook_url = f"{PUBLIC_URL}/webhook/{BOT_TOKEN}"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        logger.info("PUBLIC_URL not set, webhook not configured")

async def on_shutdown():
    """Bot shutdown actions"""
    logger.info("Bot is shutting down...")
    await bot.session.close()

# Webhook endpoint for FastAPI
@app.post(f"/webhook/{BOT_TOKEN}")
async def webhook_handler(request: Request):
    """Handle webhook updates"""
    try:
        data = await request.json()
        update = types.Update(**data)
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "bot": "Science Dating"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Science Dating Bot API",
        "webapp_url": WEBAPP_URL,
        "webhook_configured": bool(PUBLIC_URL)
    }

async def main():
    """Main function to run the bot"""
    # Register startup and shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    if PUBLIC_URL:
        # Run with webhook (production)
        logger.info("Starting bot with webhook...")
        # The FastAPI app will handle webhook requests
        # Bot will be started via uvicorn
    else:
        # Run with polling (development)
        logger.info("Starting bot with polling...")
        await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    
    if PUBLIC_URL:
        # Production mode with webhook
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            reload=False
        )
    else:
        # Development mode with polling
        asyncio.run(main())
