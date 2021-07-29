import sqlite3

class queryProcess() :
    def __init__(self):
        super().__init__()
        self.db_path = "./all_users.db"
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
        sql = "CREATE TABLE IF NOT EXISTS USERS(" \
                "userid text PRIMARY KEY," \
                "username text," \
                "phone text," \
                "address text," \
                "userpw text," \
                "email text," \
                "pw_error INTEGER)"
        try :
            self.cursor.execute(sql)
            return True
        except :
            return False
    
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

    def select_id(self,name,phone) :
        sql = "SELECT userid FROM USERS WHERE username = '" + name + "' AND phone = '" + phone + "'"
        try :
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        except :
            return False
    
    def select_pw(self,id,name,phone) :
        sql = "SELECT userpw FROM USERS WHERE userid = '" + id + "' AND username = '" + name + "' AND phone = '" + phone + "'"
        try :
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        except :
            return False

    # 로그인 실패 시, pw_error += 1 // 성공 시, pw_error = 0
    def update_pw_error_cnt(self, id, arg) :
        # 실패 했을 경우
        if arg == 'fail' :
            try :
                sql = "SELECT pw_error FROM USERS WHERE userid = '" + id + "'"
                self.cursor.execute(sql)
                pw_error_cnt = self.cursor.fetchall()[0]
                sql = "UPDATE USERS SET pw_error = " + str(pw_error_cnt[0] + 1) + " WHERE userid = '" + id + "'"
                self.cursor.execute(sql)
                return True
            except :
                return False

        # 성공 했을 경우
        else :
            sql = "UPDATE USERS SET pw_error = 0 WHERE userid = '" + id + "'"
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
            result = self.cursor.fetchone()
            return result
        except :
            return False


if __name__ == "__main__" :
    queryProcess = queryProcess()
    #print(queryProcess.create())
    #print(loging.insert('flow54','김지현','01099830448','서울특별시','dufdl0504','',0))
    #print(loging.select_from_userid('admin'))
    #print(loging.update_pw_error_cnt('admin'))
    #print(queryProcess.select_id('김지현','01099830448'))