import telebot

bot = telebot.TeleBot('7974076717:AAF298hMSaYR_RZGfH9wiPstfoThWjpm5j8')

@bot.message_handler(commands=['start'])
def main(message):
    html_content = """
    <b>Привет!</b> Это пример HTML-страницы, отправленной через Telegram Bot API.
    <i>Этот текст написан курсивом.</i>
    <u>Этот текст подчеркнут.</u>
    <s>Этот текст зачеркнут.</s>
    <a href="https://www.example.com">Это ссылка на пример.com</a>
    <code>Это моноширинный текст.</code>
    <pre>Это блок кода.</pre>
    """
    bot.send_message(message.chat.id, html_content, parse_mode='HTML')


bot.infinity_polling(timeout=10, long_polling_timeout = 5)