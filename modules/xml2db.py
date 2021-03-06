#import sqlite3 as sql
import mysql.connector
from flask import jsonify

status = True

def main(contents):
    dbCon = connectDB()
    all = xmltoDB(contents)
    if dbCon is not None and all is not None:
        insertToDB(dbCon, all)
    text=fetch(dbCon)
    text = {'content': text}
    text['status'] = status
    text = jsonify(text)
    return text


def connectDB():
    mydb = mysql.connector.connect(user='root',
                                   password='123',
                                   host='localhost',
                                   database='tanuj'
                                   )
    query = 'CREATE TABLE IF NOT EXISTS CONTACTS2(id INT PRIMARY KEY, name VARCHAR(30), email VARCHAR(30), phone VARCHAR(15))'
    cursor = mydb.cursor()
    cursor.execute(query)
    mydb.commit()
    return mydb


def xmltoDB(contents):
    all = []
    contents = contents.strip()
    content = contents.split('>', 1)
    array = content[1].strip()
    array = array.strip()
    new = array[1:len(content[1]) - len(content[0]) - 3]
    new1 = new.strip()
    sp = new.split('>', 1)
    spn = sp[0] + '>'
    spn1 = new1.split(spn)
    spn2 = spn1[1:]

    for row in spn2:
        row = row.strip()
        row1 = row[:-(len(spn) + 1)]
        row1 = row1.strip()
        sprow = row1.split('<')
        sprowf = sprow[1::2]
        dict = {}
        for i in sprowf:
            i1 = i.split('>')
            i2 = i1[1].strip()
            j1 = i1[0]
            key = j1.strip()
            value = i2.strip()

            if value.isdigit():
                dict[key] = int(value)
            else:
                dict[key] = value
        if dict:
            t = (dict['id'], dict['name'], dict['email'], dict['mobile'])
            t = tuple(t)
            all.append(t)
    return all


def insertToDB(db, tuples):
    try:
        cursor = db.cursor()
        cursor.executemany('''INSERT INTO CONTACTS2(id, name, email, phone) VALUES(%s,%s,%s,%s)''', tuples)
        db.commit()
        print('Data imported successfully!')
        global status
        status = True
    except:
        print('An error occurred while adding data!\n')
        global status
        status = False


def fetch(db):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM CONTACTS2')
        data = cursor.fetchall()
        print('Table contains-\n')
        print(data)
        return data
    except:
        print('An error occurred while fetching data!\n')
