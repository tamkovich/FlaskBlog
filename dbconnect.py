import MySQLdb


def connection():
    conn = MySQLdb.connect(host="localhost",
                           user='root',
                           passwd='123123abc',
                           db='flaskapp')
    c = conn.cursor()

    return c, conn
