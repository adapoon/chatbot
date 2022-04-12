from telegram import *
from telegram.ext import * 

SEARCH, RESULT, BROWSE, REGION, DISTRICT, VOTE, TOP10, NEAREST, HELP = range(9)
KEYBOARD = [
    [KeyboardButton("/browse"), KeyboardButton("/search"), KeyboardButton("/vote"), KeyboardButton("/top10")], 
    [KeyboardButton("Nearest routes", request_location=True), KeyboardButton("/help")]
    ]