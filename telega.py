import logging
import random
from os import environ as env

import telegram.ext

import Tools

from Achievement import Achievement, Style
from Styles import styles

from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Commands #
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def setlang(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('setlang')


def achlang(update: Update, context: CallbackContext) -> None:
    keyboard = []
    for lang in styles[context.chat_data.get('style', 0)].get_langs():
        keyboard.append([InlineKeyboardButton(f"langs.{lang}", callback_data=f"achlang.{lang}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("achlang.select", reply_markup=reply_markup)


def setstyle(update: Update, context: CallbackContext) -> None:
    keyboard = []
    for i, st in enumerate(styles):
        keyboard.append([InlineKeyboardButton(st.get_name(), callback_data=f"setstyle.{i}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("setstyle.select", reply_markup=reply_markup)

# ======== #


def create_achievement(update: Update, context: CallbackContext) -> None:
    # Checking name & description
    vals = Achievement.parse_message(update.message.text)
    for err in Achievement.check_values(**vals):
        update.message.reply_text(err)
        vals = None
    if not vals:
        return

    # Icon
    vals['icon'] = Tools.search_image(vals['name'])

    # Style
    i = context.chat_data.get('style', 0)
    if i < 0:
        i = random.randint(0, len(styles))
    i = i if 0 <= i < len(styles) else 0  # Checking index
    vals['style'] = styles[i]

    # Setting language
    resp = vals['style'].change_lang(context.chat_data.get('ach_lang', 'ENG'))
    if resp:
        update.message.reply_text("warning.ach.lang.none")

    ach = Achievement(**vals)
    gen = ach.generate()
    if type(gen) is str:
        update.message.reply_text(gen)
    else:
        update.message.reply_photo(gen)


def testphoto(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("testphoto")


def callback_button(update: Update, context: CallbackContext) -> None:
    # Commands #
    def setstyle(params):
        context.chat_data['style'] = int(params)
        update.callback_query.message.reply_text("setstyle.success")

    def achlang(params):
        context.chat_data['ach_lang'] = params
        update.callback_query.message.reply_text("achlang.success")
    # ======== #
    commands = {
        'setstyle': setstyle,
        'achlang': achlang
    }

    query = update.callback_query
    query.answer()
    data = query.data.split('.', 1)
    commands.get(data[0], lambda p: None)(data[1])


def main() -> None:
    """Start the bot."""
    # Creating database connection
    # db = DBHelper.Database("Config/Database.json", functions=Tools.DB_FUNCS)

    # Create the Updater and pass it bot's token.
    updater = Updater(env.get("TELEGRAM_TOKEN"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Commands #
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("setlang", setlang))
    dispatcher.add_handler(CommandHandler("achlang", achlang))
    dispatcher.add_handler(CommandHandler("setstyle", setstyle))
    # dispatcher.add_handler(CommandHandler("mystyles", help_command))
    # dispatcher.add_handler(CommandHandler("addstyle", help_command))
    # ======== #

    # Messages #
    dispatcher.add_handler(MessageHandler(~Filters.command & Filters.text, create_achievement))
    dispatcher.add_handler(MessageHandler(~Filters.command & Filters.text & Filters.photo, testphoto))
    # ======== #

    # Buttons #
    dispatcher.add_handler(CallbackQueryHandler(callback_button))
    # ======= #

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
