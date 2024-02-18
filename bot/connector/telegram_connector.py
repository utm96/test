import telebot
from common.helper import read_config

config = read_config('configurations.ini')

BOT_KEY = config['telegram']['BOT_KEY']
CHAT_ID = config['telegram']['CHAT_ID']

def send_message_tele(message):
    print("BOT_KEY: " + BOT_KEY)
    print("CHAT_ID: " + CHAT_ID)
    bot = telebot.TeleBot(BOT_KEY)
    print(bot)
    bot.send_message(CHAT_ID, message)


# tele("hello")