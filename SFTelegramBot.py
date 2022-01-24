import telebot
from config import exchanges, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Приветствую, Уважаемый Пользователь!\n -------------------------------\n \
    Чтобы начать работу введите команду через пробел в следующем формате:\n \
    <конвертируемая валюта>\n \
    <в какую валюту перерводить>\n \
    <количество переводимой валюты>\n -------------------------------\n \
    Список доступных валют по команде: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступны следующие валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, 'Неверное количество параметров!')

    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")


bot.polling()
