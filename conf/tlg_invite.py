from datetime import datetime

from telebot import types

from PIL import Image, ImageFont, ImageDraw

from .const import *
from .sql import *



async def makeinvite_1_city(bot, message, city: str, club: str='vtk'):
    add_invuser_city(f"{message.chat.first_name} {message.chat.last_name} @{message.chat.username}", message.chat.id, city, club)
    
    await bot.send_message(message.chat.id, "Напишите имя именинника в родительном падеже. Например: Максима", reply_markup=types.ReplyKeyboardRemove())
    

async def makeinvite_2_imeninnikname(bot, message):
    set_invuser_imeninnikname(message.chat.id, message.text)
    
    calendar, step = MyTranslationCalendar().build()
    
    await bot.send_message(message.chat.id, "Введите дату мероприятия.", reply_markup=calendar)
    
    
async def makeinvite_3_date(bot, message, result):
    date = datetime(result.year, result.month, result.day, 0, 0 , 0)
    set_invuser_date(message.chat.id, date)
    print(f"Дата: {result}, {type(result)}")
    await bot.send_message(message.chat.id, "Введите время начала в формате 15:00", reply_markup=types.ReplyKeyboardRemove())
    
    
async def makeinvite_3_minutes(bot, message):
    h = m = 0
    try:
        for delimeter in [":", ",", ".", " ", "-"]:
            if delimeter in message.text:
                h, m = message.text.split(delimeter, 1)
                h = abs(int(h))
                m = abs(int(m))
                break
        else:
            raise Exception('Не распознан формат времени')
        
        if h + m == 0:
            raise Exception('Время не может быть 00:00')
    except Exception as e:
        print(e)
        return await bot.send_message(message.chat.id, "Ошибка в формате времени. Введите время в формате 15:00", reply_markup=types.ReplyKeyboardRemove())


    date = datetime(2012, 1, 1, h, m , 0)
    set_invuser_minutes(message.chat.id, date)
    return await bot.send_message(message.chat.id, "Введите имя гостя в именительном падеже. Например: Александр", reply_markup=types.ReplyKeyboardRemove())


async def makeinvite_4_image(bot, message):
    name = message.text
    
    imeninnik_name, party_date, club = get_invuser_info(message.chat.id)

    inv_back = invite_backs.get(club, invite_backs["vtk"]).copy()
    draw = ImageDraw.Draw(inv_back)
    
    text = ("Дню рождения " + imeninnik_name).upper()
    size = 60
    font_imeninnik = ImageFont.truetype("conf/fonts/troubleside.ttf", size)
    while font_imeninnik.getsize(text)[0] > 1015:
        size -= 1
        font_imeninnik = ImageFont.truetype("conf/fonts/troubleside.ttf", size)
        
    draw.text((682, int(550 - font_imeninnik.getsize(text)[1]/2)), text, TEXT_COLOR, font=font_imeninnik)

    text = f"{party_date.day} {MONTHS[party_date.month-1]} в {party_date.hour:0>2}:{party_date.minute:0>2}"
    size = 60
    font_date = ImageFont.truetype("conf/fonts/troubleside.ttf", size)
    while font_date.getsize(text)[0] > 900:
        size -= 1
        font_date = ImageFont.truetype("conf/fonts/troubleside.ttf", size)
        
    draw.text((800, int(680 - font_date.getsize(text)[1]/2)), text, TEXT_COLOR, font=font_date)
    
        
    invite_back = inv_back.copy()        
    draw = ImageDraw.Draw(invite_back)
    
    text = name.upper()
    
    size = 140
    font_name = ImageFont.truetype("conf/fonts/troubleside.ttf", size)
    while font_name.getsize(text)[0] > 1050:
        size -= 1
        font_name = ImageFont.truetype("conf/fonts/troubleside.ttf", size)
    
    draw.text((int(899 - font_name.getsize(text)[0]/2), int(235 - font_name.getsize(text)[1]/2)), text, TEXT_COLOR, font=font_name)
    
    await bot.send_photo(message.chat.id, invite_back)
    
    invite_img = Image.new('RGB', (invite_back.size[0] + invite_front.size[0], invite_back.size[1]), (255, 255, 255))
    invite_img.paste(invite_front, (0, 0), invite_front)
    invite_img.paste(invite_back, (invite_front.size[0], 0), invite_back)
    
    await bot.send_photo(message.chat.id, invite_img)
    