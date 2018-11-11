import config
import telebot
import logging
from sql import check_user, add_to_db, get_user_link, update_link_db
from test import main, get_day, get_next_day, get_info_for_mes

bot = telebot.TeleBot(config.token)

logging.basicConfig(filename="sample.log", level=logging.INFO)


@bot.message_handler(commands=['start'])
def start(message):
    us = message.from_user.first_name
    us_id = message.from_user.id
    print(us_id)
    bot.reply_to(message, 'Hello, ' + us + str(us_id))

    if check_user(message.from_user.id):
        bot.send_message(message.chat.id, 'Вы уже зарегестрированы.')
        start_menu(message)
    else:
        msg = bot.send_message(message.chat.id, 'Введи ссылку расписания своей группы')
        bot.send_message(message.chat.id, 'Пример: https://kbp.by/rasp/timetable/view_beta_tbp/?cat=group&id=24')
        print(msg.text)
        bot.register_next_step_handler(msg, registration)


def registration(msg):
    print(msg.text)
    us_id = msg.from_user.id
    print(us_id)

    if link_check(msg.text):
        add_to_db(us_id, msg.text)
        #bot.send_message(msg.chat.id, 'Вы зарегестрировали !')
        start_menu(msg)
    else:
        bot.send_message(msg.chat.id, 'Ошибка, неверная ссылка')
        start(msg)


def update_link(msg):
    us_id = msg.from_user.id
    if link_check(msg):
        update_link_db(us_id, msg.text)
        #bot.send_message(msg.chat.id, 'Вы зарегестрировали !')
        start_menu(msg)
    else:
        bot.send_message(msg.chat.id, 'Ошибка, неверная ссылка')
        start(msg)


def link_check(msg):
    print(msg)
    link = msg
    if len(link) > 0:
        try:
            temp = link[-2:]

            if temp[0] == '=':
                temp = temp[1]

            if int(temp) <= 65:
                return True
            else:
                return False
        except Exception as err:
            pass


    else:
        return False


@bot.message_handler(func=lambda mess: 'Расписание занятий' == mess.text, content_types=['text'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Получить расписание на сегодня')
    user_markup.row('Получить расписание на завтра')
    user_markup.row('Время пар')
    user_markup.row('Назад')
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)


@bot.message_handler(commands=['menu'])
def start_menu(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    #user_markup.row('Расписание транспорта')
    user_markup.row('Расписание занятий')
    user_markup.row('Обновления', 'Обратная связь')
    user_markup.row('Изменить ссылку раписания группы')
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=user_markup)

@bot.message_handler(func=lambda mess: 'Изменить ссылку раписания группы' == mess.text, content_types=['text'])
def change_link(message):
    msg = bot.send_message(message.chat.id, 'Введи ссылку расписания своей группы')
    bot.send_message(message.chat.id, 'Пример: https://kbp.by/rasp/timetable/view_beta_tbp/?cat=group&id=24')
    print(msg.text)
    bot.register_next_step_handler(msg, update_link)


@bot.message_handler(func=lambda mess: 'Назад' == mess.text, content_types=['text'])
def go_main_menu(message):
    start_menu(message)


@bot.message_handler(func=lambda mess: 'Обновления' == mess.text, content_types=['text'])
def info_updates(message):
    message_updates = """ ИНФОРМАЦИЯ ОБ 
ПОСЛЕДНЕМ ОБНОВЛЕНИИ
                
Было добавлено расписание звонков
                v.0.9.4"""
    bot.send_message(message.chat.id, message_updates)


@bot.message_handler(func=lambda mess: 'Обратная связь' == mess.text, content_types=['text'])
def info_connection(message):
    message_updates = """По поводу предложений и ошибок, писать на электронную почту 'lxborodin@gmail.com'"""
    bot.send_message(message.chat.id, message_updates)


@bot.message_handler(func=lambda mess: 'Время пар' == mess.text, content_types=['text'])
def lessons_time(message):

    message_time = """   РАСПИСАНИЕ ЗВОНКОВ
                (ПН-ПТН)
        Пара 1: 8:30-10:00
        Пара 2: 10:10-11:40
        Пара 3: 12:10-13:40
        Пара 4: 14:00-15:30
        Пара 5: 15:40-17:10
        Пара 6: 17:20-18:50
        Пара 7: 19:00-20:30"""
    bot.send_message(message.chat.id, message_time)


@bot.message_handler(func=lambda mess: 'Получить расписание на сегодня' == mess.text, content_types=['text'])
def today(message):
    link = get_user_link(message.from_user.id)
    data = main(0, link)
    message_0 = 'Привет Буба, сегодня {}\n у тебя следующие пары:'.format(get_day())
    message_1 = get_information_for_schedule(data)
    print('len{}'.format(len(message_1)))
    i = 0
    mess = ''
    while i <= len(message_1) - 1:
        mess += message_1[i]
        i += 1

    bot.send_message(message.chat.id, message_0)
    bot.send_message(message.chat.id, mess)


@bot.message_handler(func=lambda mess: 'Получить расписание на завтра' == mess.text, content_types=['text'])
def tomorrow(message):
    message_0 = 'Привет Буба, завтра {}\n у тебя следующие пары:'.format(get_next_day())
    link = get_user_link(message.from_user.id)
    data = main(1, link)
    message_1 = get_information_for_schedule(data)
    print('len{}'.format(len(message_1)))
    i = 0
    mess = ''
    while i <= len(message_1) - 1:
        mess += message_1[i]
        i += 1
    bot.send_message(message.chat.id, message_0)
    bot.send_message(message.chat.id, mess)


def get_information_for_schedule(data):
    j = 0
    lst = []
    for i in data:
        j += 1
        message = get_info_for_mes(j, i)
        lst.append(message)
    return lst


@bot.message_handler(content_types=['text'])
def check_answer(message):
    bot.send_message(message.chat.id, 'Я тебя не понимаю(')
    bot.send_message(message.chat.id, '/start - запуск ')





if __name__ == '__main__':
    bot.polling(none_stop=True)




