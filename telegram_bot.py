import logging
import psutil
import time
from os import environ as env, getpid
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import DBHelper
import Lang
import Tools
import Styles
from Achievement import Achievement


# Logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Useful variables #
START_TIME = int(time.time())
# ================ #


# Commands #
def start(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('new', True):
        context.bot_data['users_c'] = context.bot_data.get('users_c', 0) + 1
        logger.info(f"New user! {update.effective_user.name}")
        context.user_data['new'] = False
    update.message.reply_text(Lang.get('command.start', context.chat_data.get('lang')))


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Lang.get('command.help', context.chat_data.get('lang')))


def params_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Lang.get('command.null', context.chat_data.get('lang')))


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


def stats(update: Update, context: CallbackContext) -> None:
    keys = {
        'ach_global': context.bot_data.get('ach_generated', 0),
        'ach_chat': context.chat_data.get('ach_generated', 0),
        'users_count': context.bot_data.get('users_c', 0),
        'user_styles': '0 (coming soon)'
    }
    update.message.reply_text(Lang.get('command.stats.achievement', context.chat_data.get('lang'), **keys))


def sys_stats(update: Update, context: CallbackContext) -> None:
    def get_uptime() -> dict:
        delta = int(time.time()) - START_TIME
        return {
            'ut_d': str(delta // 86400),
            'ut_h': str(delta // 3600 % 60),
            'ut_m': str(delta // 60 % 60)
        }

    mem = psutil.Process(getpid()).memory_info()
    keys = {
        **get_uptime(),     # ut_d, ut_h, ut_m
        'ram_p': "{0:.2f}".format(mem.vms / mem.rss * 100),
        'ram_mb': str(mem.vms // (1024 ** 2))
    }
    update.message.reply_text(Lang.get('command.stats.sys', context.chat_data.get('lang'), **keys))

# ======== #


# Messages handlers #
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
    elif context.chat_data.get('image_url'):
        image = context.chat_data.get('image_url')
        context.chat_data['image_url'] = None

    vals['icon'] = Tools.download_image(image or Tools.search_image(vals['name']))
    vals['style'] = Styles.get(context.chat_data.get('style'))

    # Setting language
    ach_lang = context.chat_data.get('ach_lang', 'ENG')
    if vals['style'].change_lang(ach_lang) != 'ok':
        update.message.reply_text(Lang.get('error.achievement.no_lang', lang, lang=ach_lang, style=vals['style'].get_name(lang)))

    ach = Achievement(**vals)
    gen = ach.generate()
    if type(gen) is str:
        update.message.reply_text(Lang.get(gen, lang))
    else:
        update.message.reply_photo(gen)
        # Incrementing stats
        context.bot_data['ach_generated'] = context.bot_data.get('ach_generated', 0) + 1
        context.chat_data['ach_generated'] = context.chat_data.get('ach_generated', 0) + 1

    # TODO: add buttons (other images and styles)


def require_name(update: Update, context: CallbackContext) -> None:
    photos = update.message.photo
    context.chat_data['image_url'] = photos[1 if len(photos) > 1 else 0].get_file().file_path
    update.message.reply_text(Lang.get("achievement.require_name", context.chat_data.get('lang')))
# ================= #


# Keyboard handlers #
def callback_button(update: Update, context: CallbackContext) -> None:
    lang = context.chat_data.get('lang')

    # Commands #
    def btn_setstyle(params):
        context.chat_data['style'] = int(params)
        stylename = Lang.get("keyboard.setstyle.random", lang) if int(params) < 0 else Styles.get(int(params)).get_name(lang)
        update.callback_query.message.reply_text(Lang.get('command.setstyle.changed', lang, style=stylename))

    def btn_achlang(params, same_lang=False):
        context.chat_data['ach_lang'] = params
        update.callback_query.message.reply_text(Lang.get('command.achlang.changed', params if same_lang else lang, lang=Lang.get_lang(params, True)))

    def btn_setlang(params):
        context.chat_data['lang'] = params
        update.callback_query.message.reply_text(Lang.get('command.setlang.changed', params, lang=Lang.get_lang(params, True)))
        btn_achlang(params, True)
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
# ================= #


def main() -> None:
    logger.info("Starting Telegram bot")

    # Creating database connection and persistence
    db = DBHelper.Database("Config/Database.json")
    persistence = Tools.DBHelperPersistence(db)

    # Create the Updater and pass it bot's token.
    updater = Updater(env.get("TELEGRAM_TOKEN"), persistence=persistence, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Commands #
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("params", params_command))
    dispatcher.add_handler(CommandHandler("setlang", setlang))
    dispatcher.add_handler(CommandHandler("achlang", achlang))
    dispatcher.add_handler(CommandHandler("setstyle", setstyle))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("sysstatus", sys_stats))
    # ======== #

    # Messages #
    dispatcher.add_handler(MessageHandler(~Filters.command & Filters.text | Filters.photo & Filters.caption, create_achievement))
    dispatcher.add_handler(MessageHandler(~Filters.command & Filters.photo, require_name))
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
