import logging
from os import environ as env
from Achievement import Achievement
from Styles import styles
import Tools

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext



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
    update.message.reply_text('achlang')


def styles_command(update: Update, context: CallbackContext) -> None:
    reply = []
    for i, style in enumerate(styles.keys()):
        reply.append(f"#{i}: {style.title()}")
    update.message.reply_text('\n'.join(reply))


def setstyle(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('setstyle')
# ======== #


def create_achievement(update: Update, context: CallbackContext) -> None:
    # Checking message
    msg = update.message.text
    if not msg:
        update.message.reply_text("error.null_text")
        return
    msg = msg.split('\n')
    vals = {
        'style': styles.get('default'),
        'name': msg[0],
        'icon': Tools.search_image(msg[0]),
        'description': msg[1] if len(msg) > 1 else ''
    }

    errs = Achievement.check_values(**vals)
    for err in errs:
        update.message.reply_text(err)
    if len(errs) > 0:
        return

    ach = Achievement(**vals)
    gen = ach.generate()
    if type(gen) is str:
        update.message.reply_text(gen)
    else:
        update.message.reply_photo(gen)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it bot's token.
    updater = Updater(env.get("TELEGRAM_TOKEN"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Commands #
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("setlang", setlang))
    dispatcher.add_handler(CommandHandler("achlang", achlang))
    dispatcher.add_handler(CommandHandler("styles", styles_command))
    dispatcher.add_handler(CommandHandler("setstyle", setstyle))
    # dispatcher.add_handler(CommandHandler("mystyles", help_command))
    # dispatcher.add_handler(CommandHandler("addstyle", help_command))
    # ======== #

    # Messages #
    dispatcher.add_handler(MessageHandler(~Filters.command & Filters.text, create_achievement))
    # ======== #

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
