import telebot
from telebot import types
import DB_init
import player
import threading
import computer
import json
from PyQt5.QtCore import pyqtSignal, QObject, QTimer

def paydaySlot():

    try:
        for temp in players:
            cash = players[temp].calculateCash()
            dbAdapter.addCashDB(cash, players[temp].id)
            bot.send_message(players[temp].id, text= "Ваши деньги: " + str(cash))
    except:
        pass

    timer = threading.Timer(500, paydaySlot)
    timer.start()

proxyList = open("proxy.txt", "r").read().split('\n')

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

proxyFile = open("proxy.txt", "w")
for proxy in proxyList:
    proxyFile.write(proxy + "\n")


dbAdapter = DB_init.dbAdapter()

players = dbAdapter.startDB()
timer = threading.Timer(5, paydaySlot)
timer.start()
assortment = json.loads(open("assortment", encoding="utf-8-sig").read())

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
    addCompResult = False

    if componentData[0] == "Материнская плата":

        component = assortment["Материнская плата"][call.data.split(':')[1]]

        price = component["Цена"]
        perf  = component["Производительность"]

        if players[call.from_user.id].cash >= price:

            motherboard = component['Слоты']
            compability = component['Совместимость']

            addMBResult, msg = players[call.from_user.id].computer.setMotherBoard(motherboard, compability)

            if addMBResult == True:
                players[call.from_user.id].cash = players[call.from_user.id].cash - \
                                                 assortment[
                                                      call.data.split(':')[0]][call.data.split(':')[1]].get("Цена");

            dbAdapter.addMotherboard(call.from_user.id, 1, "Материнская плата", call.data.split(':')[1], price, perf, 1)

        else:
            bot.send_message(call.from_user.id, text="Недостаточно денег!")

        a = 5

    elif componentData[0] == "sell":
        players[call.from_user.id].computer.removeComponent(componentData[1], componentData[2])
        dbAdapter.sellInDB(call.from_user.id, componentData[2])
        players[call.from_user.id].cash += int(componentData[3])


    elif componentData[0] == "Eject":
        players[call.from_user.id].computer.deactivateComponent(componentData[1], componentData[2])
        dbAdapter.deactivateInDB(call.from_user.id, componentData[2])

    elif componentData[0] == "Inject":
        flag = players[call.from_user.id].computer.activateComponent(componentData[1], componentData[2])
        if flag == True:
            dbAdapter.activateInDB(call.from_user.id, componentData[2])


    else:
        component = assortment[call.data.split(':')[0]][call.data.split(':')[1]]

        price = component["Цена"]
        perf  = component["Производительность"]
        level = component["Уровень"]

        if players[call.from_user.id].cash >= price:
            addCompResult, msg = players[call.from_user.id].computer.addComponent(call.data.split(':')[0], call.data.split(':')[1], price,
                                                                                 perf, 1, level)

            if addCompResult == True:
                players[call.from_user.id].cash = players[call.from_user.id].cash - \
                                                     assortment[
                                                          call.data.split(':')[0]][call.data.split(':')[1]].get("Цена");
        else:
            bot.send_message(call.from_user.id, text="Недостаточно денег!")


    if addCompResult == True:
        bot.send_message(call.from_user.id, text="Компонент добавлен!")

        component = assortment[call.data.split(':')[0]][call.data.split(':')[1]]

        price = component["Цена"]
        perf = component["Производительность"]
        level = component["Уровень"]

        dbAdapter.addCashDB(players[call.from_user.id].cash, players[call.from_user.id].id)
        dbAdapter.addCompomentDB(call.from_user.id, call.data.split(':')[0], call.data.split(':')[1],price, perf, 1, level, 1)

    elif componentData[0] == "sell" or componentData[0] == "Eject":
        bot.send_message(call.from_user.id, text="Вы провели продажу или извлечение!")

    elif componentData[0] == "Inject":
        if flag == True:
            bot.send_message(call.from_user.id, text="Вы провели вставку!")
        else:
            bot.send_message(call.from_user.id, text="{} итак активен!".format(componentData[1]))

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

        players[message.from_user.id] = player.player(message.from_user.id, 1500)
        players[message.from_user.id].computer = computer.computer()

        if message.from_user.id not in dbAdapter.getUsers():
            dbAdapter.addUser(message.from_user.id, "{} {}".format(message.from_user.first_name, message.from_user.last_name))
            dbAdapter.addCashDB(players[message.from_user.id].cash, players[message.from_user.id].id)
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
        #text=dbAdapter.showPC(message.from_user.id)
        testtext=players[message.from_user.id].computer.toString()
        try:
            motherboard = dbAdapter.iNeedMB(message.from_user.id)
        except:
            pass
        for line in testtext.split('\n'):
            items = line.split(":")

            try:
                itemDescription = "Тип: {}, Модель: {}, Цена: {}, Производительность: {}, Активность: {}".format(items[0], items[1], items[2], items[3], items[4])
                #bot.send_message(message.from_user.id, text=itemDescription)
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                button = types.InlineKeyboardButton(text = "Продать", callback_data = "sell:" + line)
                button1 = types.InlineKeyboardButton(text="Извлечь", callback_data = "Eject:" + line)
                button2 = types.InlineKeyboardButton(text="Вставить", callback_data="Inject:" + line)
                #keyboard.row(types.InlineKeyboardButton(text="Продать", callback_data = "sell:" + line))
               # keyboard.row(types.InlineKeyboardButton(text="Извлечь", callback_data = "Eject:" + line))
                keyboard.add(button, button1, button2)
                bot.send_message(message.from_user.id, text=itemDescription, reply_markup=keyboard)
            except:
                if testtext.split('\n')[0] == "":
                    bot.send_message(message.from_user.id, text="У вас нет материнки!")
                elif line == "":
                    bot.send_message(message.from_user.id, text="Это слоты вашей материнки: {}!".format(motherboard))
                else:
                    itemDescription = "Тип: {}, Свободен".format(items[0])
                    bot.send_message(message.from_user.id, text=itemDescription)

    if message.text == "Мой счет":
        bot.send_message(message.from_user.id, text=players[message.from_user.id].cash)
        dbAdapter.addCashDB(players[message.from_user.id].cash, players[message.from_user.id].id)

    menuItems = players[message.from_user.id].menu.showCurrentLayer()

    keyboard = types.ReplyKeyboardMarkup()

    for item in menuItems:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(message.from_user.id, text="------", reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling(none_stop=True)

