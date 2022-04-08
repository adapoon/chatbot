from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import logging
import os


def main():
    # Load your token and create an Updater for your Bot
    
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher


    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))


    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        update.message.reply_text('You have said ' + msg)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def hello_command(update: Update, context: CallbackContext) -> None:
    name = context.args[0]
    reply_message = "Good day, " + name + "!"
    update.message.reply_text(reply_message)

if __name__ == '__main__':
    main()