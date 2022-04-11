from telegram import *
from telegram.ext import * 
import mysql.connector
import logging

def start(update, context):
    update.message.reply_text('Helping you helping you.')
    logging.info('Helping you helping you.')

