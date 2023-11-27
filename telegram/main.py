import telebot

API_TOKEN = open("API_TOKEN.txt", "rt").read()
bot = telebot.TeleBot(API_TOKEN)
blacklist = open("blacklist.txt", "rt").read().split(';')
while True:
    try:
        @bot.message_handler(func=lambda x: True)
        def output(message):
            if str(message.from_user.id) in blacklist:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            print(message.from_user.id)
            print(message.text)

        bot.polling()

    except: pass
