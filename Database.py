import sqlite3
from datetime import datetime

def InsertToDB(humi, temp):
    try:
        con = sqlite3.connect('/home/pi/gitrepo/LabMonitoring/measurement.db',
                                           detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
        cur = con.cursor()
        print("Connected to SQLite")
        cur.execute('''CREATE TABLE IF NOT EXISTS measurement
                (readingTime timestamp PRIMARY KEY, humi real, temp real)''')
        sqlite_insert_with_param = """INSERT INTO 'measurement'
                          ('readingTime', 'humi', 'temp') 
                          VALUES (?, ?, ?);"""
        now = datetime.now()
        data_tuple = (now,humi,temp)
        cur.execute(sqlite_insert_with_param,data_tuple)
        con.commit()
        print('Reading Added to Database')
        cur.close()
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if con:
            con.close()
            print('Database Connection Close')

def ReadFromDB(starttime, endtime):
    try:
        con = sqlite3.connect('measurement.db',
                                           detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
        cur = con.cursor()
        print("Connected to SQLite")
        sqlite_select_query = """SELECT * from measurement 
                                 WHERE readingTime >= ?
                                 AND readingTIme <= ?"""
        cur.execute(sqlite_select_query,(starttime, endtime))
        records = cur.fetchall()
        for row in records:
            print('{} {} {}'.format(row[0],row[1],row[2]))
        cur.close()
        return records
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        if con:
            con.close()
            print('Database Connection Close')