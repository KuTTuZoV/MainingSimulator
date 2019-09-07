import telebot
from telebot import types
import DB_init
import player
import requests
from xml.dom.minidom import parseString

proxyList = open("C:/proxy.txt", "r").read().split('\n')

for proxy in proxyList:
    telebot.apihelper.proxy = {'https' : 'socks5://{}'.format(proxy)}
    try:
        bot = telebot.TeleBot('840761243:AAEvNP1aV2NHTQfXKEcflph-NTG7xmkKgB4')
        print("Trying to connect proxy {}....".format(proxy), end="")
        bot.get_me()
        print("SUCCESS")
        break
    except:
        proxyList.pop(0)
        print("FAIL")

proxyFile = open("C:/proxy.txt", "w")
for proxy in proxyList:
    proxyFile.write(proxy + "\n")

dbAdapter = DB_init.dbAdapter()

players = dict()

def initUser(id):
    usersList = dbAdapter.getUsers()
    userNames = dbAdapter.getUserNames()

    if id in usersList:
        pass
    else:
        bot.send_message(id, text='Хотите зарегистрироваться? (y/n)')
        #print('Хотите зарегистрироваться? (y/n)')
        answer = input()
        if answer == 'y':
            print('Введите имя пользователя')
            userName = userNames[0]

            while userName in userNames:
                userName = input()
                if userName in userNames:
                    print('Уже занято, введите другое')

        dbAdapter.addUser(id, userName)


#menues[message.from_user.id] = menu.menu()

@bot.message_handler(content_types=["text"])
def any_msg(message):

    #initUser(message.from_user.id)

    if message.text == "/start":
        # keyboard = types.ReplyKeyboardMarkup()
        # menuItems = menu.showCurrentLayer()
        #
        # for item in menuItems:
        #     keyboard.add(types.KeyboardButton(text=item))
        #
        # bot.send_message(message.from_user.id, text="------", reply_markup=keyboard)

        players[message.from_user.id] = player.player()

        if message.from_user.id not in dbAdapter.getUsers():
            dbAdapter.addUser(message.from_user.id, "{} {}".format(message.from_user.first_name, message.from_user.last_name))
            bot.send_message(message.from_user.id, text="Пользователь зарегистрирован!")

        keyboard = types.ReplyKeyboardMarkup()
        keyboard.add(types.KeyboardButton(text="➡️"))
        bot.send_message(message.from_user.id, text="➡️", reply_markup=keyboard)

        return

    if message.text == "➡️":

        if len(players[message.from_user.id].hints) != 0:
            bot.send_message(message.from_user.id, text=players[message.from_user.id].hints[0])
            players[message.from_user.id].hints.pop(0)

            keyboard = types.ReplyKeyboardMarkup()
            keyboard.add(types.KeyboardButton(text="➡️"))
            bot.send_message(message.from_user.id, text="➡️", reply_markup=keyboard)
            return

    if message.text in players[message.from_user.id].menu.assortment():

        items = players[message.from_user.id].menu.structure["Магазин"][message.text]
        for item in items:
            keyboard = types.InlineKeyboardMarkup()

            specification = ""

            for spec in items[item]:
                specification += spec
                specification += ": "
                specification += str(items[item][spec])
                specification += "\n"

            bot.send_message(message.from_user.id, text=item)
            keyboard.add(types.InlineKeyboardButton(text="Купить", callback_data="buy"))
            bot.send_message(message.from_user.id, text=specification, reply_markup=keyboard)
        return

    if message.text == "<-Назад":
        players[message.from_user.id].menu.backToParent()
    else:
        players[message.from_user.id].menu.selectMenuItem(message.text)

    menuItems = players[message.from_user.id].menu.showCurrentLayer()

    keyboard = types.ReplyKeyboardMarkup()

    for item in menuItems:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(message.from_user.id, text="------", reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling(none_stop=True)