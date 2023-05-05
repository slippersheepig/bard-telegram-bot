from os import environ
import asyncio
from telebot.async_telebot import AsyncTeleBot
from Bard import Chatbot

# get config
token = environ.get("BARD_TOKEN")

# init telegram bot
bot_token = environ.get("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(bot_token, parse_mode="MARKDOWN")

# init chatbot
chatbot = Chatbot(token)
print("initial bot...")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
async def send_welcome(message):
    await bot.reply_to(message, "This bot uses the google bard")
    
# define an async function to continuously display the input state
async def display_typing(chat_id):
    while True:
        await bot.send_chat_action(chat_id, 'typing')
        await asyncio.sleep(0.5)

# define a message handler to send the response and start the input state display
@bot.message_handler(func=lambda m: True)
async def send_gpt(message):
    print("get response...")
    try:
        #start the input state display
        typing_task = asyncio.create_task(display_typing(message.chat.id))
        response = chatbot.ask(message.text)
        #stop the input state display and send the response
        typing_task.cancel()
        await bot.reply_to(message, response["content"])
    except Exception as e:
        await bot.reply_to(message, e)

# run the bot
asyncio.run(bot.polling())
