import mysql.connector
import logging
from telegram import *
from telegram.ext import * 

#This function show 10 route records.
def start(update, context):
    msg = "Browse results:\n"
    cnx = mysql.connector.connect(user='comp7940group2', password='hkbuMySQL7940',
                                  host='comp7940-mysql.mysql.database.azure.com',
                                  database='chatbot')
    cursor = cnx.cursor()
    query = ("SELECT name, description FROM route LIMIT 10")
    cursor.execute(query)

    for (name, description) in cursor:
      msg += name+":  "+description+"\n"

    update.message.reply_text(msg)

    cursor.close()
    cnx.close() 