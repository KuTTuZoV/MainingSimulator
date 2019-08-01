import telebot
from telebot import types

telebot.apihelper.proxy = {'https' : 'socks5://163.172.81.30:443'}
bot = telebot.TeleBot('840761243:AAEvNP1aV2NHTQfXKEcflph-NTG7xmkKgB4')

emojies = {
    "Процессор" : "⚙",
    "Жесткий диск" : "📀",
    "Видеокарта" : "📺",
    "Память" : "📄",
    "Материнская плата" : "⚙",
}

assortment   = ("Процессор", "Жесткий диск", "Видеокарта", "Память", "Материнская плата")
currentLayer = ("Магазин", "Мой компьютер", "Мой счет")


def showCategories(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)

    for category in assortment:
        keyboard.row(types.KeyboardButton(category + " " + emojies[category]))
    bot.send_message(message.from_user.id, text="Магазин", reply_markup=keyboard)

def showMenu(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)

    for item in currentLayer:
        keyboard.row(types.KeyboardButton(item + emojies["Процессор"]))

    bot.send_message(message.from_user.id, text="Меню", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    showMenu(message)

    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")


bot.polling(none_stop=True, interval=0)


