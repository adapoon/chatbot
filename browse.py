import mysql.connector
import logging
from telegram import *
from telegram.ext import * 

#This function show 10 route records.
def start(update, context):
    msg = "Browse results:\n"
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
    cursor = cnx.cursor()
    query = ("SELECT name, description FROM route LIMIT 10")
    cursor.execute(query)

    for (name, description) in cursor:
      msg += name+":  "+description+"\n"

    update.message.reply_text(msg)

    cursor.close()
    cnx.close() 