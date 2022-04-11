from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import view

def start(update, context):
    msg = "Which route do you like more?\n"
    
    logging.info("Voting")
    
    button_list = []
    
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
    cursor = cnx.cursor()
    query = ("SELECT route_id, name FROM route ORDER BY RAND() ASC LIMIT 4;")
    cursor.execute(query)
    
    i = 65
    for (route_id, name) in cursor:
        button_list.append([InlineKeyboardButton(chr(i)+". " +name, callback_data = route_id)])
        i += 1
      
    update.message.reply_text(msg, reply_markup = InlineKeyboardMarkup(button_list))

    cursor.close()
    cnx.close()
    
    
def show_list(update: Update, context: CallbackContext):
    logging.info("Voting show_list")
    context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    
    logging.info(str(update.callback_query))
    
 
    return ConversationHandler.END
    