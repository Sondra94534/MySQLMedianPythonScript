"""
Created 04/06/2020 
@author Sondra Hoffman
"""

import mysql.connector
from mysql.connector import Error

def connect():
    """Connect to MySQL database"""
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost', database='world_x',
                                       user='jump', password='#######')
        cur = conn.cursor()

        if conn.is_connected():
            print('Connected to MySQL database')

        cur.execute('SELECT vtype FROM vehicle_type WHERE vtype LIKE "%otorcycle%";')
        cycleList = cur.fetchall()

        selectSQL = '''
                     SELECT t.vtype, a.accident_severity
                     FROM accidents_2016 AS a
                     JOIN vehicles_2016 AS v ON a.accident_index = v.Accident_Index
                     JOIN vehicle_type AS t ON v.Vehicle_Type = t.vcode
                     WHERE t.vtype LIKE %s
                     ORDER BY a.accident_severity;'''

        insertSQL = '''
                     INSERT INTO accident_medians VALUES (%s, %s);'''

        for cycle in cycleList:
            cur.execute(selectSQL, (cycle[0],))
            accidents = cur.fetchall()
            quotient, remainder = divmod(len(accidents), 2)
            if remainder:
                med_sev = accidents[quotient][1]
            else:
                med_sev = (accidents[quotient][1] + accidents[quotient + 1][1]) / 2
            print('Finding median for', cycle[0])
            cur.execute(insertSQL, (cycle[0], med_sev))
            conn.commit()

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    connect()
