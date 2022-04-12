from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import search, browse, vote, location, view, help, top10

def main():
    # Load your token and create an Updater for your Bot
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    regions = ["Hong Kong Island", "Kowloon", "New Territories", "Outlying Islands"]
    districts = ["Central and Western", "Eastern", "Islands", "Kowloon City", "Kwai Tsing", "Kwun Tong", "North", "Sai Kung", "Sha Tin", "Sham Shui Po", "Southern", "Tai Po", "Tsuen Wan", "Tuen Mun", "Wan Chai", "Yuen Long"]

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    

    # PATH: Start
    dispatcher.add_handler(CommandHandler("start", start_command))
        
    dispatcher.add_handler(CommandHandler("search", search_command))
    
    # PATH: Browse
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("browse", browse_command)],
                                states={regions[i] : [CallbackQueryHandler(browse.show_district)] for i in range(len(regions))},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # PATH: Browse -> Region
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CallbackQueryHandler(browse.show_routes, pattern=districts[i]) for i in range(len(districts))],
                                states={districts[i] : [CallbackQueryHandler(browse.show_routes)] for i in range(len(districts))},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )
                        
    # PATH: Browse -> Region -> District
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CallbackQueryHandler(browse.show_route, pattern=str(i)) for i in range(1, 533)],
                                states={i : [CallbackQueryHandler(browse.show_route)] for i in range(1,533)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # PATH: Vote
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("vote", vote_command)],
                                states={i : [CallbackQueryHandler(vote.show_result)] for i in range(1,533)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )
    
    # PATH: Nearest routes
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[MessageHandler(Filters.location, location_message)],
                                states={i : [CallbackQueryHandler(location.show_result)] for i in range(1,533)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # PATH: Top 10
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("top10", top10_command)],
                                states={i : [CallbackQueryHandler(top10.show_result)] for i in range(1,533)},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # PATH: Help
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()


def start_command(update: Update, context: CallbackContext):
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
 
def search_command(update: Update, context: CallbackContext) -> str:
    search.start(update, context)
    return "Hong Kong Island"
    
def vote_command(update: Update, context: CallbackContext) -> int:
    vote.start(update, context)
    return 1
    
def browse_command(update: Update, context: CallbackContext) -> str:
    browse.start(update, context)
    return "Hong Kong Island"
    
def top10_command(update: Update, context: CallbackContext) -> int:
    top10.start(update, context)
    return 1
    
def view_route(update: Update, context: CallbackContext):
    view.start(update, context)
    
def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END   
    
if __name__ == '__main__':
    main()