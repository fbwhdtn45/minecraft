import sqlite3

conn = sqlite3.connect(r"C:\Users\Lee\Documents\python\all_users.db",isolation_level=None)
cursor = conn.cursor()

def create() :
    sql = "CREATE TABLE IF NOT EXISTS USERS(" \
            "userid text PRIMARY KEY," \
            "username text," \
            "phone text," \
            "address text," \
            "userpw text," \
            "email text," \
            "pw_error INTEGER)"
    return sql

def insert() :
    sql = "INSERT INTO USERS VALUES('root','관리자','00000000000','부산광역시'," \
          "'1234','',0)"
    return sql

def select() :
    sql = "SELECT * FROM USERS"
    return sql

cursor.execute(select())
print(cursor.fetchone()[0] == 'admin')

conn.close()