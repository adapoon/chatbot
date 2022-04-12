from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import search, browse, vote, location, view, help, top10

SEARCH, BROWSE, REGION, DISTRICT, VOTE, TOP10, NEAREST, HELP = range(8)

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
        
    # PATH: Vote
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("vote", vote_command)],
                                states={VOTE : [CallbackQueryHandler(vote.show_result)]},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )
    
    # PATH: Search
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("search", search_command)],
                                states={SEARCH : [MessageHandler(Filters.text , search.show_result)]},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )
    
    # PATH: Browse
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("browse", browse_command)],
                                states={
                                    BROWSE : [CallbackQueryHandler(browse.show_district)],
                                    REGION : [CallbackQueryHandler(browse.show_routes)],
                                    DISTRICT : [CallbackQueryHandler(browse.show_route)]
                                    },
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )


    # PATH: Nearest routes
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[MessageHandler(Filters.location, location_message)],
                                states={NEAREST : [CallbackQueryHandler(location.show_result)]},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # PATH: Top 10
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("top10", top10_command)],
                                states={TOP10 : [CallbackQueryHandler(top10.show_result)]},
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
        [KeyboardButton("/browse"), KeyboardButton("/search"), KeyboardButton("/vote"), KeyboardButton("/top10")], 
        [KeyboardButton("Nearest routes", request_location=True), KeyboardButton("/help")]
        ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Official HikeBot!", reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))



def help_command(update: Update, context: CallbackContext) -> None:
    help.start(update, context)

def location_message(update: Update, context: CallbackContext) -> int:
    return location.start(update, context)
 
def search_command(update: Update, context: CallbackContext) -> int:
    return search.start(update, context)
    
def vote_command(update: Update, context: CallbackContext) -> int:
    return vote.start(update, context)
    
def browse_command(update: Update, context: CallbackContext) -> int:
    return browse.start(update, context)
    
def top10_command(update: Update, context: CallbackContext) -> int:
    return top10.start(update, context)
    
def view_route(update: Update, context: CallbackContext):
    view.start(update, context)
    
def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END   
    
if __name__ == '__main__':
    main()