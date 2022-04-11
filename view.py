from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector

def start(update, context, route_id):
    logging.info("View:")
    
    cnx = mysql.connector.connect(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASS'],
                                  host=os.environ['MYSQL_HOST'],
                                  database=os.environ['MYSQL_DTBS'])
    cursor = cnx.cursor()
    query = ("SELECT name, description, region, district, image, map, length, duration, elevation FROM route WHERE route_id = %s")
    cursor.execute(query, (route_id, ))
    
    for (name, description, region, district, image, map, length, duration, elevation) in cursor:
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


    logging.info(str(update))
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    #context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    #context.bot.edit_message_text(chat_id=update.effective_chat.id, text=name, message_id = update.callback_query.message.message_id, parse_mode=ParseMode.HTML)

    #update.callback_query.message.reply_html(msg)
    #update.callback_query.message.reply_text(msg)
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML, text=msg)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://comp7940images.blob.core.windows.net/images/'+image)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://comp7940images.blob.core.windows.net/images/'+map)


    cursor.close()
    cnx.close()
    