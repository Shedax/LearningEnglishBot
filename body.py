import telebot
from telebot import types
from database import *
import random

bot = telebot.TeleBot('976475763:AAHQ590SacIfLuQxrse7F4Dk0wEzr9wxcVQ')
global list1
global urword
global score
global maxscore
maxscore = 0
score = 0

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '✌Привет, <b> {0.first_name}</b>! Я бот-тренажер для улучшения'
                                      ' владения английским языком🇬🇧!'.format(message.from_user), parse_mode='html')
    bot.send_message(message.chat.id, 'Для начала нажми на /help чтобы побольше обо мне узнать!😉')

@bot.message_handler(commands=['help'])
def help_message(message):
    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row('Дальше')
    bot.send_message(message.chat.id, 'Как я уже говорил, я бот-тренажер🤖! Это значит, что со мной ты сможешь практиковаться'
                                      ' и получать новые знания📚📖. Единственное, что нужно знать перед началом это алфавит!')
    bot.send_message (message.chat.id, 'Тут ты сможешь выучить новые слова и идиомы, без знания которых не обойтись.'
                                      'Также ты сможешь попрактиковаться в их знании в миниигре!')
    to_menu=bot.send_message(message.chat.id, 'Что же такое идиомы? В английском языке часто встречаются выражения, которые при переводе'
                                      ' не имеют никакого смысла. Эти выражения называются идиомами и англичане'
                                      ' довольно часто их употребляют. Запомнив наиболее распространенные из них, ты'
                                      ' сможешь сделать свою речь ярче и живее.', reply_markup=kb1)
    bot.register_next_step_handler(to_menu, learni)

def menu_0(message):
    img = open('img.png', 'rb')
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='📚Учиться', callback_data='learni')
    kb.add(btn)
    bot.send_message(message.chat.id, 'Итак, начнём учиться?🤔', reply_markup=kb)

@bot.message_handler(commands=['menu'])
def menu(message):
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='📚Учиться', callback_data='learn')
    btn1 = types.InlineKeyboardButton(text='🎮Играть', callback_data='game')
    btn2 = types.InlineKeyboardButton(text='📖Открыть словарь', callback_data='vocabulary')
    kb.add(btn)
    kb.add(btn1)
    kb.add(btn2)
    bot.send_message(message.chat.id, 'Итак, чем будем заниматься?🤔', reply_markup=kb)

@bot.message_handler(commands=['vocabulary'])
def vocabulary(message):
    wlist=[]
    ilist=[]
    wtext='-\n-\n-\n-\nЗдесь пока пусто.😔 \nЗаходи, когда выучишь новые слова!\n-\n-\n-\n-'
    itext='-\n-\n-\n-\nЗдесь пока пусто.😔 \nЗаходи, когда выучишь новые идиомы!\n-\n-\n-\n-'
    count=0
    count2=0
    db_worker = SQLighter("wordsdb.db")
    rows = db_worker.get_vocabulary('words')
    rows2 = db_worker.get_vocabulary('idioms')
    db_worker.close()
    if len(rows) != 0:
        count = len(rows)
        wtext = ''
        for i in range(len(rows)):
            wlist.append(rows[i][1] + ' - ' + rows[i][2])
            wtext += str(wlist[i]) + '\n'
    if len(rows2)!=0:
        count2 = len(rows2)
        itext = ''
        for j in range(len(rows2)):
            ilist.append(rows2[j][1] + ' - ' + rows2[j][2])
            itext += str(ilist[j]) + '\n'
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    kb.add(btn)
    bot.send_message(message.chat.id, '📎Количество выученных слов: ' + str(count) + '\n<b>Список:</b>' + '\n' + wtext, parse_mode='html')
    bot.send_message(message.chat.id, '📎Количество выученных идиом: ' + str(count2) + '\n<b>Список:</b>' + '\n' + itext, parse_mode='html', reply_markup=kb)


def learni(message):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Учить', callback_data='idioms')
    kb.add(btn1)
    img = open('img.png', 'rb')
    bot.send_photo(message.chat.id, img, caption='Привет!\nМы братья Бодкины и мы поможем тебе увеличить твой словарный запас! \nМы предлагаем тебе начать с изучения идиом, а потом перейти к изучению новых слов.', reply_markup=kb)

@bot.message_handler(commands=['learn'])
def learn(message):
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Слова', callback_data='words')
    btn1 = types.InlineKeyboardButton(text='Идиомы', callback_data='idioms')
    kb.add(btn, btn1)
    bot.send_message(message.chat.id, 'Чтобы ты хотел выучить?🤓', reply_markup=kb)

def learn1(message):
    kb1 = types.ReplyKeyboardMarkup(True, True)
    kb1.row('Одежда', 'Животные')
    kb1.row('Техника', 'Еда и напитки')
    return bot.send_message(message.chat.id, 'Выбери тему из списка.👇', reply_markup=kb1)

def learn2(message):
    db_worker = SQLighter("wordsdb.db")
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Дальше', callback_data='idioms')
    btn2 = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    markup.add(btn)
    markup.add(btn2)
    list2 = db_worker.select_all_v2('idioms')
    if len(list2) == 0:
        list2 = db_worker.select_all('idioms')
    random.shuffle(list2)
    idiom = list2[0][1].upper()
    bot.send_message(message.chat.id, '<b>' + idiom + '</b>' +
                     '\n📖' + '<i>' + list2[0][2] + '</i>', parse_mode='html', reply_markup=markup)
    db_worker.insertq(list2[0][0], 'idioms')
    db_worker.close()

@bot.message_handler(commands=['learnword'])
def learnword(message):
    global list1
    global msg
    db_worker = SQLighter("wordsdb.db")
    marks = ['Слово: ', 'Перевод: ']
    if len(list1)==0:
            list1 = db_worker.select_single_category(msg)
    text = list()
    random.shuffle(list1)
    for j in range(len(marks)):
        text.append(marks[j] + list1[0][j+1])
    c = "\n".join([str(x) for x in text])
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text='Дальше', callback_data='det')
    btn1 = types.InlineKeyboardButton(text='Сменить тему', callback_data='new')
    btn2 = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    markup.add(btn, btn1)
    markup.add(btn2)
    bot.send_photo(message.chat.id, list1[0][4], caption=c, reply_markup=markup)
    db_worker.insertq(list1[0][0], 'words')
    del list1[0]
    db_worker.close()

@bot.message_handler(commands=['game'])
def game(message):
    global urword
    global wordlist
    global trans
    db_worker = SQLighter("wordsdb.db")
    kb1 = telebot.types.ReplyKeyboardMarkup(True, False)
    voclist = db_worker.get_vocabulary('words')
    if len(voclist) < 4:
        bot.send_message(message.chat.id, 'Чтобы приступить, необходимо выучить как минимум 4 слова.')
    else:
        i = random.randint(0, len(voclist) - 1)
        word = voclist[i][1]
        trans = voclist[i][2]
        urword = word
        if urword == message.text:
            game(message)
        else:
            wordlist = list(db_worker.select_word_column())
            wordlist.remove(word)
            del wordlist[3:]
            wordlist.append(word)
            random.shuffle(wordlist)
            kb1.row(wordlist[0], wordlist[1])
            kb1.row(wordlist[2], wordlist[3])
            kb1.row('Меню')
            bot.send_photo(message.chat.id, voclist[i][4], caption=trans, reply_markup=kb1)
    db_worker.close()

@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    if call.data == "det":
        learnword(call.message)
    if call.data == "new" or call.data == "words":
        learn1(call.message)
    if call.data == "idioms":
        learn2(call.message)
    if call.data == "game":
        game(call.message)
    if call.data == "vocabulary":
        vocabulary(call.message)
    if call.data == "learn":
        learn(call.message)
    if call.data == "learni":
        learni(call.message)
    if call.data == "menu":
        menu(call.message)

def defs(message):
    if message.text == '/start':
        start_message(message)
    elif message.text == '/game':
        game(message)
    elif message.text == '/vocabulary':
        vocabulary(message)
    elif message.text == '/help':
        help_message(message)
    elif message.text == '/menu':
        menu(message)
    elif message.text == '/learn':
        learn(message)
    else:
        return False

@bot.message_handler(content_types=['text'])
def cate(message):
    dodef = defs(message)
    if dodef == False:
        global list1
        global msg
        global urword
        global score
        global maxscore
        if score > maxscore:
            maxscore = score
        db_worker = SQLighter("wordsdb.db")
        cat = db_worker.select_cat_column()
        try:
            if message.text in cat:
                msg = message.text
                list1 = db_worker.select_single_category(msg)
                if message.text == 'Одежда':
                    img = open('img4.png', 'rb')
                    bot.send_photo(message.chat.id, img, caption='Привет! Я Бен Бодкин и я вижу, что ты уже выучил идиомы и предлагаю тебе выучить слова, связанные'
                                                            ' с одеждой. Я обожаю одежду и научу тебя всему, что знаю!')
                elif message.text == 'Животные':
                    img = open('img3.png', 'rb')
                    bot.send_photo(message.chat.id, img, caption='Привет! Я Билл Бодкин и я вижу, что ты уже выучил идиомы и предлагаю тебе выучить слова связанные'
                                                                 ' с животными. Я обожаю животных и научу тебя всему, что знаю!')
                elif message.text == 'Техника':
                    img = open('img2.png', 'rb')
                    bot.send_photo(message.chat.id, img, caption='Привет! Я Боб Бодкин и я вижу, что ты уже выучил идиомы и предлагаю тебе выучить слова связанные'
                                                                 ' с техникой. Я люблю технику и научу тебя всему, что знаю!')
                else:
                    img = open('img1.png', 'rb')
                    bot.send_photo(message.chat.id, img, caption='Привет! Я Берти Бодкин и я вижу, что ты уже выучил идиомы и предлагаю тебе выучить слова связанные с едой. '
                                                                 'Я очень люблю вкусно поесть, а также готовить. Я расскажу тебе все о еде и напитках!')
                learnword(message)
            elif message.text in wordlist:
                if message.text==urword:
                    bot.send_message(message.chat.id, '👍Верно!')
                    score+=1
                else:
                    bot.send_message(message.chat.id, '❌Увы! Правильный ответ: ' + '<b>'+urword+'</b>'+'.', parse_mode='html')
                    score = 0
                game(message)
            elif message.text == 'Меню':
                rm = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, 'Угаданных слов подряд: ' + str(score) +
                                 '\n<b>Рекорд</b>: ' + str(maxscore), reply_markup=rm, parse_mode='html')
                menu(message)
            elif message.text == 'Меню':
                rm = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, 'Угаданных слов подряд: ' + str(score) +
                                 '\n<b>Рекорд</b>: ' + str(maxscore), reply_markup=rm, parse_mode='html')
                menu(message)
            else:
                bot.send_message(message.chat.id, '⚠️Извините, я не понимаю о чем вы.')
        except:
            bot.send_message(message.chat.id, '⚠️Извините, я не понимаю о чем вы.')
        db_worker.close()
if __name__ == '__main__':
    bot.polling(none_stop=True)