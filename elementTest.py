import telebot


bot = telebot.TeleBot('7974076717:AAF298hMSaYR_RZGfH9wiPstfoThWjpm5j8')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, я нейросеть!')


bot.infinity_polling(timeout=10, long_polling_timeout = 5, skip_pending=True)