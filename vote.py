from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import view
import const

def start(update, context):
    logging.info("vote.start")
    
    msg = "Which route do you like more?\n"
    button_list = []
    
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
    cursor = cnx.cursor()
    query = ("SELECT route_id, name FROM route ORDER BY RAND() ASC LIMIT 4;")
    cursor.execute(query)
    
    a = 65
    for (route_id, name) in cursor:
        button_list.append([InlineKeyboardButton(chr(a)+". " +name, callback_data = route_id)])
        a += 1
    
    update.message.reply_text(msg, reply_markup = InlineKeyboardMarkup(button_list))

    cursor.close()
    cnx.close()
    return const.VOTE
    
def show_result(update: Update, context: CallbackContext):
    logging.info("vote.show_result")
    
    context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    
    msg = ""
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
    cursor = cnx.cursor()
    answer = update.callback_query.data
    
    ''' insert vote data '''
    query = ("INSERT INTO vote (route_id, vote_count) VALUES(%s, 1) ON DUPLICATE KEY UPDATE vote_count = vote_count + 1")
    cursor.execute(query, (answer, ))
    cnx.commit()
    
    ''' show voting result '''
    options = update.callback_query.message.reply_markup.inline_keyboard

    a = 65
    for i in range(len(options)):
        query = ("SELECT name, IFNULL(vote_count, 0) FROM route LEFT JOIN vote ON route.route_id = vote.route_id WHERE route.route_id = %s")
        route_id = options[i][0].callback_data
        cursor.execute(query, (route_id, ))
        
        row = cursor.fetchone()
        if answer == route_id:
            msg += "<b>" + chr(a)+". " + row[0] + " ["+str(row[1])+"]</b>\n";
        else:
            msg += chr(a)+". " + row[0] + " ["+str(row[1])+"]\n";
        a += 1

    msg += "\n" + "Use /top10 to view the most voted routes"

    update.callback_query.message.reply_text(msg, parse_mode=ParseMode.HTML)
        
    return ConversationHandler.END
    