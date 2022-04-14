from telegram import *
from telegram import ParseMode
from telegram.ext import * 
import logging, os, mysql.connector
import const

def start(update, context):
    logging.info("help.start")
    msg="""<b>HKHikerBot</b> is a bot for hikers in Hong Kong.
    
<b><u>Hiking Route Information</u></b>
<b>/browse</b> - Explore hiking routes in different regions and districts
<b>/search</b> - Type keyword(s) to search for hiking routes
<b>/nearby</b> - You can also send a location to get the nearest hiking routes!

<b><u>Hiker Community</u></b>
<b>/vote</b> - Vote for a route that you like
<b>/top10</b> - View the top 10 hiking routes according to the voting results

<b>/help</b> - Return to this menu

Developers: 
- LAM Chak Fung
- POON Yuen Mei Ada
- TSOI Wai Chuen Thomas
Data source: https://www.alltrails.com"""

    update.message.reply_text(msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

