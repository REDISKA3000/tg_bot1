import os
import telebot
import time
import config
from SQLighter import SQLighter
import utils
import random
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

bot = telebot.TeleBot(config.token)


commands = ['/start','/test','/game','/stata']
k = True
@bot.message_handler(func=lambda message:not(message.text in commands),content_types=['text'])
def f(message):
    global k
    if k:
        bot.send_message(message.chat.id,'If you you want to start use command /start')
        k = False
    else:
        check_answer(message)


def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        # Уберем клавиатуру с вариантами ответа.
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
            c=0
            b=1
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!',
                             reply_markup=keyboard_hider)
            c=1
            b=0
        db = SQLighter(config.database_name)
        db.update(user_id, c, b)
        db.close()
        bot.send_message(message.chat.id,'If you want to look at your statistics use command /stata')
        # Удаляем юзера из хранилища (игра закончена)
        # utils.finish_user_game(message.chat.id)


@bot.message_handler(commands=['stata'])
def stat(message):
    import matplotlib.pyplot as plt
    db1=SQLighter(config.database_name)
    l = list(db1.select_all('stata')[0][:])
    x = list(map(lambda x: int(x/sum(l)*100),l))
    print(x)
    y=['Correct','Incorrect']
    plt.bar(y,x)
    plt.savefig('statistics.png')
    img = open('statistics.PNG', 'rb')
    bot.send_photo(message.chat.id,photo=img)






@bot.message_handler(commands=['start'])
def start(message):
    global user_id
    db = SQLighter(config.database_name)
    user_id = message.from_user.id
    db.create(user_id)
    db.close()
    bot.send_message(message.chat.id,'If you want to test this bot use command /test')
    bot.send_message(message.chat.id, 'If you want to play a game use command /game')


@bot.message_handler(commands=['test'])
def f(message):
    for file in os.listdir('music/'):
        if file.split(sep='.')[-1] == 'ogg':
            p = open('music/' + file, 'rb')
            msg = bot.send_voice(message.chat.id, p, None)
            bot.send_message(message.chat.id, msg.voice.file_unique_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


@bot.message_handler(commands=['game'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    rownum = int(random.randint(1, utils.get_rows_count()))
    row = db_worker.select_single(rownum).split(sep=',')
    send_voice(message,rownum)
    # Формируем разметку
    markup = telebot.types.ReplyKeyboardMarkup()
    # Отправляем аудиофайл с вариантами ответа
    bot.send_message(message.chat.id, "ty hryak!",reply_markup = utils.generate_markup(row[0], row[1],row[2],row[3]))
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[0])
    # Отсоединяемся от БД
    db_worker.close()

def send_voice(message,rownum):
    l = os.listdir('music/')
    p = open('music/' + l[rownum-1], 'rb')
    msg = bot.send_voice(message.chat.id, p, None)
    return bot.send_message(message.chat.id, msg.voice.file_unique_id, reply_to_message_id=msg.message_id)



if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.infinity_polling()
