from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector

SEARCH, BROWSE, REGION, DISTRICT, VOTE, TOP10, NEAREST, HELP = range(8)

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


    #context.bot.delete_message(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    #context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id)
    #context.bot.edit_message_text(chat_id=update.effective_chat.id, text=name, message_id = update.callback_query.message.message_id, parse_mode=ParseMode.HTML)

    #update.callback_query.message.reply_html(msg)
    #update.callback_query.message.reply_text(msg)
    #logging.info(str(update.callback_query))

    buttons = [
        [KeyboardButton("/browse"), KeyboardButton("/search"), KeyboardButton("/vote"), KeyboardButton("/top10")], 
        [KeyboardButton("Nearest routes", request_location=True), KeyboardButton("/help")]
        ]
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML, text=msg, disable_web_page_preview=True, reply_markup=ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True))
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://comp7940images.blob.core.windows.net/images/'+image)
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://comp7940images.blob.core.windows.net/images/'+map)


    media.append(InputMediaPhoto('https://comp7940images.blob.core.windows.net/images/'+image));
    media.append(InputMediaPhoto('https://comp7940images.blob.core.windows.net/images/'+map));
    context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)
    
    cursor.close()
    cnx.close()
    