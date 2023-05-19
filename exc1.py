from flask import Flask
from flask import request
from flask import Response
import requests

import logging
from typing import List, Tuple, cast

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
    PicklePersistence,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "6262706361:AAFqMUJ2vq_dTRbuVgATxH0KYKXV62Q5pic"
 
app = Flask(__name__)
def build_keyboard(current_list: List[int]) -> InlineKeyboardMarkup:
    """Helper function to build the next inline keyboard."""
    return InlineKeyboardMarkup.from_row(
        [InlineKeyboardButton("Help", callback_data=("help", current_list)),
        InlineKeyboardButton("Etherscan", callback_data=("help", current_list)),
        InlineKeyboardButton("Dextools", callback_data=("help", current_list))],

)
def tel_send_message():
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    content = ("Artificial General Intelligence (AGI) - 🟩🟩🟩🟩🟩\n"
        +"0x507ef31852cD2E107d21727D1e5eD40177D0C5e1\n\n"
        +"First Seen: $13,269 MC\n"
        +"Currently:  $46,912 MC\n\n"
        +"Telegram popularity\n"
        +"Mentioned in ⬆️ 35 Channels and ⬆️ 580 Messages\n\n"
        +"Social Links\n"
        +"https://t.me/AGI_Portal\n")
    
    payload = {
                'chat_id': '-1001944664387',
                'text': content
                }
   
    r = requests.post(url,json=payload)
 
    return r
 
def tel_send_image(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
        'caption': "This is a sample image"
    }
 
    r = requests.post(url, json=payload)
    return r
 
@ app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            tel_send_message()
        except:
            print("from index-->")
 
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
    app.run(threaded=True)