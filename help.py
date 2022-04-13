from telegram import *
from telegram import ParseMode
from telegram.ext import * 
import logging, os, mysql.connector
import const

def start(update, context):
    msg="This is a bot for hikers.\n\n <b>Find Routes</b>\n /browse - choose a district to find a hiking route\n /search - type keyword(s) to search for hiking routes \n\n <b>Vote</b>\n /vote - choose a route that you like \n /top10 - view voting result : the top 10 hiking routes "
    update.message.reply_text(msg, parse_mode=ParseMode.HTML)

