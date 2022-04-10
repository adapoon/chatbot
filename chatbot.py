from telegram import *
from telegram.ext import * 

import logging
import os
import mysql.connector
import search, browse, vote, location, view

def main():
    # Load your token and create an Updater for your Bot
    
    
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher


    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("search", search_command))
    dispatcher.add_handler(CommandHandler("vote", vote_command))
    dispatcher.add_handler(CommandHandler("browse", browse_command))

    dispatcher.add_handler(ConversationHandler(
                                entry_points=[MessageHandler(Filters.location, location_message)],
                                states={i : [CallbackQueryHandler(reply)] for i in range(1,518)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )


    

    # To start the bot:
    updater.start_polling()
    updater.idle()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start_command(update: Update, context: CallbackContext):
    buttons = [
        [KeyboardButton("/search"), KeyboardButton("/browse")], 
        [KeyboardButton("/vote"), KeyboardButton("Nearest routes", request_location=True)],
        [KeyboardButton("/help")]
        ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!", reply_markup=ReplyKeyboardMarkup(buttons))



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def location_message(update: Update, context: CallbackContext) -> int:
    location.start(update, context)
    return 1
 
def search_command(update: Update, context: CallbackContext) -> None:
    search.start(update, context)
    
def vote_command(update: Update, context: CallbackContext) -> None:
    vote.start(update, context)
    
def browse_command(update: Update, context: CallbackContext) -> None:
    browse.start(update, context)
    
def view_route(update: Update, context: CallbackContext):
    view.start(update, context)
    
def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END   
    
def reply(update: Update, context: CallbackContext):
    logging.info("Reply: " + update.callback_query.data)
    view.start(update, context, update.callback_query.data)
    # logging.info("update: " + str(update))
    # logging.info("context: " + str(context))
    return 1
    
if __name__ == '__main__':
    main()