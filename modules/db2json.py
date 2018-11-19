import mysql.connector
from flask import jsonify

def main():
    db = connectDB()
    data = fetch(db)
    json=convertToJson(data)
    data = {'source': data}
    data['result'] = json
    text = jsonify(data)
    return text

def connectDB():
    mydb = mysql.connector.connect(user='root',
                                   password='123',
                                   host='localhost',
                                   database='tanuj'
                                   )
    return mydb


def fetch(db):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM CONTACTS2')
        data = cursor.fetchall()
        return data
    except:
        print('An error occurred while fetching data!\n')

def convertToJson(data):
   json='{\n"data" : [\n'
   for row in data:
       start=''
       if row != data[0]: start+=',\n'
       start+='{\n'
       start+='"id" : '+str(row[0])+',\n"name" : "' + row[1]+'",\n"email" : "'+row[2]+'",\n"mobile" : "'+row[3]+'"\n}'
       json+=start
   json+='\n]\n}'
   return json
