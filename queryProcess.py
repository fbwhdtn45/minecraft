import sqlite3

class queryProcess() :
    def __init__(self):
        super().__init__()
        self.db_path = r"C:\Users\Lee\Documents\python\all_users.db"
        self.conn = sqlite3.connect(self.db_path,isolation_level=None)
        
        self.cursor = self.conn.cursor()
        self.userid = ''
        self.username = ''
        self.phone = ''
        self.address = ''
        self.userpw = ''
        self.email = ''
        self.pw_error = 0

    # DB 생성
    def create(self) :
        self.sql = "CREATE TABLE IF NOT EXISTS USERS(" \
                "userid text PRIMARY KEY," \
                "username text," \
                "phone text," \
                "address text," \
                "userpw text," \
                "email text," \
                "pw_error INTEGER)"
        return self.sql
    
    # 회원가입 시 모든 정보 입력
    def insert(self, id, name, phone, address, pw, email, pw_cnt) :
        sql = "INSERT INTO USERS VALUES('"+ id
        sql += "','" + name
        sql += "','" + phone
        sql += "','" + address
        sql += "','" + pw
        sql += "','" + email
        sql += "'," + str(pw_cnt)
        sql += ")"

        try : 
            self.cursor.execute(sql)
            return True
        except :
            return False

    def select_id(name,phone) :
        sql = "SELECT userid FROM USERS WHERE name ='" + name + "', '" + phone + "'"
        try :
            self.cursor.execute(sql)
            result = self.cursor.fetchall[0]
            return result
        except :
            return False

    # 로그인 실패 시, pw_error += 1
    def update_pw_error_cnt(self, id) :
        sql = "SELECT pw_error FROM USERS WHERE userid = '" + id + "'"
        try :
            self.cursor.execute(sql)
            pw_error_cnt = self.cursor.fetchone()[0] + 1
        except :
            return False

        sql = "UPDATE USERS SET pw_error = " + str(pw_error_cnt) + " WHERE userid = '" + id + "'"
        
        try : 
            self.cursor.execute(sql)
            return True
        except :
            return False
        
    # userid 에 해당한 모든 정보 select
    def select_from_userid(self,id) :
        sql = "SELECT * FROM USERS WHERE userid ='" + id + "'"
        try :
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except :
            return False


if __name__ == "__main__" :
    queryProcess = queryProcess()
    #print(loging.insert('flow54','김지현','01099830448','서울특별시','dufdl0504','',0))
    #print(loging.select_from_userid('admin'))
    #print(loging.update_pw_error_cnt('admin'))