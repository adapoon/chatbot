from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector

SEARCH, BROWSE, REGION, DISTRICT, VOTE, TOP10, NEAREST, HELP = range(8)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Enter keywords to search:", reply_markup=ForceReply(force_reply=True));
    return SEARCH
    
def show_result(update, context):
    keywords = update.message.text
    logging.info("Check point 50")

    msg = "Search result for <code>"+ keywords +"</code>:\n"
    route_list = []
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
                                  
    cursor = cnx.cursor()
    query = ("SELECT route_id, name FROM route WHERE name LIKE %s LIMIT 10")
    cursor.execute(query, ("%"+keywords+"%", ))
    
    i = 1
    for (route_id, name) in cursor:
        route_list.append([InlineKeyboardButton(name, callback_data = route_id)])
        i += 1
      
    update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup = InlineKeyboardMarkup(route_list))

    cursor.close()
    cnx.close()

    return ConversationHandler.END