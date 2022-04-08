import mysql.connector






def start(update, context):
    msg = "Search results:\n"
    
    update.message.reply_text("Update: " + str(update))
    update.message.reply_text("context: " + str(context))
    
    # cnx = mysql.connector.connect(user='comp7940group2', password='hkbuMySQL7940',
                                  # host='comp7940-mysql.mysql.database.azure.com',
                                  # database='chatbot')
    # cursor = cnx.cursor()
    # query = ("SELECT name, district FROM route LIMIT 10")
    # cursor.execute(query)
    
    # for (name, district) in cursor:
      # msg += name+" "+district+"\n"

    # update.message.reply_text(msg)
    
    # cursor.close()
    # cnx.close()