from os import environ
import asyncio
from telebot.async_telebot import AsyncTeleBot
from Bard import AsyncChatbot

# get config
Secure_1PSID = environ.get("BARD__Secure_1PSID")
Secure_1PSIDTS = environ.get("BARD__Secure_1PSIDTS")

# init telegram bot
bot_token = environ.get("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(bot_token, parse_mode="HTML")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
async def send_welcome(message):
    await bot.reply_to(message, "This bot uses the google bard")

@bot.message_handler(func=lambda m: True)
async def send_gpt(message):
    chatbot = AsyncChatbot(Secure_1PSID, Secure_1PSIDTS)
    print("get response...")
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
#        await bot.send_message(message.chat.id, "思考中，请稍后")
        response = await chatbot.create(message.text)
        await bot.reply_to(message, response["content"])
    except BaseException as e:
        await bot.reply_to(message, str(e))

# run the bot
asyncio.run(bot.polling())
