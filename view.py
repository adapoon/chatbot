import mysql.connector
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

def start(update, context, route_id):
    logging.info("View:")
    
    cnx = mysql.connector.connect(user='comp7940group2', password='hkbuMySQL7940',
                                  host='comp7940-mysql.mysql.database.azure.com',
                                  database='chatbot')
    cursor = cnx.cursor()
    query = ("SELECT name, description FROM route WHERE route_id = %s")
    cursor.execute(query, (route_id, ))
    
    for (name, description) in cursor:
        if description != "":
            msg = name + ":\n" + description
        else:
            msg = name

    update.callback_query.message.reply_text(msg)

    cursor.close()
    cnx.close()
    