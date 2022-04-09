import mysql.connector

mydb = mysql.connector.connect(
    host='comp7940-mysql.mysql.database.azure.com',
    user='comp7940group2',
    passwd='hkbuMySQL7940',
    database='chatbot')

sql = mydb.cursor()

def browseByRegion():
    cur = mydb.cursor()
    cur.execute("SELECT region FROM chatbot.route GROUP BY region")
    result = cur.fetchall()
    return result

print(browseByRegion())


