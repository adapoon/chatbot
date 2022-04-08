import mysql.connector
import logging
import haversine as hs

def start(update, context):
    msg = "Nearest routes:\n"
    
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    
    # msg = update.message
    # update.message.reply_text('lat: {}, lng: {}'.format(msg.location.latitude, msg.location.longitude))
    
    
    cnx = mysql.connector.connect(user='comp7940group2', password='hkbuMySQL7940',
                                  host='comp7940-mysql.mysql.database.azure.com',
                                  database='chatbot')
    cursor = cnx.cursor()
    query = ("SELECT name, SQRT(POWER(latitude-%s, 2) + POWER(longitude-%s, 2)) as distance, latitude, longitude FROM route ORDER BY distance ASC LIMIT 10;")
    cursor.execute(query, (update.message.location.latitude, update.message.location.longitude))
    
    i = 1
    for (name, distance, latitude, longitude) in cursor:
        loc1 = (latitude, longitude)
        loc2 = (update.message.location.latitude, update.message.location.longitude)
        dist = hs.haversine(loc1, loc2)
    
        msg += str(i)+". " + name + " ("+str(round(dist,1))+"km)\n"
        i += 1
      

    update.message.reply_text(msg)
    
    cursor.close()
    cnx.close()