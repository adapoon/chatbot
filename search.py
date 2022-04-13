from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import view
import const

def start(update, context):
    logging.info("search.start")
    
    context.bot.send_message(chat_id=update.message.chat_id, text="Enter keywords to search:", reply_markup=ForceReply(force_reply=True));
    return const.SEARCH
    
def show_result(update, context):
    logging.info("search.show_result")
    
    keywords = update.message.text
    
    msg = "Search result for <code>"+ keywords +"</code>:\n"
    route_list = []
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
                                  
    cursor = cnx.cursor()
    query = ("SELECT route_id, name FROM route WHERE name LIKE %s OR region LIKE %s OR district LIKE %s ORDER BY route_id LIMIT 10")
    cursor.execute(query, ("%"+keywords.strip()+"%", "%"+keywords.strip()+"%", "%"+keywords.strip()+"%"))
    
    rowcount=0
    for (route_id, name) in cursor:
        route_list.append([InlineKeyboardButton(name, callback_data = route_id)])
        rowcount += 1
    
    cursor.close()
    cnx.close()
    
    if rowcount > 0:
        update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(route_list))
        return const.RESULT
    else:
        update.message.reply_text("No matches were found")
        return ConversationHandler.END
    
def show_route(update: Update, context: CallbackContext):
    logging.info("search.show_route")
    
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    view.show_route(update, context, update.callback_query.data)
    return ConversationHandler.END
    