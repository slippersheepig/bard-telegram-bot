from os import environ
import asyncio
import telebot
from Bard import Chatbot

# get config
Secure_1PSID = environ.get("BARD__Secure_1PSID")
Secure_1PSIDTS = environ.get("BARD__Secure_1PSIDTS")
chatbot = Chatbot(Secure_1PSID, Secure_1PSIDTS)

# init telegram bot
bot_token = environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(bot_token, parse_mode="HTML")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "This bot uses the google bard")

@bot.message_handler(func=lambda m: True)
def send_gpt(message):
    print("get response...")
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = chatbot.ask(message.text)
        bot.reply_to(message, response["content"])
    except BaseException as e:
        bot.reply_to(message, str(e))

# run the bot
asyncio.run(bot.polling())
