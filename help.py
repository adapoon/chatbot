from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector
import const

def start(update, context):
    update.message.reply_text('Helping you helping you.')
    logging.info('Helping you helping you.')

