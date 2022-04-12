from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import const

def show_route(update, context, route_id):
    logging.info("View:")
    media = []
    context.bot.answer_callback_query(callback_query_id=update.callback_query.id, text="Retrieving hiking route...")

    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
    cursor = cnx.cursor()
    query = ("SELECT name, description, region, district, image, map, length, duration, elevation, latitude, longitude FROM route WHERE route_id = %s")
    cursor.execute(query, (route_id, ))
    
    for (name, description, region, district, image, map, length, duration, elevation, latitude, longitude) in cursor:
        hh = duration // 60
        mm = duration % 60
        if hh > 0:
            time = str(hh) + " hr " + str(mm) + " min"
        else:
            time = str(mm) + " min"

        msg  = "<b><u>" + name + "</u></b>:\n" 
        msg += "<code>Region    :</code> " + region + "\n" 
        msg += "<code>District  :</code> " + district + "\n" 
        msg += "<code>Length    :</code> " + str(length) + " km\n" 
        msg += "<code>Duration  :</code> " + time + "\n" 
        msg += "<code>Evalation :</code> " + str(elevation) + " m\n" 
        msg += description

    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML, text=msg, disable_web_page_preview=True, reply_markup=ReplyKeyboardMarkup(keyboard=const.KEYBOARD, resize_keyboard=True))

    media.append(InputMediaPhoto('https://comp7940images.blob.core.windows.net/images/'+image));
    media.append(InputMediaPhoto('https://comp7940images.blob.core.windows.net/images/'+map));
    context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)
    
    cursor.close()
    cnx.close()
    