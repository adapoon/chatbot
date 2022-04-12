from telegram import *
from telegram.ext import * 
import logging, os, mysql.connector

SEARCH, BROWSE, REGION, DISTRICT, VOTE, TOP10, NEAREST, HELP = range(8)

def start(update, context):
    update.message.reply_text('Helping you helping you.')
    logging.info('Helping you helping you.')

