from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import haversine as hs
import view
import const

def start(update, context):
    logging.info("nearby.start")
    
    update.message.reply_text("Click the Send location button to find nearby routes", reply_markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Send location", request_location=True)]], resize_keyboard=True))

    logging.info("const.NEARBY")
    return const.NEARBY
    
def show_routes(update, context):
    logging.info("nearby.show_routes")
  
    msg = "Nearby routes:"
    button_list = []
    
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
                                  
    cursor = cnx.cursor()
    query = ("SELECT route_id, name, SQRT(POWER(latitude-%s, 2) + POWER(longitude-%s, 2)) as distance, latitude, longitude FROM route ORDER BY distance ASC LIMIT 10;")
    cursor.execute(query, (update.message.location.latitude, update.message.location.longitude))
    
    i = 1
    for (route_id, name, distance, latitude, longitude) in cursor:
        loc1 = (latitude, longitude)
        loc2 = (update.message.location.latitude, update.message.location.longitude)
        dist = hs.haversine(loc1, loc2)
  
        button_list.append([InlineKeyboardButton(str(i)+". " +name + " ("+str(round(dist,1))+"km)", callback_data = route_id)])
        i += 1
      
    update.message.reply_text(msg, reply_markup = InlineKeyboardMarkup(button_list))

    cursor.close()
    cnx.close()
    
    logging.info("const.LOCATION")
    return const.LOCATION
    
def show_route(update: Update, context: CallbackContext):
    logging.info("nearby.show_route")
    
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    view.show_route(update, context, update.callback_query.data)
    
    logging.info("ConversationHandler.END")
    return const.LOCATION
    return ConversationHandler.END
    