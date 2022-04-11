from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import search, browse, vote, location, view, help, top10

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
    dispatcher.add_handler(CommandHandler("browse", browse_command))
    
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("vote", vote_command)],
                                states={i : [CallbackQueryHandler(vote.show_result)] for i in range(1,518)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )
    
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[MessageHandler(Filters.location, location_message)],
                                states={i : [CallbackQueryHandler(location.show_result)] for i in range(1,518)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("top10", top10_command)],
                                states={i : [CallbackQueryHandler(top10.show_result)] for i in range(1,518)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # To start the bot:
    updater.start_polling()
    updater.idle()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start_command(update: Update, context: CallbackContext):
    # buttons = [
        # [InlineKeyboardButton("/search", callback_data =), InlineKeyboardButton("/browse", callback_data =)], 
        # [InlineKeyboardButton("/vote", callback_data =), InlineKeyboardButton("Nearest routes", callback_data =, request_location=True)],
        # [InlineKeyboardButton("/help", callback_data =)]
        # ]
        
        # button_list.append([InlineKeyboardButton(str(i)+". " +name + " ("+str(round(dist,1))+"km)", callback_data = route_id)])

    buttons = [
        [KeyboardButton("/search"), KeyboardButton("/browse"), KeyboardButton("/vote"), KeyboardButton("/help")], 
        [KeyboardButton("/top10"), KeyboardButton("Nearest routes", request_location=True)]
        ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Official HikeBot!", reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))



def help_command(update: Update, context: CallbackContext) -> None:
    help.start(update, context)

def location_message(update: Update, context: CallbackContext) -> int:
    location.start(update, context)
    return 1
 
def search_command(update: Update, context: CallbackContext) -> None:
    search.start(update, context)
    
def vote_command(update: Update, context: CallbackContext) -> int:
    vote.start(update, context)
    return 1
    
def browse_command(update: Update, context: CallbackContext) -> None:
    browse.start(update, context)
    
def top10_command(update: Update, context: CallbackContext) -> int:
    top10.start(update, context)
    return 1
    
def view_route(update: Update, context: CallbackContext):
    view.start(update, context)
    
def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END   
    
if __name__ == '__main__':
    main()