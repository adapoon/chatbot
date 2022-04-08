from telegram import *
from telegram.ext import * 

import logging
import os
import mysql.connector
import search, browse, vote, location

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
    
    dispatcher.add_handler(MessageHandler(Filters.location,
                                        location_resource,
                                        pass_user_data=True))
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("search", search_command))
    dispatcher.add_handler(CommandHandler("vote", vote_command))
    dispatcher.add_handler(CommandHandler("browse", browse_command))


    # To start the bot:
    updater.start_polling()
    updater.idle()


# def echo(update, context):
    # reply_message = update.message.text.upper()
    # logging.info("Update: " + str(update))
    # logging.info("context: " + str(context))
    # context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start_command(update: Update, context: CallbackContext):
    buttons = [
        [KeyboardButton("/search")], 
        [KeyboardButton("/browse")],
        [KeyboardButton("/vote")],
        [KeyboardButton("Nearest routes", request_location=True)],
        [KeyboardButton("/help")]
        ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def location_resource(update: Update, context: CallbackContext) -> None:
    location.start(update, context)
 
def search_command(update: Update, context: CallbackContext) -> None:
    search.start(update, context)
    
def vote_command(update: Update, context: CallbackContext) -> None:
    vote.start(update, context)
    
def browse_command(update: Update, context: CallbackContext) -> None:
    browse.start(update, context)
    
    
    
if __name__ == '__main__':
    main()