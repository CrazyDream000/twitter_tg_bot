#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""This example showcases how PTBs "arbitrary callback data" feature can be used.

For detailed info on arbitrary callback data, see the wiki page at
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Arbitrary-callback_data

Note:
To use arbitrary callback data, you must install PTB via
`pip install python-telegram-bot[callback-data]`
"""
import logging
import telegram
import tweepy
import requests
import json
from datetime import datetime

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

bot = telegram.Bot(token='6262706361:AAFqMUJ2vq_dTRbuVgATxH0KYKXV62Q5pic')

consumer_key = "YOUR_TWITTER_CONSUMER_KEY"
consumer_secret = "YOUR_TWITTER_CONSUMER_SECRET"
access_token = "YOUR_TWITTER_ACCESS_TOKEN"
access_token_secret = "YOUR_TWITTER_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up the Telegram Bot API credentials
bot_token = "6262706361:AAFqMUJ2vq_dTRbuVgATxH0KYKXV62Q5pic"
chat_id = "@wantedethchannel"
user_id = "YOUR_USER_ID"



async def get_content() -> InlineKeyboardMarkup:    
    text = ("Artificial General Intelligence (AGI) - 🟩🟩🟩🟩🟩\n"
    +"0x507ef31852cD2E107d21727D1e5eD40177D0C5e1\n\n"
    +"First Seen: $13,269 MC\n"
    +"Currently:  $46,912 MC\n\n"
    +"Telegram popularity\n"
    +"Mentioned in ⬆️ 35 Channels and ⬆️ 580 Messages\n\n"
    +"Social Links\n"
    +"https://t.me/AGI_Portal\n")

    """Sends a message with 5 inline buttons attached."""
    HelpBtn = InlineKeyboardButton(text='Help', url='https://www.twitter.com')
    EtherscanBtn = InlineKeyboardButton(text='Etherscan', url='https://etherscan.io/')
    DextoolsBtn = InlineKeyboardButton(text='Dextools', url='https://www.dextools.io/app/en')
    keyboard = InlineKeyboardMarkup.from_row([HelpBtn,EtherscanBtn,DextoolsBtn])
    return text, keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    updates = bot.getUpdates()
    message = updates[-1].message
    user_id = message.from_user.id
    text1, keyboard = await get_content()  
    await bot.send_message(chat_id=chat_id, text=text1, reply_markup=keyboard, disable_web_page_preview=True)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happand to know my work timeens, if the button data is not available. "
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clears the callback data cache"""
    context.bot.callback_data_cache.clear_callback_data()
    context.bot.callback_data_cache.clear_callback_queries()
    await update.effective_message.reply_text("All clear!")


async def list_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    # Get the data from the callback_data.
    # If you're using a type checker like MyPy, you'll have to use typing.cast
    # to make the checker get the expected type of the callback_data
    number, number_list = cast(Tuple[int, List[int]], query.data)
    # append the number to the list
    number_list.append(number)

    await query.edit_message_text(
        text=f"So far you've selected {number_list}. Choose the next item:",
        reply_markup=build_keyboard(number_list),
    )

    # we can delete the data stored for the query, because we've replaced the buttons
    context.drop_callback_data(query)


async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."
    )


def main() -> None:
    """Run the bot."""
    # We use persistence to demonstrate how buttons can still work after the bot was restarted
    persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(bot_token)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(
        CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
    )
    application.add_handler(CallbackQueryHandler(list_button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()