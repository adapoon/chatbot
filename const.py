from telegram import *
from telegram.ext import * 

SEARCH, RESULT, BROWSE, REGION, DISTRICT, VOTE, TOP10, NEARBY, LOCATION, HELP = range(10)
KEYBOARD = [
    [KeyboardButton("/browse"), KeyboardButton("/search"), KeyboardButton("/vote"), KeyboardButton("/top10")], 
    [KeyboardButton("Nearby routes", request_location=True), KeyboardButton("/help")]
    ]
WELCOME = "Welcome to the HKHikerBot!"