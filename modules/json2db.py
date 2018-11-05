## all the source code for the first module (part) of the project goes here
## other modules will also be made as other python files under this folder 'modules'
import sqlite3 as sql

def main(contents):
    db = connectDB()
    tuples = parseJSON(contents)
    if dict is not None:
        insertToDB(db, tuples)
    fetch(db)


def connectDB():
    con = sql.connect('Primary.db')
    # creating a new table
    query = 'CREATE TABLE IF NOT EXISTS CONTACTS(id INT PRIMARY KEY, name VARCHAR(30), email VARCHAR(30), phone VARCHAR(15))'
    con.execute(query)
    con.commit()
    return con


def parseJSON(contents):
    tuples = []
    contents = contents.strip()
    contents = contents[1:len(contents) - 1]
    contents = contents.strip()
    data = contents.split(':', 1)
    if data[0].strip() != '"data"':
        return None
    else:
        arr = data[1].strip()
        arr = arr[1: len(arr) - 1]
        arr = arr.strip()
        arr = arr[1:len(arr)]
        rows = arr.split('{')
        for row in rows:
            row = row.strip()
            keys = row.split(',')
            if len(keys) > 4:
                del keys[len(keys)-1]
            all=[]
            for key in keys:
                key = key.strip()
                pair=key.split(':',2)
                value=pair[1].strip()
                value=value.split('"',2)
                if value[0] != '':
                    all.append(int(value[0]))
                else:
                    all.append(value[1])
            tup=tuple(all)
            tuples.append(tup)

        return tuples


def insertToDB(db, tuples):
    try:
        cursor = db.cursor()
        cursor.executemany('''INSERT INTO CONTACTS(id, name, email, phone) VALUES(?,?,?,?)''', tuples)
        db.commit()
    except:
        print('An error occurred while adding data!\n')


def fetch(db):
    try:
        cursor=db.cursor()
        cursor.execute('SELECT * FROM CONTACTS')
        data=cursor.fetchall()
        print('Table contains-\n')
        for row in data:
            print(row)
    except:
        print('An error occurred while fetching data!\n')

