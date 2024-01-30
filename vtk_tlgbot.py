import asyncio, requests

import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types

from telegram_bot_calendar import LSTEP_tr

from PIL import Image
from io import BytesIO

from conf.const import *
from conf.tlg_invite import *
from config.settings import settings



bot = AsyncTeleBot(settings["vtk_tlg_token"], parse_mode=None)


@bot.message_handler(content_types=['new_chat_members'])
async def welcome_new_member(message):
    if message.json['new_chat_participant']['id'] == 1603029657:
        await bot.send_message(-674296167, f'Меня добавили в группу "{message.chat.title}" (ID: {message.chat.id})')
        

@bot.message_handler(content_types=['photo'])
async def handle_photo(message):
    if message.chat.type != "private":
        return
    
    photo_size = message.photo[-1]
    file_info = await bot.get_file(photo_size.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    avatar = Image.open(BytesIO(downloaded_file))
    under = Image.open("assets/logo_cs.png")

    width, height = avatar.size   # Get dimensions
    new_width = min(width, height)
    new_height = new_width
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    # Crop the center of the image
    avatar = avatar.crop((left, top, right, bottom))
    under = under.resize(avatar.size)

    avatar.paste(under, (0, 0), under)

    await bot.send_photo(message.chat.id, avatar)


# Handler for .json statistics
@bot.message_handler(content_types=['document'])
async def handle_document(message):
    if message.chat.type != "private":
        return

    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        await bot.send_message(message.chat.id, f'Начата обработка файла "{message.document.file_name}".')

        filename = f"{message.document.file_unique_id}"
        with open("./statistic/"+filename+".json", "wb") as f:
            f.write(downloaded_file)

        text = message.caption.split(" ")
  
        try:
            login = text[0]
            password = text[1]

            if not login: login = "-"
            if not password: password = "-"
        except Exception as e:
            login = "-"
            password = "-"
   
        try:
            theme = text[2]

            if not theme: theme = "dark"
        except Exception as e:
            theme = "dark"

        s = requests.Session()
        payload = {
            "login": login,
            "password": password,
            "filename": filename,
            "theme": theme
        }
        response = s.post("http://localhost:8081/api/handle_game_statistic", params=payload)

        if response.status_code == 200:
            await bot.send_message(message.chat.id, response.text)
        elif response.status_code == 400:
            await bot.send_message(message.chat.id, f'Не удалось обработать статистику. {response.text} ¯\_(ツ)_/¯')
        else:
            await bot.send_message(message.chat.id, 'Не удалось обработать статистику. Попробуйте еще раз ¯\_(ツ)_/¯')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start'])
async def command_start(message):
    if message.chat.type == "private":
        send_mess = f"Привет, отправь команду /invite для создания пригласительных ко дню рождения :)"
        await bot.send_message(message.chat.id, send_mess)
  
@bot.message_handler(commands=['invite'])
async def command_invite(message):
    if message.chat.type == "private":
          markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton("Ангарск")
          btn2 = types.KeyboardButton("Братск")
          markup.add(btn1, btn2)
          await bot.send_message(message.chat.id, text="Здравствуйте, для начала выберите свой город", reply_markup=markup)
          
          
@bot.message_handler(commands=['client'])
async def command_client(message):
    if not message.chat.type == "private":
        return
    # Проверка на аккаунт менеджера по ID
    if not message.from_user.id in VTK_MANAGERS_IDS:
        return
    
    await bot.send_message(message.chat.id, text="Информация о клиенте (поиск, добавить, изменить, удалить <- \"reaction button\" кнопки)")
    

@bot.message_handler(commands=['order'])
async def command_order(message):
    if not message.chat.type == "private":
        return
    # Проверка на аккаунт менеджера по ID
    if not message.from_user.id in VTK_MANAGERS_IDS:
        return
    
    await bot.send_message(message.chat.id, text="Создание новой заявки")
    

@bot.message_handler(commands=['calendar'])
async def command_calendar(message):
    if not message.chat.type == "private":
        return
    # Проверка на аккаунт менеджера по ID
    if not message.from_user.id in VTK_MANAGERS_IDS:
        return
    
    await bot.send_message(message.chat.id, text="Просмотр заявок в виде календаря")


@bot.callback_query_handler(func=MyTranslationCalendar.func())
async def cal(c):
    result, key, step = MyTranslationCalendar().process(c.data)
    if not result and key:
        await bot.edit_message_text(f"Выберите {LSTEP_tr[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        return await makeinvite_3_date(bot, c.message, result)
        
        

@bot.message_handler(content_types=['text'])
async def func(message):
    if message.chat.type != "private":
        return
    
    status = False
    
    if message.text.lower() == "invite":
        return await command_invite(message)
    
    if message.text == "Ангарск":
        return await makeinvite_1_city(bot, message, "Ангарск", 'vtk')
    elif message.text == "Братск":
        return await makeinvite_1_city(bot, message, "Братск", 'br')
    else:
        status = get_invuser_status(message.chat.id)
        print(f"Status: {status}")
        
    if status and status != "complete":
        if status == "imeninnik_name":
            return await makeinvite_2_imeninnikname(bot, message)
        if status == "date":
            calendar, step = MyTranslationCalendar().build()
            bot.send_message(message.chat.id,
                            f"Выберите {LSTEP_tr[step]}",
                            reply_markup=calendar)
        if status == "minutes":
            return await makeinvite_3_minutes(bot, message)
        if status == "name":
            return await makeinvite_4_image(bot, message)
        

asyncio.run(bot.polling(timeout=300, request_timeout=300, none_stop=True))
