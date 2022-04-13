from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import search, browse, vote, nearby, view, help, top10
import const

def main():
    # Load your token and create an Updater for your Bot
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # PATH: Start
    dispatcher.add_handler(CommandHandler("start", start_command))
        
    # PATH: Vote
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("vote", vote.start)],
                                states={const.VOTE : [CallbackQueryHandler(vote.show_result)]},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )
    
    # PATH: Search
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("search", search.start)],
                                states={
                                    const.SEARCH : [MessageHandler(Filters.text , search.show_result)],
                                    const.RESULT : [CallbackQueryHandler(search.show_route)]
                                    },
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )
    
    # PATH: Browse
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("browse", browse.show_region)],
                                states={
                                    const.BROWSE : [CallbackQueryHandler(browse.show_district)],
                                    const.REGION : [CallbackQueryHandler(browse.show_routes)],
                                    const.DISTRICT : [CallbackQueryHandler(browse.show_route)]
                                    },
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # PATH: Nearby
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("nearby", nearby.start)],
                                states={
                                    const.NEARBY : [MessageHandler(Filters.location, nearby.show_routes)],
                                    const.LOCATION : [CallbackQueryHandler(nearby.show_route)]
                                    },
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    dispatcher.add_handler(ConversationHandler(
                                entry_points=[MessageHandler(Filters.location, nearby.show_routes)],
                                states={const.LOCATION : [CallbackQueryHandler(nearby.show_route)]},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )



    # PATH: Top 10
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[CommandHandler("top10", top10.start)],
                                states={const.TOP10 : [CallbackQueryHandler(top10.show_result)]},
                                fallbacks=[CommandHandler('cancel', cancel)]
                            )
                        )

    # PATH: Help
    dispatcher.add_handler(CommandHandler("help", help.start))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()


def start_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=const.WELCOME)
    help.start(update, context)

def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END   
    
if __name__ == '__main__':
    main()