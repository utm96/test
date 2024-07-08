import telebot
from common.helper import read_config

config = read_config('./configurations.ini')

BOT_KEY = config['telegram']['BOT_KEY']
CHAT_ID = config['telegram']['CHAT_ID']

bot_key = '6841144574:AAF2Qxf_90IHC-ZOJxWz0NHSMgq6zgMHu14'
chat_id = "-4117127789"  # Replace with your chat ID or group ID


def send_message_tele(message):
    print("BOT_KEY: " + BOT_KEY)
    print("BOT_KEY: " + bot_key)

    print("CHAT_ID: " + CHAT_ID)
    print("CHAT_ID: " + chat_id)

    bot = telebot.TeleBot(str(BOT_KEY))
    print(bot)
    bot.send_message(str(CHAT_ID), message)

def send_file_tele(file_path = 'result.csv', caption = "Result file"):
    print("BOT_KEY: " + BOT_KEY)
    print("BOT_KEY: " + bot_key)

    print("CHAT_ID: " + CHAT_ID)
    print("CHAT_ID: " + chat_id)

    bot = telebot.TeleBot(str(BOT_KEY))
    with open(file_path, 'rb') as file:
        bot.send_document(CHAT_ID, file, caption=caption)


# tele("hello")