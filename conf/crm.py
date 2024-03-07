from datetime import datetime

from telebot import types

from telegram_bot_calendar import LSTEP_tr

from PIL import Image, ImageFont, ImageDraw

from .const import *
from .classes import CRMClient
from .sql import *



async def process_dialog_crm(bot, message, d_status, data):    
    if d_status.startswith("crm_client"):
        await process_crm_client(bot, message, d_status, data)
    
    # if message.text == "Ангарск":
    #     return await makeinvite_1_city(bot, message, "Ангарск", 'vtk')
    # elif message.text == "Братск":
    #     return await makeinvite_1_city(bot, message, "Братск", 'br')
    # else:
    #     status = get_invuser_status(message.chat.id)
    #     print(f"Invite status: {status}")
        
    # if status and status != "complete":
    #     if status == "imeninnik_name":
    #         return await makeinvite_2_imeninnikname(bot, message)
    #     if status == "date":
    #         calendar, step = MyTranslationCalendar().build()
    #         bot.send_message(message.chat.id,
    #                         f"Выберите {LSTEP_tr[step]}",
    #                         reply_markup=calendar)
    #     if status == "minutes":
    #         return await makeinvite_3_minutes(bot, message)
    #     if status == "name":
    #         return await makeinvite_4_image(bot, message)


async def process_crm_client(bot, message, d_status, data):
    status = False
    
    if message.text == "Найти":
        return await crm_client_find_1(bot, message)
    elif message.text == "Добавить":
        return await crm_client_add_1(bot, message)
    else:
        status, data = get_dialog_status(message.chat.id)
        print(f"CRM-client status: {status}")
        
    if status == 'crm_client_find':
        return await crm_client_find_2(bot, message)
        
        
async def crm_client_find_1(bot, message):
    set_dialog_status(message.chat.id, 'crm_client_find')
    
    await bot.send_message(message.chat.id, "Введите номер клиента", reply_markup=types.ReplyKeyboardRemove())
    
    
async def crm_client_find_2(bot, message):
    phone = message.text.lower()
    phone = phone.replace('+', '')
    
    # Кнопка для отмены
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Отмена")
    markup.add(btn1)
    
    # Если нажали кнопку (или ввели) Отмена - сбросить статус
    if phone == "отмена":
        set_dialog_status(message.chat.id, '-')
        return await bot.send_message(message.chat.id, "👍", reply_markup=types.ReplyKeyboardRemove())
    
    # Приводим номер к стандарту 7**********
    if len(phone) == 10:
        phone = '7' + phone
    if phone[0] == '8':
        phone = '7' + phone[1:]
        
    # Проверка корректности номера (начинается с 7, 11 символов, все цифры)
    if phone[0] != '7' or len(phone) != 11 or not phone.isdigit():
        # Поиск клиента по имени в базе
        client = await find_client(bot, message.text)
        if not client:
            return await bot.send_message(message.chat.id, f"Клиент с именем '{message.text}' не найден. Повторите", reply_markup=markup)
    else:
        # Поиск клиента по телефону в базе
        client = await find_client(bot, phone)
        if not client:
            return await bot.send_message(message.chat.id, f"Клиент с номером '+{phone}' не найден. Повторите", reply_markup=markup)
        
    
    await bot.send_message(message.chat.id, f"{client.uid}: {client.name} (+{client.phone})", reply_markup=markup)


async def crm_client_add_1(bot, message):
    pass



async def find_client(bot, promt: str):
    promt = promt.lower()
    
    data = await bot.db.select("*", "crm_clients", where=f"WHERE phone = '{promt}' OR secondphone = '{promt}'")
    
    if not data:
        data = await bot.db.select("*", "crm_clients", where=f"WHERE LOWER(CONCAT(surname, ' ', name, ' ', midname)) LIKE LOWER('%{promt}%')")
    
    if not data:
        return None
    
    return CRMClient(**data)