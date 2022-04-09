import mysql.connector

mydb = mysql.connector.connect(
    host='comp7940-mysql.mysql.database.azure.com',
    user='comp7940group2',
    passwd='hkbuMySQL7940',
    database='chatbot')

sql = mydb.cursor()

def startCommand(update: Update, context: CallbackContext):

    sql.execute("select region from chatbot.route group by region")
    sql_result = sql.fetchall() 
    markup = types.ReplyKeyboardMarkup()
    for x in sql_result:
      markup.add(types.ReplyKeyboardButton(x[0]))
      
    buttons = [[KeyboardButton(button1)], [KeyboardButton(button2)], [KeyboardButton(button3)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Which region are you looking for?", reply_markup=markup)



#def browseByRegion():
    #cur = mydb.cursor()
    #cur.execute("SELECT region FROM chatbot.route GROUP BY region")
    #result = cur.fetchall()
    #return result

#print(browseByRegion())


