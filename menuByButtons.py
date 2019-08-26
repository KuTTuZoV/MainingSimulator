import telebot
from telebot import types
import DB_init
import player
from PyQt5.QtCore import pyqtSignal, QObject, QTimer


telebot.apihelper.proxy = {'https' : 'socks5://166.62.123.35:32612'}
bot = telebot.TeleBot('840761243:AAEvNP1aV2NHTQfXKEcflph-NTG7xmkKgB4')

def paydaySlot(id, cash):
    bot.send_message(id, text="Ваши деньги: " + str(cash))

dbAdapter = DB_init.dbAdapter()

players = dbAdapter.startDB()

for tempPlayer in players:
    players[tempPlayer].paydaySignal.connect(paydaySlot)

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

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):

    componentData = call.data.split(':')

    if componentData[0] == "Материнская плата":
        motherboard = players[call.from_user.id].menu.structure["Магазин"]["Материнская плата"][call.data.split(':')[1]]['Слоты']

        addCompResult = players[call.from_user.id].computer.setMotherBoard(motherboard)

        a = 5
    else:
        addCompResult = players[call.from_user.id].computer.addComponent(call.data.split(':')[0], call.data.split(':')[1], int(call.data.split(':')[2]))

    if addCompResult == True:
        bot.send_message(call.from_user.id, text="Компонент добавлен!")
        dbAdapter.addCompomentDB(call.from_user.id, call.data.split(':')[0], call.data.split(':')[1], players[call.from_user.id].menu.structure["Магазин"][call.data.split(':')[0]][call.data.split(':')[1]].get("Цена")
                                 , players[call.from_user.id].menu.structure["Магазин"][call.data.split(':')[0]][call.data.split(':')[1]].get("Производительность"))
    else:
        bot.send_message(call.from_user.id, text="Что-то пошло не так!")
    pass

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

        players[message.from_user.id] = player.player(id)

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
            keyboard.add(types.InlineKeyboardButton(text="Купить", callback_data=message.text + ":" + item + ":" + str(items[item]["Производительность"])))
            bot.send_message(message.from_user.id, text=specification, reply_markup=keyboard)
        return

    if message.text == "<-Назад":
        players[message.from_user.id].menu.backToParent()
    else:
        players[message.from_user.id].menu.selectMenuItem(message.text)

    if message.text == "Мой компьютер":
        text=dbAdapter.showPC(message.from_user.id)
        testtext=players[message.from_user.id].computer.toString()
        bot.send_message(message.from_user.id, text=text)

    menuItems = players[message.from_user.id].menu.showCurrentLayer()

    keyboard = types.ReplyKeyboardMarkup()

    for item in menuItems:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(message.from_user.id, text="------", reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling(none_stop=True)