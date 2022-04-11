from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import view

#This function show 10 route records.
def start(update, context):
    msg = "Top 10 hiking routes:\n"
    
    button_list = []
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
                                  
    cursor = cnx.cursor()
    query = ("SELECT route.route_id, name, IFNULL(vote_count, 0) FROM route LEFT JOIN vote ON route.route_id = vote.route_id ORDER BY vote_count DESC LIMIT 10")
    cursor.execute(query)
    
    i = 1
    for (route_id, name, vote_count) in cursor:
        button_list.append([InlineKeyboardButton(str(i)+". " +name + " ["+str(vote_count)+"]", callback_data = route_id)])
        i += 1
      
    update.message.reply_text(msg, reply_markup = InlineKeyboardMarkup(button_list))

    cursor.close()
    cnx.close()
    
    
def show_result(update: Update, context: CallbackContext):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    view.show_route(update, context, update.callback_query.data)
    return ConversationHandler.END
    