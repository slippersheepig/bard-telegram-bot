from os import environ
import asyncio
from telebot.async_telebot import AsyncTeleBot
from Bard import Chatbot

# get config
token = environ.get("BARD_TOKEN")

# init telegram bot
bot_token = environ.get("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(bot_token, parse_mode="MARKDOWNV2")

# init chatbot
chatbot = Chatbot(token)
print("initial bot...")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
async def send_welcome(message):
    await bot.reply_to(message, "This bot uses the google bard")

@bot.message_handler(func=lambda m: True)
async def send_gpt(message):
    print("get response...")
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
#        await bot.send_message(message.chat.id, "思考中，请稍后")
        response = chatbot.ask(message.text)
        await bot.reply_to(message, response["content"].replace(/_/gi, "\\_").replace(/-/gi, "\\-").replace("~", "\\~").replace(/`/gi, "\\`").replace(/\./g, "\\."))
    except Exception as e:
        await bot.reply_to(message, e)

# run the bot
asyncio.run(bot.polling())
