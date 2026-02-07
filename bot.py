import telebot
from config import TOKEN, currencies
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Введите запрос в формате:\n"
        "<валюта> <в какую валюту> <количество>\n"
        "Пример: доллар рубль 100\n\n"
        "/values — список валют"
    )


@bot.message_handler(commands=["values"])
def values(message):
    text = "Доступные валюты:\n"
    for val in currencies:
        text += f"- {val}\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def convert(message):
    try:
        base, quote, amount = message.text.lower().split()
        price = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка ввода")
    else:
        bot.send_message(
            message.chat.id,
            f"{amount} {base} = {round(price, 2)} {quote}"
        )


bot.polling()
