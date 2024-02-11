from datetime import datetime

from telebot import types

from PIL import Image, ImageFont, ImageDraw

from .const import *
from .sql import *



# async def makeinvite_1_city(bot, message, city: str, club: str='vtk'):
#     add_invuser_city(f"{message.chat.first_name} {message.chat.last_name} @{message.chat.username}", message.chat.id, city, club)
    
#     await bot.send_message(message.chat.id, "Напишите имя именинника в родительном падеже. Например: Максима", reply_markup=types.ReplyKeyboardRemove())
    