import logging
from io import BytesIO
from os import environ as env
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import Lang
import Tools
import Styles
from Achievement import Achievement


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Commands #
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Lang.get('command.start'), context.chat_data.get('lang'))


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Lang.get('command.help'), context.chat_data.get('lang'))


def params_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Lang.get('command.params'), context.chat_data.get('lang'))


def setlang(update: Update, context: CallbackContext) -> None:
    keyboard = []

    for lang in Lang.get_langs():
        keyboard.append([InlineKeyboardButton(Lang.get_lang(lang), callback_data=f"setlang.{lang}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(Lang.get('command.setlang.select', context.chat_data.get('lang')),
                              reply_markup=reply_markup)


def achlang(update: Update, context: CallbackContext) -> None:
    keyboard = []

    for lang in Styles.get(context.chat_data.get('style')).get_langs():
        keyboard.append([InlineKeyboardButton(Lang.get_lang(lang), callback_data=f"achlang.{lang}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(Lang.get('command.achlang.select', context.chat_data.get('lang')), reply_markup=reply_markup)


def setstyle(update: Update, context: CallbackContext) -> None:
    lang = context.chat_data.get('lang')
    keyboard = []

    for i, st in enumerate(Styles.styles):
        keyboard.append([InlineKeyboardButton(st.get_name(), callback_data=f"setstyle.{i}")])
    keyboard.append([InlineKeyboardButton(Lang.get('keyboard.setstyle.random', lang), callback_data=f"setstyle.-1")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(Lang.get('command.setstyle.select', lang), reply_markup=reply_markup)

# ======== #


def create_achievement(update: Update, context: CallbackContext) -> None:
    lang = context.chat_data.get('lang')

    # Checking name & description
    vals = Achievement.parse_message(update.message.text or update.message.caption)
    for err in Achievement.check_values(**vals):
        update.message.reply_text(Lang.get(err, lang, **Achievement.LIMITS))
        vals = None
    if not vals:
        return

    # Icon & style
    image = None
    if update.message.photo:
        photos = update.message.photo
        image = photos[1 if len(photos) > 1 else 0].get_file().file_path

    vals['icon'] = Tools.download_image(image or Tools.search_image(vals['name']))
    vals['style'] = Styles.get(context.chat_data.get('style'))

    # Setting language
    ach_lang = context.chat_data.get('ach_lang', 'ENG')
    resp = vals['style'].change_lang(ach_lang)
    if resp:
        update.message.reply_text(Lang.get('error.achievement.no_lang', lang, msg_lang=ach_lang))

    ach = Achievement(**vals)
    gen = ach.generate()
    if type(gen) is str:
        update.message.reply_text(Lang.get(gen, lang))
    else:
        update.message.reply_photo(gen)

    # TODO: add buttons (other images and styles)


def callback_button(update: Update, context: CallbackContext) -> None:
    lang = context.chat_data.get('lang')

    # Commands #
    def btn_setstyle(params):
        context.chat_data['style'] = int(params)
        update.callback_query.message.reply_text(Lang.get('command.setstyle.changed', lang, style=Styles.get(int(params)).get_name()))

    def btn_achlang(params):
        context.chat_data['ach_lang'] = params
        update.callback_query.message.reply_text(Lang.get('command.achlang.changed', lang, lang=Lang.get_lang(params, True)))

    def btn_setlang(params):
        context.chat_data['lang'] = params
        update.callback_query.message.reply_text(Lang.get('command.setlang.changed', lang, lang=Lang.get_lang(params, True)))
    # ======== #

    commands = {
        'setstyle': btn_setstyle,
        'achlang': btn_achlang,
        'setlang': btn_setlang
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
    dispatcher.add_handler(CommandHandler("params", params_command))
    dispatcher.add_handler(CommandHandler("setlang", setlang))
    dispatcher.add_handler(CommandHandler("achlang", achlang))
    dispatcher.add_handler(CommandHandler("setstyle", setstyle))
    # dispatcher.add_handler(CommandHandler("mystyles", help_command))
    # dispatcher.add_handler(CommandHandler("addstyle", help_command))
    # ======== #

    # Messages #
    dispatcher.add_handler(MessageHandler(~Filters.command & Filters.text | Filters.photo & Filters.caption, create_achievement))
    # TODO: add photo handler that require text (name & description)
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
