import telebot
from telebot import types
import menu
import psycopg2
import DB_init

telebot.apihelper.proxy = {'https' : 'socks5://192.169.216.124:31864'}
bot = telebot.TeleBot('840761243:AAEvNP1aV2NHTQfXKEcflph-NTG7xmkKgB4')

menu = menu.menu()

dbAdapter = DB_init.dbAdapter()

#dbAdapter.db_init()
#dbAdapter.createTestData()
#dbAdapter.getUsers()

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

    initUser(message.from_user.id)

    if message.text in menu.assortment():

        items = menu.structure["Магазин"][message.text]
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

    if message.text == "/start":
        keyboard = types.ReplyKeyboardMarkup()
        menuItems = menu.showCurrentLayer()

        for item in menuItems:
            keyboard.add(types.KeyboardButton(text=item))

        bot.send_message(message.from_user.id, text="------", reply_markup=keyboard)
        return

    if message.text == "<-Назад":
        menu.backToParent()
    else:
        menu.selectMenuItem(message.text)

    menuItems = menu.showCurrentLayer()

    keyboard = types.ReplyKeyboardMarkup()

    for item in menuItems:
        keyboard.add(types.KeyboardButton(text=item))

    bot.send_message(message.from_user.id, text="------", reply_markup=keyboard)

    # if message.text == "Магазин":
    #     keyboard = types.ReplyKeyboardMarkup()
    #     proc = types.KeyboardButton(text="Процессор")#, callback_data="proc")
    #     videocard = types.KeyboardButton(text="Видеокарта")#, callback_data="card")
    #     hd = types.KeyboardButton(text="Жесткий диск")#, callback_data="hd")
    #     memory = types.KeyboardButton(text="Память")#, callback_data="memory")
    #     motherboard = types.KeyboardButton(text="Материнка")#, callback_data="mb")
    #     backbutton = types.KeyboardButton(text="back")#, callback_data="mainmenu")
    #     keyboard.add(proc, videocard, hd, memory, motherboard, backbutton)
    #     bot.send_message(message.from_user.id, text="Вы попали в магаизн",reply_markup=keyboard)
    #     return


    # keyboardmain = types.ReplyKeyboardMarkup(row_width=3)
    # shop_button = types.KeyboardButton(text="Магазин")#, callback_data="shop")
    # bank_button = types.KeyboardButton(text="Мой счет")#, callback_data="mybank")
    # pc_button = types.KeyboardButton(text="Мой компьютер")#, callback_data="mypc")
    # keyboardmain.add(shop_button, bank_button, pc_button)
    # bot.send_message(message.chat.id, "Чего желаете?", reply_markup=keyboardmain)

# @bot.callback_query_handler(func=lambda call:True)
# def callback_inline(call):
#     if call.data == "mainmenu":
#
#         keyboardmain = types.ReplyKeyboardMarkup(row_width=3)
#         shop_button = types.KeyboardButton(text="Магазин")#, callback_data="shop")
#         bank_button = types.KeyboardButton(text="Мой счет")#, callback_data="mybank")
#         pc_button = types.KeyboardButton(text="Мой компьютер")#, callback_data="mypc")
#         keyboardmain.add(shop_button, bank_button, pc_button)
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чего желаете?", reply_markup=keyboardmain)
#
#     if call.data == "shop":
#         keyboard = types.ReplyKeyboardMarkup()
#         proc = types.KeyboardButton(text="Процессор")#, callback_data="proc")
#         videocard = types.KeyboardButton(text="Видеокарта")#, callback_data="card")
#         hd = types.KeyboardButton(text="Жесткий диск")#, callback_data="hd")
#         memory = types.KeyboardButton(text="Память")#, callback_data="memory")
#         motherboard = types.KeyboardButton(text="Материнка")#, callback_data="mb")
#         backbutton = types.KeyboardButton(text="back")#, callback_data="mainmenu")
#         keyboard.add(proc, videocard, hd, memory, motherboard, backbutton)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)
#
#     elif call.data == "mybank":
#         keyboard = types.ReplyKeyboardMarkup()
#         backbutton = types.KeyboardButton(text="back")#, callback_data="mainmenu")
#         keyboard.add(backbutton)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)
#
#     elif call.data == "1" or call.data == "2" or call.data == "3":
#         bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="alert")
#         keyboard3 = types.ReplyKeyboardMarkup()
#         button = types.KeyboardButton(text="lastlayer")#, callback_data="ll")
#         keyboard3.add(button)
#         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="last layer",reply_markup=keyboard3)


if __name__ == "__main__":
    bot.polling(none_stop=True)