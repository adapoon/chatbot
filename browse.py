from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import view

#This function show 10 route records.
def start(update, context):
    msg = "Choose a region:\n"
    
    region_list = []
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
                                  
    cursor = cnx.cursor()
    query = ("SELECT DISTINCT region FROM route ORDER BY region")
    cursor.execute(query)
    
    i = 1
    for (region, ) in cursor:
        region_list.append([InlineKeyboardButton(region, callback_data = region)])
        i += 1
      
    update.message.reply_text(msg, reply_markup = InlineKeyboardMarkup(region_list))

    logging.info("Check point 1")
    cursor.close()
    cnx.close()
    
    
def show_district(update: Update, context: CallbackContext):
    region = update.callback_query.data
    context.bot.edit_message_text(chat_id=update.effective_chat.id, text="<b><u>"+region+"</u></b>", message_id = update.callback_query.message.message_id, parse_mode=ParseMode.HTML)

    msg = "Choose a district:\n"
    
    logging.info("Check point 1")
    district_list = []
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
                                  
    cursor = cnx.cursor()
    query = ("SELECT DISTINCT district FROM route WHERE region = %s ORDER BY district")
    cursor.execute(query, (region, ))
    
    i = 1
    for (district, ) in cursor:
        district_list.append([InlineKeyboardButton(district, callback_data = district)])
        i += 1
      
    update.callback_query.message.reply_text(msg, reply_markup = InlineKeyboardMarkup(district_list))

    logging.info("Check point 2")
    cursor.close()
    cnx.close()


    return ConversationHandler.END
    
    
def show_routes(update: Update, context: CallbackContext):
    district = update.callback_query.data

    logging.info("Check point 10")
    
    context.bot.edit_message_text(chat_id=update.effective_chat.id, text="<b><u>"+district+"</u></b>", message_id = update.callback_query.message.message_id, parse_mode=ParseMode.HTML)

    msg = "Choose a route:\n"
    
    logging.info("Check point 11")
    route_list = []
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
                                  
    cursor = cnx.cursor()
    query = ("SELECT route_id, name FROM route WHERE district = %s ORDER BY route_id LIMIT 10")
    cursor.execute(query, (district, ))
    
    i = 1
    for (route_id, name) in cursor:
        route_list.append([InlineKeyboardButton(name, callback_data = route_id)])
        i += 1
      
    update.callback_query.message.reply_text(msg, reply_markup = InlineKeyboardMarkup(route_list))

    logging.info("Check point 12")
    cursor.close()
    cnx.close()

    return ConversationHandler.END
    
def show_route(update: Update, context: CallbackContext):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    view.show_route(update, context, update.callback_query.data)
    logging.info("Check point 20")

    return ConversationHandler.END
    