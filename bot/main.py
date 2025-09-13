import os, logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, MenuButtonWebApp, Update
from fastapi import FastAPI, Request, HTTPException
import uvicorn

# настройки
logging.basicConfig(level=logging.INFO)
BOT_TOKEN  = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://science-dating.onrender.com")
PUBLIC_URL = (os.getenv("PUBLIC_URL") or "").rstrip("/")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var is not set")

# aiogram
bot = Bot(BOT_TOKEN)
dp  = Dispatcher()

@dp.message(Command("start"))
async def on_start(m: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await m.answer("Привет! Жми кнопку ниже 👇", reply_markup=kb)

@dp.message(Command("demo"))
async def on_demo(m: types.Message):
    await on_start(m)

@dp.message(Command("help"))
async def on_help(m: types.Message):
    await m.answer("/start — открыть мини-приложение\n/demo — демо\n/help — помощь")

# fastapi
app = FastAPI(title="Science Dating Bot")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"ok": True, "service": "science-dating-bot"}

@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != BOT_TOKEN:
        raise HTTPException(status_code=403, detail="wrong token")
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@dp.startup()
async def _on_startup():
    # команды и кнопка меню
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Открыть мини-приложение"),
        types.BotCommand(command="demo",  description="Демо"),
        types.BotCommand(command="help",  description="Помощь"),
    ])
    try:
        await bot.set_chat_menu_button(MenuButtonWebApp(
            text="Открыть мини-приложение",
            web_app=WebAppInfo(url=WEBAPP_URL)
        ))
    except Exception:
        pass
    # авто-вебхук, если задан PUBLIC_URL
    if PUBLIC_URL:
        url = f"{PUBLIC_URL}/webhook/{BOT_TOKEN}"
        try:
            await bot.set_webhook(url, drop_pending_updates=True)
            logging.info("Webhook set to %s", url)
        except Exception as e:
            logging.warning("Failed to set webhook: %s", e)

@dp.shutdown()
async def _on_shutdown():
    await bot.session.close()

if __name__ == "__main__":
    uvicorn.run("bot.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
