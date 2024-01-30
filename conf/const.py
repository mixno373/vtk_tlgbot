import aiohttp, random
import re
from datetime import datetime

from telegram_bot_calendar import DetailedTelegramCalendar

from PIL import Image



random.seed()

APP_LATEST_VERSION = "1.17.2-81"
APP_LATEST_UPDATE_URI = f"/home/ubuntu/bots/lasertag/apk/Diverstat_{APP_LATEST_VERSION}.apk"
APP_STALKER_URI = f"/home/ubuntu/bots/lasertag/apk/Diverstat - Stalker v1.18.0-90.apk"

QRCODES_SAVE_PATH = "statistic/qrcodes"
QRCODES_FILENAME = "{uid}_{lang}_{theme_name}"
BEST_PLAYERS_SAVE_PATH = "statistic/best_players"
BEST_PLAYERS_FILENAME = "Best_Players_{polygon_uid}_{lang}_{sort}_{theme_name}_{limit}_{minimum_games_played}"

VTK_TLG_LT_LOGCHAT_ID = -4059829948

VTK_MANAGERS_IDS = [
  773985834,    # Минеева С.В.
  773211221,    # Минеев М.В.
  1008371645,   # Минеев Н.В.
  544779397,    # Минеев В.В.
]

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

admins_list = [
    638308159215370252,
    554418178940338194,
    659257029172396052,
    650258096098377767,

]

logos_list = {
    638308159215370252: "vtk",
    829769846106488922: "vtk",
    34: "phoenix",
    32: "druzhina",
    757506057110159390: "druzhina",
    650258096098377767: "vtk",
    554418178940338194: "vtk",
    659257029172396052: "vtk",
    1: "vtk",
    37: "vtk",
    38: "vtk",
    47: "vtk",
    688289274151436308: "patriots",
    640160464181133323: "vtk_zima",
    49: "vtk_zima",
    692625321219850311: "bryansk",
    124: "fine_br",
    154: "spetz",
    297: "br",
    298: "sarmat",
    319: "vl",
    302: "stalker",
    175: "default",
}

vtk_users = [
    638308159215370252,
    650258096098377767,
    554418178940338194,
    659257029172396052,
    829769846106488922,
    1
]

DEFAULT_REVIEWS_CHAT_IDS = {
    "vl": "-1001501905733"
}

RALC_POLYGON_UID = 4


TELEGRAM_CHANNELS = {
    "vtk": "-1001189271225",
    "br": "-1001877745134",
    "vl": "-1001501905733"
}

def unix_time():
    return int(datetime.utcnow().timestamp())


def split_int(value, char = "."):
    char = str(char)
    value = str(value)
    pattern = "([0-9]{3})"
    value = value[::-1]
    value = re.sub(pattern, r"\1"+char, value)
    value = value[::-1]
    value = value.lstrip(char)
    return value

def get_int_from_data(data, key, min=1, max=1, default=1):
    try:
        value = int(data[key])
    except:
        value = default
    if value > max:
        value = max
    if value < min:
        value = min
    return value



def is_admin(user):
    try:
        if user.id in admins_list:
            return True
    except:
        pass
    return False

async def say_log(text, description=None, **kwargs):
    url = wh_log_urls.get(kwargs.pop("url", "stats"), wh_log_urls["stats"])
    try:
        kwargs.pop("url")
    except:
        pass

    em = Embed(title=text)
    if description:
        em.description = str(description)
    for key in sorted(kwargs.keys()):
        value = kwargs[key]
        em.add_field(
            name=str(key),
            value=str(value),
            inline=True
        )

    em.timestamp = datetime.utcnow()

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        try:
            await webhook.send(embed=em)
        except Exception as e:
            print(f"webhook: Unknown exception ({e})]")




BADGES_PER_LINE_1 = 5
BADGES_PER_LINE_2 = 4
PLAYERS_PER_PAGE = 19
BEST_PLAYERS_PER_PAGE = 20


PLOT_TIMEZONES_COUNT = 25
PLOT_YAXIS_SCALE = 30

def get_ranges(start, stop, zones):
    zone_length = int((stop - start) / zones)

    ranges = []

    for i in range(zones):
        range_ = [start+i*zone_length, start+(i+1)*zone_length-1]
        if stop - zone_length < range_[1]:
            range_[1] = stop
        ranges.append(range_)

    return ranges




class MyTranslationCalendar(DetailedTelegramCalendar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locale = "ru"
        
        
invite_backs = {
        "vtk": Image.open("conf/img/invite_back_vtk.png"),
        "br": Image.open("conf/img/invite_back_br.png"),
    }
invite_front = Image.open("conf/img/invite_front.png")

MONTHS = [
    "Января",
    "Февраля",
    "Марта",
    "Апреля",
    "Мая",
    "Июня",
    "Июля",
    "Августа",
    "Сентября",
    "Октября",
    "Ноября",
    "Декабря",
]

TEXT_COLOR = (0, 0, 0)