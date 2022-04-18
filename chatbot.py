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
        
    # PATH: Conversation Handler
    dispatcher.add_handler(ConversationHandler(
                                entry_points=[
                                    CommandHandler("vote", vote.start),
                                    CommandHandler("search", search.start),
                                    CommandHandler("browse", browse.show_region),
                                    CommandHandler("nearby", nearby.start),
                                    CommandHandler("top10", top10.start),
                                    MessageHandler(Filters.location, nearby.show_routes)
                                    ],
                                states={
                                    const.VOTE : [CallbackQueryHandler(vote.show_result)],
                                    const.SEARCH : [MessageHandler(Filters.text , search.show_result)],
                                    const.RESULT : [CallbackQueryHandler(search.show_route)],
                                    const.BROWSE : [CallbackQueryHandler(browse.show_district)],
                                    const.REGION : [CallbackQueryHandler(browse.show_routes)],
                                    const.DISTRICT : [CallbackQueryHandler(browse.show_route)],
                                    const.NEARBY : [MessageHandler(Filters.location, nearby.show_routes)],
                                    const.LOCATION : [CallbackQueryHandler(nearby.show_route)],
                                    const.LOCATION : [CallbackQueryHandler(nearby.show_route)],
                                    const.TOP10 : [CallbackQueryHandler(top10.show_result)]
                                    },
                                fallbacks=[CommandHandler('cancel', cancel)],
                                allow_reentry=True
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