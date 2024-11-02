import telebot
from telebot import types
import datetime

token = input('Token: ')
bot = telebot.TeleBot(f'{token}')
print('Bot started')
age = 0
# @bot.message_handler(commands=['start'])
# def startBot(message):
#     first_mess = f"<b>{message.from_user.first_name}, добро пожаловать в калькулятор калорий по фотографии!\nУкажите Ваш возраст, чтобы мы могли давать рекомендации?"
#     markup = types.InlineKeyboardMarkup()
#     button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
#     markup.add(button_yes)
#     bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, f"{message.from_user.first_name}, добро пожаловать в калькулятор калорий по фотографии\nУкажите Ваш возраст, чтобы мы могли давать рекомендации?");
        bot.register_next_step_handler(message, get_age) #следующий шаг – функция get_age
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_age(message):
    print(message.text)
    global age
    print(f'Start func get_age: {age}')
    while age == 0: #проверяем что возраст изменился
        try:
            age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
            bot.register_next_step_handler(message, get_age)
            return
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе '+str(age)+' лет, все верно?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global age
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню : )\n Пришлите фото Вашей еды.')
        bot.register_next_step_handler(call.message, get_food)
    elif call.data == "no":
        age = 0
        bot.send_message(call.message.chat.id,f"{call.from_user.first_name}, укажите Ваш возраст.")
        bot.register_next_step_handler(call.message, get_age)
        print('callback:', call.message.text)

@bot.message_handler(content_types=['photo'])
def get_food(message):
     fileID = message.photo[-1].file_id
     file_info = bot.get_file(fileID)
     downloaded_file = bot.download_file(file_info.file_path)
     time_now = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
     print(time_now)
     folder_id = message.from_user.id
     with open("images/foods/"+time_now+".jpg", 'wb', encoding='utf-8') as new_file:
         new_file.write(downloaded_file)



bot.polling(none_stop=True, interval=0)